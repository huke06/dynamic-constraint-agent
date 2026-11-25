"""Offline acceptance for the mathematical contracts; no model inference."""
from copy import deepcopy
from engine import Case, SAT, UNMET, UNKNOWN, NA
from exchange_core import packed


def semantic_fixture(fixture):
    # Test-only interpretation. Online run obtains it from the actual user message.
    return {'item_id': fixture['approved_prefix']['old_plan']['item_ids'][0],
            'hard_options': {'switch type': 'clicky', 'backlight': 'RGB'},
            'preferred_options': {'size': 'full size'}, 'alternative_permission': 'unknown'}


def offline(fixture):
    from run import RetailDB, RetailTools, DATA, USER_POLICY, hash_value, score
    tests = []
    case = Case(fixture, semantic_fixture(fixture))
    state = case.state()
    assert set(state) == {'g', 'F', 'C', 'P', 'H', 'D'}
    assert all(c['sat'] in (SAT, UNMET, UNKNOWN, NA) and c['validity'] in ('fresh', 'pending_review') for c in state['C'].values())
    assert state['C']['alternative_permission']['sat'] == UNKNOWN
    assert state['C']['old_keyboard_match']['sat'] == UNMET
    assert state['C']['authorization_current']['validity'] == 'pending_review'
    tests.append('six-part state; four-valued conditions distinct from evidence validity')
    change = case.transitions[0]
    assert change['match_content_changed'] and change['direct_pending'] and change['propagated_pending']
    untouched = [iid for iid in case.core.scope if iid != case.changed_item][0]
    for key in ('identity', 'payment', 'scope', 'match:' + untouched, 'delta:' + untouched, 'confirmation:' + untouched):
        assert change['before'][key] == change['after'][key]
    tests.append('mark direct dependents, review changed match, propagate; unrelated provenance preserved')
    candidates = case.candidates()
    ready = [w for w in candidates if w['ready']]
    assert {w['work_id'] for w in ready} == {'screen', 'clarify'}
    assert all(all(c['sat'] == SAT for c in w['preconditions'].values()) for w in ready)
    assert not next(w for w in candidates if w['work_id'] == 'submit')['ready']
    assert all('H.screen' not in w['evidence_refs'] and 'H.plan' not in w['evidence_refs'] for w in ready)
    tests.append('candidate-specific Pre and W_ready permit clarification without submission approval')
    for candidate in ready:
        case.validate_instruction(case.instruction(candidate))
    broken = case.instruction(ready[0])
    broken['e'] = 'invented completion'
    try:
        case.validate_instruction(broken)
    except ValueError:
        tests.append('u=(a,z,K,e) contract rejects invented completion condition')
    else:
        raise AssertionError('invalid instruction accepted')
    database = RetailDB.load(DATA / 'db.json').model_dump(mode='json')
    snapshot = case.snapshot(database, USER_POLICY)
    branches = [deepcopy(case), deepcopy(case)]
    assert hash_value(branches[0].snapshot(deepcopy(database), USER_POLICY)) == hash_value(snapshot)
    assert hash_value(branches[1].snapshot(deepcopy(database), USER_POLICY)) == hash_value(snapshot)
    branches[0].user_state['turns'] += 1
    branches[0].remaining_budget['agent_calls'] -= 1
    branches[0].event_state['change_injected'] = False
    assert hash_value(branches[1].snapshot(database, USER_POLICY)) == hash_value(snapshot)
    assert hash_value(case.snapshot(database, USER_POLICY)) == hash_value(snapshot)
    tests.append('database, state, user, event, random state and budget cloned without cross-branch leakage')
    tools_a = RetailTools(RetailDB.model_validate(deepcopy(database)))
    tools_b = RetailTools(RetailDB.model_validate(deepcopy(database)))
    screen = next(w for w in case.candidates() if w['work_id'] == 'screen')
    result = case.deterministic(case.instruction(screen), tools_a)
    assert result['available_hard_matches'] and result['preferred_available'] is False
    assert all(v['options']['backlight'] == 'RGB' and v['options']['switch type'] == 'clicky' for v in result['available_hard_matches'])
    assert case.goal['alternative_permission'] == 'unknown'
    assert not next(w for w in case.candidates() if w['work_id'] == 'screen')['ready']
    tests.append('deterministic screening records available alternatives but does not grant user permission or repeat completed work')
    try:
        case.core.gate(fixture['approved_prefix']['old_plan'])
    except ValueError:
        tests.append('old approval cannot authorize a now-disallowed keyboard')
    else:
        raise AssertionError('old invalid plan authorized')
    case.history.append({'role': 'assistant', 'content': 'Test-only alternative question'})
    case.history.append({'role': 'user', 'content': 'Test-only permission'})
    case.apply_user({'permission': 'allow_80', 'scope': 'both', 'approved': False}, len(case.history) - 2, len(case.history) - 1)
    assert case.conditions()['alternative_permission']['sat'] == SAT
    assert case.conditions()['authorization_current']['sat'] == UNMET
    tests.append('size permission does not become transaction confirmation')
    args = {'order_id': case.core.order_id, 'item_ids': list(case.core.scope), 'new_item_ids': [], 'payment_method_id': case.core.payment}
    for iid in args['item_ids']:
        item = case.core.item(iid)
        variants = case.core.products[item['product_id']]['variants'].values()
        matches = [v['item_id'] for v in variants if v['available'] and all(v['options'].get(k) == value for k, value in case.core.requirements[iid].items())]
        assert len(matches) == 1
        args['new_item_ids'].append(matches[0])
    prepare = next(w for w in case.candidates() if w['work_id'] == 'prepare')
    instruction = case.instruction(prepare, {'arguments': args})
    case.deterministic(instruction, tools_a)
    assert case.plan['quote']['difference'] == -48.31
    assert not next(w for w in case.candidates() if w['work_id'] == 'submit')['ready']
    tests.append('program price computation and plan artifact do not substitute for fresh confirmation')
    case.apply_user({'permission': 'unknown', 'scope': 'unchanged', 'approved': True, 'arguments': args, 'stated_difference': -48.31},
                    len(case.history) - 2, len(case.history) - 1)
    submit = next(w for w in case.candidates() if w['work_id'] == 'submit')
    case.deterministic(case.instruction(submit, {'arguments': args}), tools_a)
    assert score(case, tools_a)['business_request_correct']
    assert tools_b.db.orders[case.core.order_id].status == 'delivered'
    assert tools_a.db.orders[case.core.order_id].status == 'exchange requested'
    tests.append('shared executor submits actual official write; other branch database remains unchanged')
    assert case.completed('official_write_verified')
    assert not case.conditions()['not_written']['sat'] == SAT
    tests.append('completion is checked against effects; repeat write prerequisite fails')
    fresh = Case(fixture, semantic_fixture(fixture))
    fresh.apply_user({'permission': 'reject_smaller', 'scope': 'thermostat_only', 'approved': False}, 16, 17)
    assert fresh.core.scope == [untouched] and fresh.goal['scope'] == [untouched]
    assert fresh.core.records['confirmation:' + untouched] == fresh.transitions[0]['before']['confirmation:' + untouched]
    assert fresh.conditions()['authorization_current']['sat'] == UNMET
    tests.append('authorized scope change differs from silently omitting an item; prior unchanged evidence retained')
    visible = fresh.compact()
    assert 'hidden_fallback' not in packed(visible) and 'user_private' not in packed(visible)
    assert 'expected_difference' not in packed(visible)
    tests.append('hidden user policy and evaluation targets absent from controller/worker context')
    return {'status': 'passed', 'checks': tests, 'n_checks': len(tests),
            'limitation': 'Tests validate implementation contracts; not independent human annotations or model outcome evidence.'}
