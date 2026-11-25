"""No-inference acceptance, including exact replay of the frozen known anchor."""
from copy import deepcopy
import json
from engine import Case, SAT, UNKNOWN
from exchange_core import packed


class Replay:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0

    def ask(self, branch, category, stage, messages, max_tokens=1400, case=None):
        row = self.rows[self.index]
        self.index += 1
        assert (row['branch'], row['category'], row['stage']) == (branch, category, stage)
        assert row['messages'] == messages, (branch, stage, 'known-state policy changed')
        assert row['max_tokens'] == max_tokens
        if case and category == 'agent':
            case.remaining_budget['agent_calls'] -= 1
            case.remaining_budget['agent_tokens'] -= row['response']['usage']['total_tokens']
        content = row['response']['choices'][0]['message']['content']
        return content if stage == 'worker' else json.loads(content)


def stock_values(value, target):
    values = []
    if isinstance(value, str) and value[:1] in ('{', '['):
        try:
            return stock_values(json.loads(value), target)
        except (ValueError, TypeError):
            return []
    if isinstance(value, dict):
        if value.get('item_id') == target and 'available' in value:
            values.append(value['available'])
        if target in value and isinstance(value[target], dict) and 'available' in value[target]:
            values.append(value[target]['available'])
        for child in value.values():
            values.extend(stock_values(child, target))
    elif isinstance(value, list):
        for child in value:
            values.extend(stock_values(child, target))
    return values


def normalize(value):
    return json.loads(packed(value))


def offline(fixture, adjacent, intervention, semantics, database, output):
    import run
    base = run.base
    tests = []
    change = intervention['changes'][0]
    target, pid = change['variant_id'], change['product_id']
    known, unknown = Case(fixture, semantics), Case(adjacent, semantics)
    restored = deepcopy(adjacent)
    index = change['message_index']
    content = json.loads(restored['shared_history'][index]['content'])
    content['variants'][target]['available'] = True
    # Preserve the exact old string representation; check semantic identity first.
    assert content == json.loads(fixture['shared_history'][index]['content'])
    restored['shared_history'][index]['content'] = fixture['shared_history'][index]['content']
    assert restored == fixture
    assert known.goal == unknown.goal and known.user_state == unknown.user_state
    assert known.event_state == unknown.event_state and known.remaining_budget == unknown.remaining_budget
    assert known.core.scope == unknown.core.scope and known.core.payment == unknown.core.payment
    tests.append('exactly one primitive observation changed; goals, event, user state, scope, payment and budget unchanged')
    assert database['products'][pid]['variants'][target]['available'] is True
    assert base.hash_value(database) == base.hash_value(base.read(run.KNOWN / 'initial_database.json'))
    tests.append('actual stock/world and official rules remain unchanged')
    for public in (unknown.state(), unknown.compact(), unknown.core.snapshot(), unknown.history):
        statuses = stock_values(public, target)
        assert statuses and all(value is None for value in statuses)
    assert all(value is True for value in stock_values(known.state(), target))
    tests.append('masked positive stock absent from current facts, historical tool response and all derived caches')
    ready = {w['work_id'] for w in unknown.candidates() if w['ready']}
    assert ready == {'inventory', 'clarify'}
    assert unknown.conditions()['alternative_inventory']['sat'] == UNKNOWN
    assert not next(w for w in unknown.candidates() if w['work_id'] == 'screen')['ready']
    tests.append('unknown stock enables official acquisition; cached screening cannot treat unknown as absent')
    # User can grant conditional permission before any stock query; this must not grant write permission.
    conditional = deepcopy(unknown)
    conditional.apply_user({'permission': 'allow_80', 'scope': 'both', 'approved': False}, 16, 17)
    assert conditional.conditions()['selection_available']['sat'] == UNKNOWN
    assert conditional.core.records['match:' + conditional.changed_item]['value'] is None
    assert not next(w for w in conditional.candidates() if w['work_id'] == 'prepare')['ready']
    assert not next(w for w in conditional.candidates() if w['work_id'] == 'submit')['ready']
    tests.append('conditional size acceptance does not imply stock or approval; unknown matching remains unknown')
    clone = deepcopy(unknown)
    tools = base.RetailTools(base.RetailDB.model_validate(deepcopy(database)))
    inventory = next(w for w in clone.candidates() if w['work_id'] == 'inventory')
    class NoModel:
        def ask(self, *args, **kwargs):
            raise AssertionError('official stock acquisition and exact filtering must not call an LLM')
    event = run.work(clone, clone.instruction(inventory), NoModel(), 'offline', tools, '')
    assert event['result']['official_result'] == tools.get_product_details(product_id=pid).model_dump(mode='json')
    assert clone.core.products[pid]['variants'][target]['available'] is True and clone.completed('inventory_recorded')
    assert unknown.core.products[pid]['variants'][target]['available'] is None
    assert clone.goal['alternative_permission'] == 'unknown'
    assert tools.db.model_dump(mode='json') == database
    tests.append('actual official read restores evidence, without changing stock, user permission or sibling branch')
    assert clone.screen['available_hard_matches'] and clone.screen['preferred_available'] is False
    assert {w['work_id'] for w in clone.candidates() if w['ready']} == {'clarify'}
    tests.append('query completes evidence work; customer acceptance still unresolved, no forced rescreen')
    conditional_tools = base.RetailTools(base.RetailDB.model_validate(deepcopy(database)))
    inventory = next(w for w in conditional.candidates() if w['work_id'] == 'inventory')
    run.work(conditional, conditional.instruction(inventory), NoModel(), 'offline', conditional_tools, '')
    assert conditional.conditions()['selection_available']['sat'] == SAT
    assert next(w for w in conditional.candidates() if w['work_id'] == 'prepare')['ready']
    tests.append('prior conditional permission survives query; no script forces repeated clarification')
    snapshots = [deepcopy(unknown).snapshot(deepcopy(database), base.USER_POLICY) for _ in range(2)]
    assert snapshots[0] == snapshots[1]
    assert 'hidden_fallback' not in packed(unknown.compact())
    tests.append('unknown-state fork includes equal complete state, user, database, trigger and budget; no private-goal leak')
    # Strong compatibility check: all 22 original model requests must replay exactly under this engine.
    rows = [json.loads(line) for line in (run.KNOWN / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    replay = Replay(rows)
    initial_input = [{'role': 'system', 'content': base.SEMANTIC_CHANGE},
                     {'role': 'user', 'content': packed({'old_plan': fixture['approved_prefix']['old_plan'],
                         'new_user_message': base.CHANGE, 'order_items': database['orders'][fixture['order_id']]['items']})}]
    assert replay.ask('shared_prefix', 'agent', 'initial_semantics', initial_input, max_tokens=700) == semantics
    replay_output = output / 'known_anchor_replay'
    replay_output.mkdir()
    for wid in ('screen', 'clarify'):
        first = next(w for w in known.candidates() if w['work_id'] == wid)
        result = base.rollout(wid + '_first', known, database, first, replay, replay_output,
                              (base.DATA / 'policy.md').read_text(encoding='utf-8'))
        assert normalize(result) == base.read(run.KNOWN / (wid + '_first_result.json'))
    assert replay.index == len(rows)
    tests.append('all original known-state LLM requests and official effects replay identically; no new samples')
    return {'status': 'passed', 'n_checks': len(tests), 'checks': tests,
            'known_anchor_requests_replayed_without_api': replay.index,
            'limitation': 'One controlled knowledge-state neighbor; copied observation view is explicitly synthetic, not an actual historical tool response.'}
