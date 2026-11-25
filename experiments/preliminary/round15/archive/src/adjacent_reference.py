"""One epistemic neighbor of the frozen Task 0 state; business world unchanged."""
from copy import deepcopy
from baseline_engine import Case as KnownCase, SAT, UNMET, UNKNOWN, NA


class Case(KnownCase):
    def remember_conditional(self, parsed, user_ref):
        if parsed.get('grant') is not True:
            return False
        iid = self.changed_item
        pid = self.core.item(iid)['product_id']
        vid = parsed['variant_id']
        variant = self.core.products[pid]['variants'].get(vid)
        if (not variant or parsed['size'] != '80%' or variant['options'].get('size') != parsed['size']
                or parsed.get('availability_required') is not True
                or not all(variant['options'].get(k) == value for k, value in self.goal['hard_options'].items())):
            raise ValueError('conditional permission has unsupported entity, size or condition')
        quote = parsed['source_quote']
        if not isinstance(quote, str) or not quote or quote not in self.history[user_ref]['content']:
            raise ValueError('conditional rule lacks exact source quotation')
        self.conditional_permission = {'item_id': iid, 'variant_id': vid, 'size': parsed['size'],
            'condition': {'product_id': pid, 'variant_id': vid, 'field': 'available', 'op': 'eq', 'value': True},
            'source': user_ref, 'source_quote': quote, 'sat': UNKNOWN}
        self.goal['conditional_permission'] = deepcopy(self.conditional_permission)
        self.core.put('conditional_rule:' + iid, deepcopy(self.conditional_permission), sources=[user_ref])
        return True

    def resolve_conditional(self, inventory_ref):
        rule = getattr(self, 'conditional_permission', None)
        if not rule:
            return
        pid, vid = rule['condition']['product_id'], rule['variant_id']
        stock = self.core.products[pid]['variants'][vid].get('available')
        rule['sat'] = SAT if stock is True else UNMET if stock is False else UNKNOWN
        rule['inventory_source'] = inventory_ref
        self.goal['conditional_permission'] = deepcopy(rule)
        if stock is True:
            self.core.put('conditional_trigger:' + self.changed_item, {'size': rule['size'], 'satisfied': True},
                ['conditional_rule:' + self.changed_item, 'catalog:' + pid], [rule['source'], inventory_ref])
            self.goal['alternative_permission'] = rule['size']
            self.goal['permission_source'] = rule['source']
            self.stage_change({'size': rule['size']}, rule['source'])
            self.core.records['requirement:' + self.changed_item]['depends_on'] = ['conditional_trigger:' + self.changed_item]

    def inventory_unknown(self):
        product = self.core.products[self.core.item(self.changed_item)['product_id']]
        relevant = [v for v in product['variants'].values() if all(
            str(v['options'].get(key, '')).casefold() == str(value).casefold()
            for key, value in self.goal['hard_options'].items())]
        return any(type(v.get('available')) is not bool for v in relevant)

    def stage_change(self, options, ref):
        core, iid = self.core, self.changed_item
        desired = {**core.requirements[iid], **options}
        product = core.products[core.item(iid)['product_id']]
        uncertain = any(type(v.get('available')) is not bool and all(
            str(v['options'].get(k, '')).casefold() == str(value).casefold() for k, value in desired.items())
                        for v in product['variants'].values())
        if not uncertain:
            return super().stage_change(options, ref)
        # Unknown availability is not an empty set of available matches.
        before = core.snapshot()
        delta = core.effective_changes([{'item_id': iid, 'set_options': options}])
        if not delta:
            return
        key = 'requirement:' + iid
        old = core.records[key]
        core.requirements[iid] = desired
        core.records[key] = {**deepcopy(old), 'value': desired, 'version': old['version'] + 1, 'sources': [ref]}
        direct = [k for k, r in core.records.items() if key in r['depends_on']]
        for node in direct:
            core.records[node]['status'] = 'stale'
        pending = core.snapshot()
        match = 'match:' + iid
        previous = deepcopy(core.records[match])
        core.put(match, None, previous['depends_on'], [ref], status='unknown')
        after = core.snapshot()
        affected = [k for k in before if before[k]['status'] == 'supported' and after[k]['status'] == 'stale']
        self.transitions.append({'source': ref, 'delta': delta, 'direct_pending': direct,
            'before': before, 'after_direct_marking': pending,
            'reviewed_match': {'item_id': iid, 'availability': 'unknown', 'matched_items': None},
            'match_content_changed': before[match]['value'] is not None,
            'propagated_pending': [k for k in affected if k not in direct], 'after': after})

    def conditions(self):
        conditions = super().conditions()
        if not self.inventory_unknown():
            if getattr(self, 'conditional_permission', None):
                conditions['conditional_permission_trigger'] = self.condition(
                    self.conditional_permission['sat'], ['g.conditional_permission', 'F.catalog'])
            return conditions  # Exact frozen known-state interface.
        conditions['alternative_inventory'] = self.condition(UNKNOWN, ['F.catalog'])
        conditions['inventory_query_needed'] = self.condition(SAT, ['F.catalog'])
        # Distinguish unknown eligible availability from proven absence.
        unknown_selection = False
        for iid in self.core.scope:
            product = self.core.products[self.core.item(iid)['product_id']]
            matches = [v for v in product['variants'].values() if all(
                str(v['options'].get(k, '')).casefold() == str(value).casefold()
                for k, value in self.core.requirements[iid].items())]
            if not any(v.get('available') is True for v in matches) and any(type(v.get('available')) is not bool for v in matches):
                unknown_selection = True
        if unknown_selection:
            conditions['selection_available'] = self.condition(UNKNOWN, ['g', 'F.catalog'])
        if getattr(self, 'conditional_permission', None):
            conditions['conditional_permission_trigger'] = self.condition(
                self.conditional_permission['sat'], ['g.conditional_permission', 'F.catalog'])
        return conditions

    def candidates(self):
        candidates = super().candidates()
        if not self.inventory_unknown():
            return candidates
        c = self.conditions()
        for candidate in candidates:
            if candidate['work_id'] in ('screen', 'prepare'):
                candidate['preconditions']['alternative_inventory'] = c['alternative_inventory']
                candidate['ready'] = False
        product_id = self.core.item(self.changed_item)['product_id']
        inventory = {'work_id': 'inventory', 'work_type': 'ACQUIRE', 'target': {'product_id': product_id},
            'evidence_refs': ['g', 'F.catalog'],
            'preconditions': {key: c[key] for key in ('identity', 'inventory_query_needed')},
            'expected_output': 'official inventory evidence and exact currently available hard-matching alternatives',
            'expected_effects': ['resolve unknown alternative availability', 'support evidence-grounded user clarification'],
            'completion_test': 'inventory_recorded', 'ready': True}
        return [inventory] + candidates

    def deterministic(self, instruction, tools):
        if instruction['z']['work_id'] != 'inventory':
            return super().deterministic(instruction, tools)
        self.validate_instruction(instruction)
        product_id = instruction['z']['target']['product_id']
        result = tools.get_product_details(product_id=product_id).model_dump(mode='json')
        source = len(self.history)
        self.core.observe('get_product_details', {'product_id': product_id}, result, source)
        self.resolve_conditional(source)
        self.core.review([self.changed_item], source)
        screen = next(w for w in self.candidates() if w['work_id'] == 'screen')
        derived = super().deterministic(self.instruction(screen), tools)
        return {'official_tool': 'get_product_details', 'arguments': {'product_id': product_id},
                'official_result': result, 'derived_available_options': derived, 'source': source}

    def completed(self, test):
        if test == 'inventory_recorded':
            return not self.inventory_unknown() and self.screen is not None
        return super().completed(test)
