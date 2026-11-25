"""Offline contract tests; only this test/evaluation module reads private targets."""
from copy import deepcopy
from ledger import Ledger, packed


def offline(case):
    checks = []
    old = deepcopy(case['private_evaluation']['old_arguments'])
    latest = deepcopy(case['private_evaluation']['expected_arguments'])
    history = case['shared_history']
    semantic_fixture = {'old_plan': old, 'old_difference': -16.63, 'old_confirmed': True,
                        'changes': [{'item_id': old['item_ids'][0], 'set_options': {
                            'switch type': 'tactile', 'backlight': 'white', 'size': 'full size'}}]}

    def seeded():
        ledger = Ledger(history)
        ledger.seed(semantic_fixture, len(history) - 2, len(history) - 1)
        return ledger

    def rejected(fn):
        try:
            fn()
        except (ValueError, KeyError):
            return
        raise AssertionError('invalid operation accepted')

    ledger = seeded()
    assert ledger.gate(old)['allowed']
    assert ledger.compile(old)['difference'] == -16.63
    checks.append('typed official-tool ingestion and original exact authorization')
    before = ledger.snapshot()
    event = ledger.apply_changes(semantic_fixture['changes'], len(history))
    iid, untouched = old['item_ids']
    expected = {'match:' + iid, 'delta:' + iid, 'confirmation:' + iid, 'total', 'authorization'}
    assert set(event['affected']) == expected
    for key in ('identity', 'scope', 'payment', 'order:' + old['order_id'], 'requirement:' + untouched,
                'match:' + untouched, 'delta:' + untouched, 'confirmation:' + untouched):
        assert ledger.records[key] == before[key]
    checks.append('selective dependency invalidation retains unrelated values, versions and provenance')
    rejected(lambda: ledger.gate(old))
    rejected(lambda: ledger.gate(latest))
    assert len(ledger.old_confirmations) == 1
    checks.append('old approval remains historical; neither old nor changed write bypasses re-confirmation')
    assert ledger.view()['latest_prepared_proposal']['current_requirements_match'] is False
    checks.append('compact context labels historical proposal as incompatible')
    review = ledger.review([iid], 17)
    assert [v['item_id'] for v in review[0]['candidates']] == [latest['new_item_ids'][0]]
    assert review[0]['evidence'] and ledger.records['match:' + iid]['depends_on']
    checks.append('program exact filtering uses cached evidence, without selecting a workflow or model call')
    proposal = ledger.prepare(latest, 19)
    assert proposal['difference'] == -59.68
    assert all(row['sources'] for row in proposal['rows'])
    rejected(lambda: ledger.gate(latest))
    checks.append('Decimal combined refund calculated correctly; prepared proposal is not approval')
    rejected(lambda: ledger.confirm(latest, -16.63, 22, 21))
    rejected(lambda: ledger.gate(latest))
    checks.append('wrong communicated amount cannot acquire authorization')
    ledger.confirm(latest, -59.68, 22, 21)
    assert ledger.gate(latest)['allowed']
    assert ledger.records['confirmation:' + untouched] == before['confirmation:' + untouched]
    assert ledger.old_confirmations[0]['arguments'] == old
    checks.append('new plan confirmation accepted while unchanged item confirmation retains original evidence')
    reversed_args = deepcopy(latest)
    reversed_args['item_ids'].reverse()
    reversed_args['new_item_ids'].reverse()
    assert ledger.gate(reversed_args)['allowed']
    broken = deepcopy(latest)
    broken['new_item_ids'].reverse()
    rejected(lambda: ledger.gate(broken))
    partial = deepcopy(latest)
    partial['item_ids'] = partial['item_ids'][:1]
    partial['new_item_ids'] = partial['new_item_ids'][:1]
    rejected(lambda: ledger.gate(partial))
    checks.append('canonical pair reordering allowed; wrong product mapping and partial once-only write rejected')
    assert ledger.read_evidence(['8'])['8'] == history[8]
    assert 'catalog:' + ledger.item(iid)['product_id'] in ledger.records
    checks.append('unabridged original evidence remains available on demand')
    stable = ledger.snapshot()
    ledger.apply_changes(semantic_fixture['changes'], 23)
    assert ledger.snapshot() == stable
    checks.append('identical delta is idempotent and does not churn versions')
    restatement = [{'item_id': iid, 'set_options': deepcopy(ledger.requirements[iid])},
                   {'item_id': untouched, 'set_options': deepcopy(ledger.requirements[untouched])}]
    assert ledger.effective_changes(restatement) == []
    assert ledger.effective_changes([{'item_id': iid, 'set_options': {'size': 'FULL SIZE'}}]) == []
    assert ledger.effective_changes([{'item_id': iid, 'set_options': {'size': '80%'}}])
    checks.append('reaffirming current options is not a new change; a genuine option change remains effective')
    altered = seeded()
    altered.apply_changes(semantic_fixture['changes'], 15)
    pid = altered.item(iid)['product_id']
    new_catalog = deepcopy(altered.products[pid])
    new_catalog['variants'][latest['new_item_ids'][0]]['available'] = False
    altered.observe('get_product_details', {'product_id': pid}, new_catalog, 25)
    assert altered.review([iid], 26)[0]['candidates'] == []
    rejected(lambda: altered.prepare(latest, 27))
    checks.append('availability changes follow observations, not a hardcoded answer list')
    other = seeded()
    rejected(lambda: other.apply_changes([{'item_id': 'not-in-order', 'set_options': {'size': 'x'}}], 15))
    rejected(lambda: other.apply_changes([{'item_id': iid, 'set_options': {'invented_field': 'x'}}], 15))
    checks.append('semantic output cannot invent an entity or option field')
    other.completed_writes = 1
    rejected(lambda: other.gate(old))
    checks.append('common program guard rejects repeat writes')
    assert 'private_evaluation' not in packed(ledger.view())
    assert '272.33' in packed(review)  # observed price, not a private target
    checks.append('packed current context contains no evaluation object')
    return {'status': 'passed', 'checks': checks,
            'note': 'Test-only semantic fixture is not used in online inference; actor receives no expected IDs or workflow.'}
