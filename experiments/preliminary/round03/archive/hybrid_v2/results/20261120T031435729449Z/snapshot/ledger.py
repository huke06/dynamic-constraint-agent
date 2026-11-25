"""Retail exchange adapter: typed observations, rule-derived dependencies and money.

No task IDs, expected answer, natural-language keyword intent parser, or LLM graph.
The adapter consumes semantic deltas; selecting work remains the agent's responsibility.
"""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json


def packed(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=True)


def fingerprint(value):
    return hashlib.sha256(packed(value).encode()).hexdigest()[:20]


class Ledger:
    def __init__(self, history):
        self.history = deepcopy(history)
        self.records, self.products, self.product_refs = {}, {}, {}
        self.orders, self.users = {}, {}
        self.evidence = {str(i): deepcopy(m) for i, m in enumerate(history)}
        self.authenticated = None
        self.scope, self.requirements = [], {}
        self.old_confirmations, self.proposals = [], []
        self.events = []
        self.order_id = self.payment = None
        self.completed_writes = 0
        self.ingest_prefix(history)

    def put(self, key, value, dependencies=(), sources=(), status='supported'):
        previous = self.records.get(key)
        if previous and previous['value'] == value and previous['status'] == status:
            return []  # Repeated evidence does not churn provenance or versions.
        affected, queue = [], [key]
        while queue:
            parent = queue.pop(0)
            for child, record in self.records.items():
                if child != key and parent in record['depends_on'] and child not in affected:
                    record['status'] = 'stale'
                    affected.append(child)
                    queue.append(child)
        self.records[key] = {'value': deepcopy(value), 'version': (previous['version'] if previous else 0) + 1,
                             'status': status, 'depends_on': list(dependencies), 'sources': list(sources)}
        return affected

    def ingest_prefix(self, history):
        pending = {}
        for index, message in enumerate(history):
            if message.get('tool_calls'):
                for tc in message['tool_calls']:
                    pending[tc['id']] = tc['function']
            if message['role'] == 'tool':
                function = pending[message['tool_call_id']]
                self.observe(function['name'], json.loads(function['arguments']), json.loads(message['content']), index)

    def observe(self, name, arguments, result, ref):
        if isinstance(result, dict) and 'error' in result:
            return
        if name.startswith('find_user_id_'):
            self.authenticated = result
            self.put('identity', result, sources=[ref])
        elif name == 'get_user_details':
            self.users[result['user_id']] = deepcopy(result)
            self.put('profile:' + result['user_id'], result, ['identity'], [ref])
        elif name == 'get_order_details':
            self.orders[result['order_id']] = deepcopy(result)
            self.put('order:' + result['order_id'], result, ['identity'], [ref])
        elif name == 'get_product_details':
            pid = result['product_id']
            self.products[pid], self.product_refs[pid] = deepcopy(result), ref
            self.put('catalog:' + pid, result, sources=[ref])
        elif name == 'exchange_delivered_order_items':
            self.orders[result['order_id']] = deepcopy(result)
            self.put('order:' + result['order_id'], result, ['identity'], [ref])
            self.completed_writes += 1
            self.put('execution', {'order_id': result['order_id'], 'status': result['status']}, sources=[ref])

    def item(self, iid):
        order = self.orders[self.order_id]
        return next(item for item in order['items'] if item['item_id'] == iid)

    def seed(self, semantics, proposal_ref, approval_ref):
        args = semantics['old_plan']
        self.order_id, self.payment = args['order_id'], args['payment_method_id']
        self.scope = list(args['item_ids'])
        if len(set(self.scope)) != len(self.scope) or not self.scope:
            raise ValueError('adapter requires distinct items and nonempty exchange scope')
        if len(self.scope) != len(args['new_item_ids']):
            raise ValueError('invalid original pair lengths')
        for iid, nid in zip(self.scope, args['new_item_ids']):
            item = self.item(iid)
            variant = self.products[item['product_id']]['variants'][nid]
            self.requirements[iid] = deepcopy(variant['options'])
            self.put('requirement:' + iid, variant['options'], sources=[proposal_ref, approval_ref])
        self.put('scope', self.scope, sources=[proposal_ref, approval_ref])
        self.put('payment', self.payment, ['profile:' + self.authenticated], [proposal_ref, approval_ref])
        quote = self.compile(args)
        if semantics['old_confirmed'] is not True or Decimal(str(semantics['old_difference'])) != Decimal(str(quote['difference'])):
            raise ValueError('original semantic approval/amount unsupported by observed prices')
        self.prepare(args, proposal_ref)
        self.confirm(args, semantics['old_difference'], approval_ref, proposal_ref)

    def effective_changes(self, changes):
        effective = []
        for change in changes:
            iid = change['item_id']
            if iid not in self.scope or not isinstance(change['set_options'], dict) or not change['set_options']:
                raise ValueError('unknown item or empty semantic option delta')
            item = self.item(iid)
            catalog = self.products.get(item['product_id'])
            known_keys = set().union(*(set(v['options']) for v in catalog['variants'].values())) if catalog else set(item['options'])
            if not set(change['set_options']) <= known_keys:
                raise ValueError('unknown option field')
            if any(not isinstance(v, str) for v in change['set_options'].values()):
                raise ValueError('semantic option values must be strings')
            difference = {k: v for k, v in change['set_options'].items()
                          if str(self.requirements[iid].get(k, '')).strip().casefold() != v.strip().casefold()}
            if difference:
                effective.append({'item_id': iid, 'set_options': difference})
        return effective

    def apply_changes(self, changes, source):
        before = self.snapshot()
        affected = []
        effective = self.effective_changes(changes)
        for change in effective:
            iid = change['item_id']
            if iid not in self.scope or not isinstance(change['set_options'], dict) or not change['set_options']:
                raise ValueError('unknown item or empty semantic option delta')
            item = self.item(iid)
            catalog = self.products.get(item['product_id'])
            known_keys = set().union(*(set(v['options']) for v in catalog['variants'].values())) if catalog else set(item['options'])
            if not set(change['set_options']) <= known_keys:
                raise ValueError('unknown option field')
            value = {**self.requirements[iid], **change['set_options']}
            affected += self.put('requirement:' + iid, value, sources=[source])
            self.requirements[iid] = value
        event = {'kind': 'semantic_change', 'source': source, 'proposed_changes': deepcopy(changes), 'changes': effective,
                 'affected': sorted(set(affected)), 'before': before, 'after': self.snapshot()}
        self.events.append(event)
        return event

    def review(self, item_ids, source):
        results = []
        for iid in item_ids:
            if iid not in self.scope:
                raise ValueError('item outside current exchange scope')
            item = self.item(iid)
            pid = item['product_id']
            if pid not in self.products:
                results.append({'item_id': iid, 'missing': 'product details', 'product_id': pid})
                continue
            variants = self.products[pid]['variants'].values()
            matches = [deepcopy(v) for v in variants if v['available'] and all(
                str(v['options'].get(k, '')).casefold() == str(value).casefold()
                for k, value in self.requirements[iid].items())]
            dependencies = ['requirement:' + iid, 'catalog:' + pid, 'order:' + self.order_id]
            self.put('match:' + iid, [v['item_id'] for v in matches], dependencies, [self.product_refs[pid], source])
            results.append({'item_id': iid, 'requirements': self.requirements[iid], 'candidates': matches,
                            'evidence': [self.product_refs[pid]], 'old_price': item['price']})
        return results

    def compile(self, arguments):
        required = {'order_id', 'item_ids', 'new_item_ids', 'payment_method_id'}
        if set(arguments) != required:
            raise ValueError('write schema must contain exactly the required exchange arguments')
        if arguments['order_id'] != self.order_id:
            raise ValueError('order outside authorized scope')
        order = self.orders[self.order_id]
        if order['user_id'] != self.authenticated or order['status'] != 'delivered':
            raise ValueError('identity/ownership/order stage prerequisite failed')
        if self.completed_writes:
            raise ValueError('order already written')
        if sorted(arguments['item_ids']) != sorted(self.scope) or len(arguments['new_item_ids']) != len(self.scope):
            raise ValueError('collect every authorized item into one request')
        if arguments['payment_method_id'] != self.payment or self.payment not in self.users[self.authenticated]['payment_methods']:
            raise ValueError('payment not authorized or absent from observed user profile')
        rows, total = [], Decimal('0')
        for iid, nid in zip(arguments['item_ids'], arguments['new_item_ids']):
            item = self.item(iid)
            pid = item['product_id']
            if pid not in self.products:
                raise ValueError('product evidence missing')
            variant = self.products[pid]['variants'].get(nid)
            if not variant or not variant['available']:
                raise ValueError('new variant unavailable or different product')
            if not all(str(variant['options'].get(k, '')).casefold() == str(v).casefold()
                       for k, v in self.requirements[iid].items()):
                raise ValueError('variant conflicts with current normalized user requirements')
            delta = (Decimal(str(variant['price'])) - Decimal(str(item['price']))).quantize(Decimal('.01'))
            total += delta
            rows.append({'item_id': iid, 'new_item_id': nid, 'options': deepcopy(variant['options']),
                         'new_price': variant['price'], 'old_price': item['price'], 'difference': float(delta),
                         'sources': [self.product_refs[pid]]})
        method = self.users[self.authenticated]['payment_methods'][self.payment]
        if method['source'] == 'gift_card' and Decimal(str(method['balance'])) < total:
            raise ValueError('insufficient observed gift card balance')
        rows.sort(key=lambda row: row['item_id'])
        canonical = {'order_id': self.order_id, 'payment_method_id': self.payment,
                     'pairs': [(r['item_id'], r['new_item_id']) for r in rows], 'difference': float(total)}
        return {'rows': rows, 'difference': float(total), 'fingerprint': fingerprint(canonical), **canonical}

    def prepare(self, arguments, source):
        plan = self.compile(arguments)
        for row in plan['rows']:
            iid = row['item_id']
            self.review([iid], source)
            self.put('delta:' + iid, row['difference'], ['match:' + iid, 'catalog:' + self.item(iid)['product_id']], row['sources'])
        self.put('total', plan['difference'], ['delta:' + iid for iid in self.scope], [source])
        self.proposals.append({'arguments': deepcopy(arguments), 'plan': plan, 'source': source})
        return plan

    def item_signature(self, row):
        return fingerprint({k: row[k] for k in ('item_id', 'new_item_id', 'difference')})

    def confirm(self, arguments, stated_difference, user_ref, assistant_ref):
        plan = self.prepare(arguments, assistant_ref)
        if Decimal(str(stated_difference)) != Decimal(str(plan['difference'])):
            raise ValueError('communicated amount does not match observed exact calculation')
        for row in plan['rows']:
            iid = row['item_id']
            self.put('confirmation:' + iid, self.item_signature(row), ['requirement:' + iid, 'match:' + iid, 'delta:' + iid],
                     [assistant_ref, user_ref])
        self.put('authorization', plan['fingerprint'], ['scope', 'payment', 'total'] + ['confirmation:' + iid for iid in self.scope],
                 [assistant_ref, user_ref])
        self.old_confirmations.append({'fingerprint': plan['fingerprint'], 'user_ref': user_ref, 'assistant_ref': assistant_ref,
                                       'arguments': deepcopy(arguments), 'difference': plan['difference']})
        return {'accepted': True, 'fingerprint': plan['fingerprint'], 'sources': [assistant_ref, user_ref]}

    def gate(self, arguments):
        plan = self.compile(arguments)
        record = self.records.get('authorization')
        if not record or record['status'] != 'supported' or record['value'] != plan['fingerprint']:
            raise ValueError('no explicit confirmation bound to this exact current plan and amount')
        return {'allowed': True, 'fingerprint': plan['fingerprint'], 'confirmation_sources': record['sources']}

    def snapshot(self):
        return deepcopy(self.records)

    def view(self):
        order = self.orders.get(self.order_id, {})
        items = []
        for iid in self.scope:
            item = self.item(iid)
            record = self.records.get('match:' + iid, {})
            items.append({'item_id': iid, 'product_id': item['product_id'], 'name': item['name'], 'old_price': item['price'],
                          'requirements': self.requirements[iid], 'match_status': record.get('status', 'unknown'),
                          'cached_candidates': record.get('value') if record.get('status') == 'supported' else None,
                          'confirmation_status': self.records.get('confirmation:' + iid, {}).get('status', 'unknown'),
                          'catalog_cached': item['product_id'] in self.products})
        latest = deepcopy(self.proposals[-1]) if self.proposals else None
        if latest:
            try:
                self.compile(latest['arguments'])
                latest['current_requirements_match'] = True
            except ValueError:
                latest['current_requirements_match'] = False
        return {'identity': self.authenticated, 'order_id': self.order_id, 'status': order.get('status'),
                'scope': items, 'payment_method_id': self.payment,
                'total': deepcopy(self.records.get('total')), 'authorization': deepcopy(self.records.get('authorization')),
                'records_available': list(self.records), 'source_messages_available': list(self.evidence),
                'latest_prepared_proposal': latest}

    def read_evidence(self, references):
        output = {}
        for ref in references:
            if ref in self.records:
                output[ref] = deepcopy(self.records[ref])
            elif str(ref) in self.evidence:
                output[ref] = deepcopy(self.evidence[str(ref)])
            else:
                raise ValueError('unknown evidence reference: ' + str(ref))
        return output
