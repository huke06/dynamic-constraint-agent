"""One official retail task, one user-message variant, two autonomous arms."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO = ROOT / 'tau2-official'
os.environ['TAU2_DATA_DIR'] = str(REPO / 'data')
os.environ['LITELLM_LOCAL_MODEL_COST_MAP'] = 'True'
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(ROOT / 'exp2layer'))
from tau2.domains.retail.data_model import RetailDB
from tau2.domains.retail.tools import RetailTools
from state import EvidenceState

DATA = REPO / 'data' / 'tau2' / 'domains' / 'retail'
MODEL = 'deepseek-flash'
ARMS = ('direct', 'full_framework')
MAX_STEPS = 12
CHANGE = ('Before you submit, change just the keyboard: I now want tactile switches, white backlight, '
          'and full size instead of the clicky, no-backlight one. Keep the black Google Assistant '
          'thermostat exchange and the same Mastercard; those are still what I want. '
          'Those are all the items. Please check the updated amount before proceeding.')
ACTOR = '''You are a retail agent continuing the actual conversation below. Follow the retail policy.
Choose your own next work: obtain information, review existing evidence, reason, communicate, or execute.
Use the actual tools with arguments you choose. Available tool schemas are identical across conditions.
Do not treat earlier approval as approval of a changed proposal. Keep evidence that remains applicable.
If a maintained evidence state is provided, it is fallible memory, not new external evidence or an action instruction.
You may use cached results without repeating queries. Do not invent facts. At most one tool per turn;
do not combine a tool call and a user-facing reply. No fixed workflow or tool sequence is required.
'''
OBSERVER = '''Maintain evidence memory from the numbered conversation. Output JSON only:
{"facts":[{"id":"f.stable_name","value":<JSON>,"sources":[message_index]}],
 "judgments":[{"id":"j.stable_name","text":"a conclusion", "depends_on":["f.name","j.name"],
 "sources":[message_index],"status":"supported|unknown"}]}
Return a compact patch, keeping existing IDs stable; unchanged entries may be omitted. No deletions.
Separate observed facts from derived judgments. Keep intent per entity/item rather than a merged request blob.
Facts are grounded only in user messages or successful tool outputs. User intent changes are interpreted from
the actual user message, never from an external event dictionary. Assistant proposals are not user approvals.
Record the scope and terms of any approval and connect derived validity of that approval to the exact
plan/intent/amount on which it depends. Do not mutate historical approval into approval of a new proposal.
Retain unrelated facts and judgments. Changed conditions invalidate dependent judgments through the engine;
refresh a judgment only if current evidence supports it. Preserve provenance for derived conclusions.
Do not select tools, suggest a next action, or provide a ready-made tool-call plan. Do not invent any
unobserved IDs, prices or availability. About 18 facts and 16 judgments are sufficient; keep values compact.
'''
USER = '''You are the customer Yusuf Rossi in this retail conversation, not the retail agent.
The last user message changed only the keyboard to tactile switches, white backlight, full size.
The black Google Assistant thermostat and original Mastercard remain desired. These are all items.
Reply naturally to the agent. Do not provide any tool/variant IDs, database facts, or calculate unknown prices.
Only give explicit yes when the agent has explained the revised keyboard and updated combined price
difference/refund, with the unchanged thermostat/payment retained in the context. A targeted updated
confirmation is sufficient; do not demand that unchanged evidence be re-queried or every detail repeated.
If asked about the same unchanged identity/payment/order, answer consistently but do not request it yourself.
If the agent wrongly claims an exchange already happened, ask about the requested keyboard change.
Only return your customer reply, no JSON or analysis.
'''


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serial(value):
    if hasattr(value, 'model_dump'):
        return value.model_dump(mode='json')
    return value


def new_tools():
    return RetailTools(RetailDB.load(DATA / 'db.json'))


def call(tools, name, args):
    return serial(tools.get_tools()[name](**args))


def fixture():
    task = next(t for t in json.loads((DATA / 'tasks.json').read_text(encoding='utf-8')) if t['id'] == '0')
    tools = new_tools()
    history = [{'role': 'user', 'content': task['user_scenario']['instructions']['reason_for_call'] +
                ' I am Yusuf Rossi, zip 19122. I do not remember my email.'}]

    def read(name, args):
        cid = 'prefix_' + str(len(history))
        history.append({'role': 'assistant', 'tool_calls': [{'id': cid, 'type': 'function',
                        'function': {'name': name, 'arguments': json.dumps(args)}}]})
        result = call(tools, name, args)
        history.append({'role': 'tool', 'tool_call_id': cid, 'content': json.dumps(result, ensure_ascii=False)})
        return result

    uid = read('find_user_id_by_name_zip', {'first_name': 'Yusuf', 'last_name': 'Rossi', 'zip': '19122'})
    read('get_user_details', {'user_id': uid})
    order = read('get_order_details', {'order_id': '#W2378156'})
    for pid in ('1656367028', '4896585277'):
        read('get_product_details', {'product_id': pid})
    read('calculate', {'expression': '(269.16 - 272.33) + (249.01 - 262.47)'})
    history += [
        {'role': 'assistant', 'content': 'For order #W2378156, exchange keyboard 1151293680 for '
         '7706410293 (clicky switches, no backlight, full size), price $269.16 instead of $272.33; '
         'and thermostat 4983901480 for 7747408585 (Google Assistant, black), price $249.01 instead of '
         '$262.47. Combined refund: $16.63 to the original Mastercard ending 2478 '
         '(credit_card_9513926). Exchanges can be requested only once per order. '
         'Please confirm these are all the items you wish to exchange and that I should proceed.'},
        {'role': 'user', 'content': 'Yes, I confirm both exchanges exactly as described, the $16.63 refund '
         'to that Mastercard, and that these are all the items. Please proceed.'},
    ]
    baseline = next(a['arguments'] for a in task['evaluation_criteria']['actions']
                    if a['name'] == 'exchange_delivered_order_items')
    changed = deepcopy(baseline)
    changed['new_item_ids'][0] = '3616838507'
    variant = {'task_id': '0', 'order_id': order['order_id'], 'source_task': task,
               'construction': 'curated shared prefix replayed through unmodified official read tools; not a sampled prefix',
               'shared_history': history, 'change_message': {'role': 'user', 'content': CHANGE},
               'private_evaluation': {'old_arguments': baseline, 'expected_arguments': changed,
                                      'expected_difference': -59.68},
               'db_sha256': sha(DATA / 'db.json'), 'policy_sha256': sha(DATA / 'policy.md')}
    return variant


def protected():
    work = ROOT / 'Codex工作区'
    roots = [HERE.parent / '01_动态约束认知决策小试', HERE.parent / '02_动态约束多轮小试']
    paths = [p for root in roots for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [p for p in (work / '申报与文献').rglob('*') if p.is_file() and '申报' in p.name
              and p.suffix.lower() in ('.md', '.docx') and not p.name.startswith('~$')]
    paths += [DATA / n for n in ('db.json', 'tasks.json', 'policy.md')]
    return {str(p): sha(p) for p in sorted(paths)}


def same_arguments(actual, expected):
    try:
        return (actual['order_id'] == expected['order_id'] and
                actual['payment_method_id'] == expected['payment_method_id'] and
                len(actual['item_ids']) == len(actual['new_item_ids']) == len(expected['item_ids']) and
                sorted(zip(actual['item_ids'], actual['new_item_ids'])) ==
                sorted(zip(expected['item_ids'], expected['new_item_ids'])))
    except (KeyError, TypeError):
        return False


def final_score(tools, variant, calls):
    private = variant['private_evaluation']
    order = tools.db.orders[variant['order_id']].model_dump(mode='json')
    writes = [c for c in calls if c['write']]
    exact_call = len(writes) == 1 and writes[0]['ok'] and writes[0]['name'] == 'exchange_delivered_order_items' and same_arguments(writes[0]['arguments'], private['expected_arguments'])
    correct_effect = (order['status'] == 'exchange requested' and
                      order.get('exchange_items') == sorted(private['expected_arguments']['item_ids']) and
                      order.get('exchange_new_items') == sorted(private['expected_arguments']['new_item_ids']) and
                      order.get('exchange_payment_method_id') == private['expected_arguments']['payment_method_id'] and
                      Decimal(str(order.get('exchange_price_difference'))) == Decimal(str(private['expected_difference'])))
    return {'actual_write_correct': bool(exact_call and correct_effect),
            'write_attempts': len(writes), 'final_order': order,
            'confirmation_and_evidence_reuse': 'pending transcript review; not inferred from tool success'}


def offline(variant):
    checks = []
    tools = new_tools()
    schemas = [t.openai_schema for t in tools.get_tools().values()]
    assert any(t['function']['name'] == 'exchange_delivered_order_items' for t in schemas)
    assert tools.db.orders[variant['order_id']].status == 'delivered'
    args = variant['private_evaluation']['expected_arguments']
    result = call(tools, 'exchange_delivered_order_items', args)
    fake_call = {'name': 'exchange_delivered_order_items', 'arguments': args, 'write': True, 'ok': True}
    assert final_score(tools, variant, [fake_call])['actual_write_correct']
    assert result['exchange_price_difference'] == -59.68
    checks.append('official tools accept revised pair and compute refund 59.68')
    try:
        call(tools, 'exchange_delivered_order_items', args)
    except ValueError:
        checks.append('official once-per-order behavior retained')
    else:
        raise AssertionError('repeat exchange accepted')
    old = new_tools()
    old_args = variant['private_evaluation']['old_arguments']
    call(old, 'exchange_delivered_order_items', old_args)
    assert not final_score(old, variant, [{'name': 'exchange_delivered_order_items', 'arguments': old_args,
                                          'write': True, 'ok': True}])['actual_write_correct']
    checks.append('old approved plan can pass official tools but must fail revised task scorer')
    partial = deepcopy(args)
    partial['item_ids'] = partial['item_ids'][:1]
    partial['new_item_ids'] = partial['new_item_ids'][:1]
    assert not same_arguments(partial, args)
    reverse = deepcopy(args)
    reverse['new_item_ids'].reverse()
    assert not same_arguments(reverse, args)
    reordered = deepcopy(args)
    reordered['item_ids'].reverse()
    reordered['new_item_ids'].reverse()
    assert same_arguments(reordered, args)
    checks.append('missing item/wrong positional mapping fail; valid paired reordering passes')
    state = EvidenceState()
    state.apply({'facts': [{'id': 'f.a', 'value': 1, 'sources': [0]}, {'id': 'f.b', 'value': 2, 'sources': [0]}],
                 'judgments': [{'id': 'j.a', 'text': 'a conclusion', 'depends_on': ['f.a'], 'sources': [0], 'status': 'supported'},
                               {'id': 'j.downstream', 'text': 'dependent conclusion', 'depends_on': ['j.a'], 'sources': [0], 'status': 'supported'},
                               {'id': 'j.b', 'text': 'unrelated conclusion', 'depends_on': ['f.b'], 'sources': [0], 'status': 'supported'}]}, 1)
    trans = state.apply({'facts': [{'id': 'f.a', 'value': 3, 'sources': [1]}]}, 2)
    assert trans['still_stale'] == ['j.a', 'j.downstream']
    assert state.judgments['j.b']['status'] == 'supported'
    assert state.facts['f.b']['version'] == 1
    checks.append('domain-neutral transitive invalidation preserves unrelated evidence/version')
    nested = EvidenceState()
    nested.apply({'facts': [{'id': 'f.observation', 'value': {'content': 'observed', 'sources': [0]}}]}, 1)
    assert nested.facts['f.observation']['sources'] == [0]
    checks.append('lossless nested provenance syntax accepted without inferring evidence')
    before = state.snapshot()
    try:
        state.apply({'judgments': [{'id': 'j.bad', 'text': 'cycle', 'depends_on': ['j.bad'], 'sources': [0], 'status': 'supported'}]}, 2)
    except ValueError:
        assert state.snapshot() == before
        checks.append('invalid dependency patch rejected atomically')
    else:
        raise AssertionError('cycle accepted')
    state.apply({'judgments': [{'id': 'j.unresolved', 'text': 'no invented support', 'depends_on': ['f.not_observed'],
                               'sources': [0], 'status': 'supported'}]}, 2)
    assert state.judgments['j.unresolved']['status'] == 'unknown'
    assert state.snapshot()['unresolved_dependencies'] == ['f.not_observed']
    assert state.judgments['j.b']['status'] == 'supported'
    checks.append('unresolved dependency stays explicit and unknown, without guessing or discarding unrelated support')
    assert 'private_evaluation' not in json.dumps(variant['shared_history'])
    checks.append('model conversation contains no evaluation fields or injected future facts')
    return {'status': 'passed', 'checks': checks, 'reference_final_order': result,
            'note': 'offline tests are not model results; no confirmation gate added to official tools'}


class LoggedClient:
    def __init__(self, output, replay_from=None):
        from llm import DeepSeek
        self.client = DeepSeek(model=MODEL, timeout=60)
        self.stream = (output / 'model_calls.jsonl').open('w', encoding='utf-8')
        self.count = 0
        self.replay = {}
        self.replay_from = replay_from
        if replay_from:
            archived = [json.loads(line) for line in (replay_from / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
            self.replay = {r['kind']: r for r in archived if 'response' in r}
            if len(self.replay) != len(archived):
                raise ValueError('replay source contains duplicate kinds or API errors')

    def ask(self, kind, messages, tools=None, max_tokens=1600):
        self.count += 1
        request = {'kind': kind, 'messages': deepcopy(messages), 'tools': tools,
                   'temperature': 0, 'thinking': False, 'max_tokens': max_tokens}
        if kind in self.replay:
            row = deepcopy(self.replay.pop(kind))
            assert all(row[k] == value for k, value in request.items()), 'replay request differs: ' + kind
            row.update(call=self.count, reused_from=str(self.replay_from.resolve()),
                       archived_log_sha256=sha(self.replay_from / 'model_calls.jsonl'))
            self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            self.stream.flush()
            print(f'call {self.count}: {kind} (exact replay, no API call)', flush=True)
            return row['response']['choices'][0]['message']
        try:
            rec = self.client.chat(kind, messages, tools=tools, temperature=0, thinking=False,
                                   max_tokens=max_tokens, retries=0)
            row = {'call': self.count, **request, 'response': rec['response'], 'seconds': rec['seconds']}
        except Exception as exc:
            code = re.search(r'Error code: (\d+)', str(exc))
            row = {'call': self.count, **request, 'error': ('HTTP ' + code[1]) if code else type(exc).__name__}
            self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            self.stream.flush()
            raise RuntimeError(row['error']) from None
        self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.stream.flush()
        print(f'call {self.count}: {kind}', flush=True)
        return rec['response']['choices'][0]['message']

    def close(self):
        self.stream.close()
        self.client.close()

    def adopt_prefix_response(self, source, variant):
        archived = [json.loads(line) for line in (source / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(archived) == 1 and archived[0]['kind'] == 'full_framework/prefix_memory'
        row = archived[0]
        assert row['messages'][0]['content'] == OBSERVER
        payload = json.loads(row['messages'][1]['content'])
        assert payload == {'existing_state': {'facts': {}, 'judgments': {}},
                           'numbered_conversation': [{'index': i, **m} for i, m in enumerate(variant['shared_history'])]}
        assert row['response']['model'] == MODEL and row['max_tokens'] == 4096
        self.count = 1
        row['reused_from'] = str(source.resolve())
        row['archived_log_sha256'] = sha(source / 'model_calls.jsonl')
        self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        self.stream.flush()
        return row['response']['choices'][0]['message']


def parse_json(text):
    return json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', text.strip()))


def maintain(client, state, history, kind):
    messages = [{'role': 'system', 'content': OBSERVER}, {'role': 'user', 'content': json.dumps({
        'existing_state': state.snapshot(),
        'numbered_conversation': [{'index': i, **m} for i, m in enumerate(history)]}, ensure_ascii=False)}]
    response = client.ask(kind, messages, max_tokens=4096)
    patch = parse_json(response.get('content') or '')
    return state.apply(patch, len(history))


def execute_arm(arm, variant, client, output, seed_state):
    history = deepcopy(variant['shared_history']) + [deepcopy(variant['change_message'])]
    tools = new_tools()
    schemas = [t.openai_schema for t in tools.get_tools().values()]
    state = EvidenceState()
    if arm == 'full_framework':
        state.facts = deepcopy(seed_state['facts'])
        state.judgments = deepcopy(seed_state['judgments'])
    rows, executed = [], []
    stop = 'step_limit'
    for step in range(1, MAX_STEPS + 1):
        row = {'step': step, 'history_before': deepcopy(history)}
        if arm == 'full_framework':
            row['state_transition'] = maintain(client, state, history, f'{arm}/maintain/{step}')
        system = ACTOR + '\n\n' + (DATA / 'policy.md').read_text(encoding='utf-8')
        if arm == 'full_framework':
            system += '\nMaintained evidence state:\n' + json.dumps(state.snapshot(), ensure_ascii=False)
        messages = [{'role': 'system', 'content': system}] + history
        message = client.ask(f'{arm}/actor/{step}', messages, tools=schemas, max_tokens=1600)
        content, tcs = message.get('content') or '', message.get('tool_calls') or []
        row['assistant'] = deepcopy(message)
        if len(tcs) > 1 or (tcs and content.strip()) or (not tcs and not content.strip()):
            row['error'] = 'invalid single-action response'
            rows.append(row)
            stop = 'format_error'
            break
        clean = {'role': 'assistant'}
        if tcs:
            clean['tool_calls'] = tcs
        else:
            clean['content'] = content
        history.append(clean)
        if tcs:
            tc = tcs[0]
            name = tc['function']['name']
            args = parse_json(tc['function']['arguments'])
            write = name in tools.tools and str(tools.tool_type(name).value) == 'write'
            action = {'name': name, 'arguments': args, 'write': write}
            try:
                result = call(tools, name, args)
                action.update(ok=True, result=result)
            except Exception as exc:
                action.update(ok=False, error=type(exc).__name__ + ': ' + str(exc))
                result = {'error': action['error']}
            history.append({'role': 'tool', 'tool_call_id': tc['id'], 'content': json.dumps(result, ensure_ascii=False)})
            executed.append(action)
            row['tool_execution'] = action
            if write and action['ok']:
                stop = 'write_completed'
            if name == 'transfer_to_human_agents':
                stop = 'transferred'
        else:
            # The customer sees only actual conversational utterances, not tool outputs or state memory.
            visible = [{'index': i, 'role': m['role'], 'content': m['content']} for i, m in enumerate(history)
                       if m['role'] in ('user', 'assistant') and m.get('content')]
            reply = client.ask(f'{arm}/customer/{step}', [
                {'role': 'system', 'content': USER},
                {'role': 'user', 'content': json.dumps(visible, ensure_ascii=False)}], max_tokens=512)
            customer = {'role': 'user', 'content': reply.get('content') or ''}
            if not customer['content'].strip():
                raise ValueError('empty customer reply')
            history.append(customer)
            row['customer'] = customer
        rows.append(row)
        save(output / f'{arm}_trajectory.json', {'arm': arm, 'steps': rows, 'history': history, 'stop': stop})
        print(f'{arm} step {step}: {tcs[0]["function"]["name"] if tcs else "communicate"}', flush=True)
        if stop != 'step_limit':
            break
    # Observe final tool feedback; this never gets another corrective actor turn.
    if arm == 'full_framework' and stop == 'write_completed':
        save(output / 'full_framework_final_state_transition.json',
             maintain(client, state, history, f'{arm}/final_observation'))
    result = {'arm': arm, 'steps': len(rows), 'stop': stop, 'business_calls': executed,
              'state_final': state.snapshot() if arm == 'full_framework' else None,
              **final_score(tools, variant, executed)}
    save(output / f'{arm}_result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--prefix-from', type=Path, help='reuse an archived initialization response after syntax-only compatibility fix')
    parser.add_argument('--replay-from', type=Path, help='exactly replay archived requests/responses and continue only unseen work')
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = HERE / ('selfcheck' if args.check else 'results') / stamp
    out.mkdir(parents=True)
    before = protected()
    save(out / 'protected_before.json', before)
    variant = fixture()
    save(out / 'scenario.json', variant)
    save(out / 'offline_check.json', offline(variant))
    print('Offline checks passed.', flush=True)
    if args.check:
        save(out / 'protected_verification.json', {'unchanged': protected() == before, 'files': len(before)})
        print(out, flush=True)
        return
    snapshot = out / 'snapshot'
    snapshot.mkdir()
    for name in ('run.py', 'state.py', 'README.md', '方案.md'):
        shutil.copy2(HERE / name, snapshot / name)
    shutil.copy2(ROOT / 'exp2layer' / 'llm.py', snapshot / 'llm.py')
    shutil.copy2(DATA / 'policy.md', snapshot / 'official_policy.md')
    shutil.copy2(DATA / 'db.json', snapshot / 'official_db.json')
    save(snapshot / 'official_task.json', variant['source_task'])
    source_paths = [DATA / n for n in ('db.json', 'tasks.json', 'policy.md')]
    source_paths += [REPO / 'src' / 'tau2' / 'domains' / 'retail' / n for n in ('tools.py', 'data_model.py')]
    save(out / 'metadata.json', {'model': MODEL, 'temperature': 0, 'thinking': False, 'retries': 0,
         'timeout': 60, 'actor_max_tokens': 1600, 'observer_max_tokens': 4096, 'customer_max_tokens': 512,
         'actor_step_limit': MAX_STEPS, 'task_count': 1, 'arm_order': list(ARMS), 'repetitions': 1,
         'reused_prefix_response_from': str(args.prefix_from.resolve()) if args.prefix_from else None,
         'replayed_responses_from': str(args.replay_from.resolve()) if args.replay_from else None,
         'shared_prefix_sha256': hashlib.sha256(json.dumps(variant['shared_history'], ensure_ascii=False).encode()).hexdigest(),
         'official_source_sha256': {str(p): sha(p) for p in source_paths},
         'snapshot_sha256': {p.name: sha(p) for p in snapshot.iterdir()},
         'observer_prompt': OBSERVER, 'actor_prompt': ACTOR, 'customer_prompt': USER,
         'architecture': 'versioned evidence state -> model-selected cognitive work and free native tool execution -> observation',
         'resource_note': 'framework has extra memory maintenance calls; report separately, not a matched-compute ablation'})
    client = LoggedClient(out, args.replay_from)
    results = []
    error = None
    try:
        seed = EvidenceState()
        if args.prefix_from:
            archived = client.adopt_prefix_response(args.prefix_from, variant)
            initial_transition = seed.apply(parse_json(archived.get('content') or ''), len(variant['shared_history']))
        else:
            initial_transition = maintain(client, seed, variant['shared_history'], 'full_framework/prefix_memory')
        save(out / 'prefix_state.json', initial_transition)
        for arm in ARMS:
            results.append(execute_arm(arm, variant, client, out, seed.snapshot()))
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        client.close()
        after = protected()
        save(out / 'protected_verification.json', {'unchanged': before == after, 'files': len(before),
             'changed_paths': [p for p in before.keys() | after.keys() if before.get(p) != after.get(p)]})
        save(out / 'run_status.json', {'complete': len(results) == 2 and error is None,
                                     'model_calls': client.count, 'error': error})
        save(out / 'results.json', results)
    print(out, flush=True)
    if error:
        raise SystemExit(error)
    assert before == after


if __name__ == '__main__':
    main()
