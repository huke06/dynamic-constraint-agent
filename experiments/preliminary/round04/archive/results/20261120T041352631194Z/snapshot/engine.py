"""State, candidate contracts and fixed executor for one retail mechanism pilot."""
from copy import deepcopy
from decimal import Decimal
from exchange_core import Ledger, packed, fingerprint

SAT, UNMET, UNKNOWN, NA = '满足', '未满足', '未知', '不适用'


class Case:
    def __init__(self, fixture, semantic_change):
        self.core = Ledger(fixture['shared_history'])
        seed = fixture['approved_prefix']
        size = len(fixture['shared_history'])
        self.core.seed(seed, size - 2, size - 1)
        self.history = deepcopy(fixture['shared_history']) + [fixture['change_message']]
        self.core.evidence[str(size)] = deepcopy(fixture['change_message'])
        self.changed_item = semantic_change['item_id']
        if self.changed_item not in self.core.scope:
            raise ValueError('semantic change refers to unknown item')
        self.goal = {'order': self.core.order_id, 'scope': list(self.core.scope),
                     'hard_options': deepcopy(semantic_change['hard_options']),
                     'preferred_options': deepcopy(semantic_change['preferred_options']),
                     'alternative_permission': 'unknown', 'permission_source': None,
                     'payment': self.core.payment, 'change_source': size}
        self.screen = None
        self.plan = None
        self.confirmations = []
        self.writes = []
        self.transitions = []
        self.work = []
        self.steps = 0
        self.event_state = {'change_injected': True, 'further_external_events': 0}
        self.user_state = {'turns': 0, 'allowed_smaller': False, 'confirmed': False}
        self.rng_state = {'seed': 71, 'position': 0}
        self.remaining_budget = {'agent_calls': 24, 'agent_tokens': 60000, 'work_steps': 9}
        self.stage_change(semantic_change['hard_options'], size)

    def stage_change(self, options, ref):
        core, iid = self.core, self.changed_item
        before = core.snapshot()
        delta = core.effective_changes([{'item_id': iid, 'set_options': options}])
        if not delta:
            return
        key = 'requirement:' + iid
        old = core.records[key]
        value = {**core.requirements[iid], **delta[0]['set_options']}
        core.requirements[iid] = value
        core.records[key] = {**deepcopy(old), 'value': value, 'version': old['version'] + 1, 'sources': [ref]}
        direct = [k for k, r in core.records.items() if key in r['depends_on']]
        for node in direct:
            core.records[node]['status'] = 'stale'
        direct_pending = core.snapshot()
        # Recheck a deterministic matching conclusion, THEN propagate actual change.
        old_match = deepcopy(before.get('match:' + iid))
        reviewed = core.review([iid], ref)
        after = core.snapshot()
        affected = [k for k in before if before[k]['status'] == 'supported' and after[k]['status'] == 'stale']
        self.transitions.append({'source': ref, 'delta': delta, 'direct_pending': direct,
                                 'before': before, 'after_direct_marking': direct_pending,
                                 'reviewed_match': reviewed, 'match_content_changed': old_match['value'] != after['match:' + iid]['value'],
                                 'propagated_pending': [k for k in affected if k not in direct], 'after': after})

    def condition(self, value, refs, validity='fresh'):
        return {'sat': value, 'evidence_refs': refs, 'validity': validity}

    def conditions(self):
        core = self.core
        allowed = self.goal['alternative_permission'] != 'unknown'
        plan_valid = False
        if self.plan:
            try:
                core.compile(self.plan['arguments'])
                plan_valid = True
            except ValueError:
                pass
        authorization = core.records.get('authorization', {})
        auth = plan_valid and authorization.get('status') == 'supported' and authorization.get('value') == self.plan['quote']['fingerprint']
        selection = all(any(v['available'] and all(str(v['options'].get(k, '')).casefold() == str(value).casefold()
                        for k, value in core.requirements[iid].items())
                        for v in core.products[core.item(iid)['product_id']]['variants'].values()) for iid in core.scope)
        return {
            'identity': self.condition(SAT if core.authenticated else UNKNOWN, ['F.identity']),
            'catalog': self.condition(SAT if core.item(self.changed_item)['product_id'] in core.products else UNKNOWN, ['F.catalog']),
            'user_channel': self.condition(SAT, ['F.dialogue']),
            'alternative_permission': self.condition(SAT if allowed else UNKNOWN, ['g.alternative_permission']),
            'old_keyboard_match': self.condition(UNMET if self.changed_item in core.scope else NA, ['g.hard_options', 'H.original_approval']),
            'selection_available': self.condition(SAT if selection else UNMET, ['g', 'F.catalog']),
            'plan_current': self.condition(SAT if plan_valid else UNKNOWN, ['H.plan']),
            'authorization_current': self.condition(SAT if auth else UNMET, ['H.confirmations', 'H.plan'],
                                                     'pending_review' if authorization.get('status') == 'stale' else 'fresh'),
            'not_written': self.condition(SAT if not self.writes else UNMET, ['P.writes']),
            'screen_absent': self.condition(SAT if self.screen is None else UNMET, ['H.screen']),
        }

    def state(self):
        core = self.core
        return {'g': deepcopy(self.goal),
                'F': {'identity': core.authenticated, 'order': deepcopy(core.orders[core.order_id]),
                      'catalog': deepcopy(core.products), 'catalog_sources': deepcopy(core.product_refs),
                      'payment': deepcopy(core.users[core.authenticated]['payment_methods']),
                      'dialogue': deepcopy(self.history)},
                'C': self.conditions(),
                'P': {'completed_work': deepcopy(self.work), 'writes': deepcopy(self.writes), 'steps': self.steps},
                'H': {'original_approval': deepcopy(core.old_confirmations[0]), 'screen': deepcopy(self.screen),
                      'plan': deepcopy(self.plan), 'confirmations': deepcopy(self.confirmations),
                      'records': core.snapshot()},
                'D': {key: record['depends_on'] for key, record in core.records.items()}}

    def snapshot(self, database, user_policy):
        return {'state': self.state(), 'database': deepcopy(database), 'user_private': deepcopy(user_policy),
                'user_state': deepcopy(self.user_state), 'event_state': deepcopy(self.event_state),
                'rng_state': deepcopy(self.rng_state), 'remaining_budget': deepcopy(self.remaining_budget)}

    def candidates(self):
        c = self.conditions()
        entries = [
            ('screen', 'ACT', self.changed_item, ['identity', 'catalog', 'screen_absent'], ['g', 'F.catalog'],
             'available alternatives with exact prices', ['establish H.screen', 'support targeted user clarification'], 'screen_recorded'),
            ('clarify', 'ACQUIRE', self.changed_item, ['identity', 'user_channel'], ['g', 'F.catalog', 'H.screen'],
             'user permission or clarified information gap', ['resolve permission before selecting different size/scope'], 'permission_known'),
            ('prepare', 'ACT', list(self.core.scope), ['identity', 'catalog', 'alternative_permission', 'selection_available', 'not_written'], ['g', 'F.catalog', 'H.screen'],
             'checked exact plan and difference', ['establish proposal for explicit confirmation'], 'plan_recorded'),
            ('confirm', 'ACQUIRE', list(self.core.scope), ['plan_current', 'user_channel', 'not_written'], ['g', 'H.plan'],
             'explicit user authorization of current plan', ['establish C.authorization_current'], 'authorization_bound'),
            ('submit', 'ACT', self.core.order_id, ['identity', 'plan_current', 'authorization_current', 'not_written'], ['g', 'H.plan', 'C.authorization_current'],
             'official exchange request', ['reach business terminal state'], 'official_write_verified'),
        ]
        result = []
        for wid, kind, target, pre, refs, output, effects, completion in entries:
            refs = [ref for ref in refs if not (ref == 'H.screen' and self.screen is None)
                    and not (ref == 'H.plan' and self.plan is None)]
            if wid == 'clarify' and self.goal['alternative_permission'] != 'unknown':
                continue
            if wid == 'prepare' and self.plan:
                continue
            if wid == 'confirm' and c['authorization_current']['sat'] == SAT:
                continue
            checks = {key: c[key] for key in pre if c[key]['sat'] != NA}
            result.append({'work_id': wid, 'work_type': kind, 'target': target, 'evidence_refs': refs,
                           'preconditions': checks, 'expected_output': output, 'expected_effects': effects,
                           'completion_test': completion, 'ready': all(v['sat'] == SAT for v in checks.values())})
        return result

    def compact(self):
        core = self.core
        return {'g': deepcopy(self.goal), 'identity': core.authenticated, 'order_id': core.order_id,
                'items': [deepcopy(core.item(iid)) for iid in core.scope], 'payment_method_id': core.payment,
                'catalog': deepcopy(core.products), 'C': self.conditions(), 'P': deepcopy(self.work[-4:]),
                'H': {'screen': self.screen, 'plan': self.plan, 'original_approval': core.old_confirmations[0]},
                'recent_dialogue': [m for m in self.history if m['role'] in ('user', 'assistant') and m.get('content')][-4:]}

    def instruction(self, candidate, parameters=None):
        return {'a': candidate['work_type'], 'z': {'work_id': candidate['work_id'], 'target': candidate['target'],
                                               'parameters': parameters or {}},
                'K': candidate['evidence_refs'], 'e': candidate['completion_test']}

    def validate_instruction(self, instruction):
        candidate = next((w for w in self.candidates() if w['work_id'] == instruction['z']['work_id']), None)
        if not candidate or not candidate['ready']:
            raise ValueError('work absent or preconditions not satisfied')
        if instruction['a'] != candidate['work_type'] or instruction['z']['target'] != candidate['target'] or instruction['e'] != candidate['completion_test']:
            raise ValueError('instruction does not match work contract')
        if not instruction['K'] or not set(instruction['K']) <= set(candidate['evidence_refs']):
            raise ValueError('unavailable instruction evidence reference')
        return candidate

    def deterministic(self, instruction, tools):
        candidate = self.validate_instruction(instruction)
        op, core = candidate['work_id'], self.core
        if op == 'screen':
            item = core.item(self.changed_item)
            variants = core.products[item['product_id']]['variants'].values()
            hard = self.goal['hard_options']
            feasible = [deepcopy(v) for v in variants if v['available'] and all(
                str(v['options'].get(k, '')).casefold() == str(value).casefold() for k, value in hard.items())]
            self.screen = {'item_id': self.changed_item, 'available_hard_matches': feasible,
                           'preferred_options': self.goal['preferred_options'],
                           'preferred_available': any(all(v['options'].get(k) == value for k, value in self.goal['preferred_options'].items()) for v in feasible),
                           'source': core.product_refs[item['product_id']]}
            return deepcopy(self.screen)
        args = instruction['z']['parameters']['arguments']
        if op == 'prepare':
            quote = core.prepare(args, len(self.history))
            self.plan = {'arguments': deepcopy(args), 'quote': quote}
            return deepcopy(self.plan)
        if op == 'submit':
            gate = core.gate(args)
            result = tools.exchange_delivered_order_items(**args).model_dump(mode='json')
            core.observe('exchange_delivered_order_items', args, result, len(self.history))
            self.writes.append({'arguments': deepcopy(args), 'gate': gate, 'result': result})
            return result
        raise ValueError('this work requires semantic worker execution')

    def apply_user(self, parsed, assistant_ref, user_ref):
        permission = parsed['permission']
        if permission == 'allow_80':
            self.goal['alternative_permission'] = '80%'
            self.goal['permission_source'] = user_ref
            self.stage_change({'size': '80%'}, user_ref)
        elif permission == 'reject_smaller':
            self.goal['alternative_permission'] = 'rejected'
            self.goal['permission_source'] = user_ref
        elif permission != 'unknown':
            raise ValueError('unsupported semantic permission value')
        if parsed.get('scope') == 'thermostat_only':
            self.core.scope = [iid for iid in self.core.scope if iid != self.changed_item]
            self.goal['scope'] = list(self.core.scope)
            self.core.put('scope', self.core.scope, sources=[user_ref])
        if parsed.get('approved'):
            if not self.plan:
                raise ValueError('approval without current plan')
            result = self.core.confirm(parsed['arguments'], parsed['stated_difference'], user_ref, assistant_ref)
            if result['fingerprint'] != self.plan['quote']['fingerprint']:
                raise ValueError('confirmation refers to another plan')
            self.confirmations.append({'result': result, 'assistant_ref': assistant_ref, 'user_ref': user_ref})

    def completed(self, test):
        return {'screen_recorded': self.screen is not None,
                'permission_known': self.goal['alternative_permission'] != 'unknown',
                'plan_recorded': self.plan is not None,
                'authorization_bound': self.conditions()['authorization_current']['sat'] == SAT,
                'official_write_verified': bool(self.writes)}[test]
