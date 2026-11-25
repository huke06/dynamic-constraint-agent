"""LLM semantics + deterministic retail state; one existing paired case only."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'tau2-official').is_dir())
REPO = ROOT / 'tau2-official'
DATA = REPO / 'data/tau2/domains/retail'
SOURCE = HERE.parent / 'results/20261120T023925255858Z'
os.environ['TAU2_DATA_DIR'] = str(REPO / 'data')
os.environ['LITELLM_LOCAL_MODEL_COST_MAP'] = 'True'
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(ROOT / 'exp2layer'))
from tau2.domains.retail.data_model import RetailDB
from tau2.domains.retail.tools import RetailTools
from ledger import Ledger, packed

MODEL = 'deepseek-flash'
ARMS = ('direct', 'hybrid_framework')
WRITE = 'exchange_delivered_order_items'
ARGUMENTS = {'type': 'object', 'properties': {
    'order_id': {'type': 'string'}, 'item_ids': {'type': 'array', 'items': {'type': 'string'}},
    'new_item_ids': {'type': 'array', 'items': {'type': 'string'}}, 'payment_method_id': {'type': 'string'}},
    'required': ['order_id', 'item_ids', 'new_item_ids', 'payment_method_id'], 'additionalProperties': False}
ACTOR = '''Continue this retail case under the policy. Independently decide what information, review,
reasoning, communication or execution is needed. Choose exact tool arguments yourself. At most one tool
call or one user-facing reply per turn. Retain applicable evidence; approvals apply to their exact terms.
Program helpers are available equally to both conditions: delegate exact filtering/calculation/checks
to them. A prepared quote is not user approval. You may use cached evidence without re-querying.
If receiving a compact case view, source records remain available via read_evidence; request evidence
when needed. Stale values are historical, not currently applicable. Tool feedback is authoritative
only for what that tool actually establishes. No predetermined action order is required.
'''
BOOT = '''Interpret ONLY the three numbered utterances using the observed entity inventory. Return JSON:
{"old_plan":{"order_id":"...","item_ids":["..."],"new_item_ids":["..."],"payment_method_id":"..."},
"old_difference":-12.34,"old_confirmed":true,"changes":[{"item_id":"old item id","set_options":{"option key":"new value"}}]}.
Extract the old explicitly approved proposal from assistant+user utterances; negative difference means
refund, positive means charge. Interpret the newest user message as semantic option deltas ONLY.
Keep unmentioned items/options/payment unchanged by omitting them from changes. Use exact observed
option keys and normalize user wording to observed option vocabulary. Do not select a new variant,
calculate amounts, invent a dependency graph, or output any source IDs. Code handles these.
'''
CONFIRM = '''Interpret this assistant proposal and the following customer reply in their case context.
Return JSON only: {"approved":true|false,"proposal":null|{"order_id":"...","item_ids":["..."],
"new_item_ids":["..."],"payment_method_id":"..."},"stated_difference":number|null,
"changes":[{"item_id":"old item id","set_options":{"option key":"new value"}}],"reason":"brief"}.
Approve only if the reply explicitly agrees and the assistant/context identifies the revised items,
the updated combined charge/refund and payment. A targeted confirmation can preserve unchanged terms.
No approval if customer changes terms in the reply. Extract actual stated terms, not a preferred answer.
Negative difference means refund. Do not calculate missing amounts. IDs may be resolved from observed
context when natural language identifies the item unambiguously. Do not invent facts or source IDs.
'''


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(raw):
    return json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip()))


def tools_new():
    return RetailTools(RetailDB.load(DATA / 'db.json'))


def serial(result):
    return result.model_dump(mode='json') if hasattr(result, 'model_dump') else result


def schemas(tools):
    official = [tool.openai_schema for tool in tools.get_tools().values()]
    helpers = [
        ('review_items', 'Re-evaluate selected items using cached product evidence and current normalized requirements. Exact filtering only, no model call. Returns all matching available variants and observed prices; does not choose among multiple matches or submit.',
         {'type': 'object', 'properties': {'item_ids': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['item_ids'], 'additionalProperties': False}),
        ('prepare_proposal', 'Check these self-selected exchange arguments against observed facts and current requirements; compute exact per-item and combined difference, create a proposal fingerprint. Does not contact/confirm with user and does not submit.', ARGUMENTS),
        ('read_evidence', 'Read cached source messages by numeric string index or typed record names. No external query. Preserves access to unabridged evidence when a compact context omits it.',
         {'type': 'object', 'properties': {'references': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['references'], 'additionalProperties': False}),
    ]
    return official + [{'type': 'function', 'function': {'name': name, 'description': description, 'parameters': parameters}}
                       for name, description, parameters in helpers]


def protected():
    experiment = HERE.parent.parent
    paths = [p for folder in experiment.iterdir() if folder.is_dir() and folder != HERE
             for p in folder.rglob('*') if p.is_file() and HERE not in p.parents and '__pycache__' not in p.parts]
    proposal = ROOT / 'Codex工作区/申报与文献'
    paths += [p for p in proposal.rglob('*') if p.is_file() and '申报' in p.name and p.suffix.lower() in ('.md', '.docx') and not p.name.startswith('~$')]
    paths += [DATA / n for n in ('db.json', 'tasks.json', 'policy.md')]
    return {str(p): sha(p) for p in sorted(set(paths))}


class Client:
    def __init__(self, output):
        from llm import DeepSeek
        self.llm = DeepSeek(model=MODEL, timeout=60)
        self.file = (output / 'model_calls.jsonl').open('w', encoding='utf-8')
        self.rows = []

    def ask(self, kind, messages, tool_schemas=None, max_tokens=1200):
        row = {'kind': kind, 'messages': deepcopy(messages), 'tools': deepcopy(tool_schemas),
               'temperature': 0, 'thinking': False, 'max_tokens': max_tokens}
        try:
            rec = self.llm.chat(kind, messages, tools=tool_schemas, max_tokens=max_tokens,
                                temperature=0, thinking=False, retries=0)
            row.update(response=rec['response'], seconds=rec['seconds'])
        except Exception as exc:
            row['error'] = type(exc).__name__
            raise RuntimeError(row['error']) from None
        finally:
            self.rows.append(row)
            self.file.write(json.dumps(row, ensure_ascii=False) + '\n')
            self.file.flush()
        print(kind, flush=True)
        return row['response']['choices'][0]['message']

    def close(self):
        self.file.close()
        self.llm.close()


def bootstrap_input(case, ledger):
    history = case['shared_history']
    return {'observed_entities': {'orders': ledger.orders, 'user_ids': list(ledger.users),
                                 'payment_methods': {uid: list(user['payment_methods']) for uid, user in ledger.users.items()},
                                 'option_keys': {pid: sorted(set().union(*(set(v['options']) for v in p['variants'].values())))
                                                 for pid, p in ledger.products.items()}},
            'utterances': [{'index': len(history) - 2, **history[-2]}, {'index': len(history) - 1, **history[-1]},
                           {'index': len(history), **case['change_message']}]}


def bootstrap(case, semantics):
    ledger = Ledger(case['shared_history'])
    size = len(case['shared_history'])
    ledger.seed(semantics, size - 2, size - 1)
    ledger.evidence[str(size)] = deepcopy(case['change_message'])
    change = ledger.apply_changes(semantics['changes'], size)
    return ledger, change


def context(ledger, latest, dialogue):
    # Exact typed state only, never an LLM summary or a truncated raw transcript.
    return {'case': ledger.view(), 'latest_observation': latest, 'recent_user_visible_dialogue': dialogue[-4:]}


def evaluate(tools, case, executions, confirmations):
    expected = case['private_evaluation']['expected_arguments']
    writes = [entry for entry in executions if entry['write']]
    pairs = lambda args: sorted(zip(args['item_ids'], args['new_item_ids']))
    good = (len(writes) == 1 and writes[0]['ok'] and writes[0]['name'] == WRITE and
            pairs(writes[0]['arguments']) == pairs(expected) and
            writes[0]['arguments']['order_id'] == expected['order_id'] and
            writes[0]['arguments']['payment_method_id'] == expected['payment_method_id'])
    actual = tools.db.orders[case['order_id']].model_dump(mode='json')
    good = good and actual['status'] == 'exchange requested' and actual.get('exchange_price_difference') == case['private_evaluation']['expected_difference']
    return {'actual_write_correct': bool(good), 'write_attempts': len(writes),
            'accepted_new_confirmations': len(confirmations), 'final_order': actual,
            'compliant_completion': bool(good and len(confirmations) > 0 and all(w.get('gate', {}).get('allowed') for w in writes))}


def execute(arm, case, semantics, client, output, customer_prompt):
    ledger, change = bootstrap(case, semantics)
    history = deepcopy(case['shared_history']) + [deepcopy(case['change_message'])]
    tools = tools_new()
    all_schemas = schemas(tools)
    policy = (DATA / 'policy.md').read_text(encoding='utf-8')
    dialogue = [m for m in history if m['role'] in ('user', 'assistant') and m.get('content')][-3:]
    latest = {'user_message': case['change_message']['content'], 'source': len(history) - 1}
    steps, executions, confirmations = [], [], []
    save(output / f'{arm}_initial_state.json', {'semantic_transition': change, 'state': ledger.snapshot()})
    stop = 'step_limit'
    for step in range(1, 11):
        if arm == 'direct':
            messages = [{'role': 'system', 'content': ACTOR + '\n' + policy}] + history
        else:
            messages = [{'role': 'system', 'content': ACTOR + '\n' + policy},
                        {'role': 'user', 'content': packed(context(ledger, latest, dialogue))}]
        row = {'step': step, 'state_before': ledger.snapshot(), 'request_characters': len(packed(messages))}
        message = client.ask(f'{arm}/actor/{step}', messages, all_schemas, max_tokens=1600)
        row['assistant'] = message
        tcs, content = message.get('tool_calls') or [], message.get('content') or ''
        if len(tcs) > 1 or (tcs and content.strip()) or (not tcs and not content.strip()):
            row['error'] = 'single-action format violation'
            steps.append(row)
            stop = 'format_error'
            break
        if tcs:
            tcs = [{k: v for k, v in tc.items() if k != 'index'} for tc in tcs]
            history.append({'role': 'assistant', 'tool_calls': tcs})
            tc = tcs[0]
            name, arguments = tc['function']['name'], parse(tc['function']['arguments'])
            write = name in tools.tools and tools.tool_type(name).value == 'write'
            action = {'name': name, 'arguments': arguments, 'write': write, 'ok': False}
            ref = len(history)
            try:
                if name == 'review_items':
                    result = ledger.review(arguments['item_ids'], ref)
                elif name == 'prepare_proposal':
                    result = ledger.prepare(arguments, ref)
                elif name == 'read_evidence':
                    result = ledger.read_evidence(arguments['references'])
                else:
                    if write:
                        if name != WRITE:
                            raise ValueError('no user-authorized action of this write type in this adapter')
                        action['gate'] = ledger.gate(arguments)
                    result = serial(tools.get_tools()[name](**arguments))
                    ledger.observe(name, arguments, result, ref)
                action.update(ok=True, result=result)
            except (ValueError, KeyError, TypeError) as exc:
                result = {'error': str(exc)}
                action['error'] = str(exc)
            tool_message = {'role': 'tool', 'tool_call_id': tc['id'], 'content': json.dumps(result, ensure_ascii=False)}
            ledger.evidence[str(ref)] = deepcopy(tool_message)
            history.append(tool_message)
            latest = {'tool': name, 'result': result, 'source': ref}
            # Large raw records stay cached. Their full contents can be explicitly requested.
            if name in ('get_product_details', 'get_order_details', 'get_user_details') and action['ok']:
                latest = {'tool': name, 'stored_source': ref, 'result': 'typed records updated; unabridged evidence available'}
            row['tool_execution'] = action
            executions.append(action)
            if write and action['ok']:
                stop = 'write_completed'
            elif name == 'transfer_to_human_agents':
                stop = 'transferred'
        else:
            assistant_ref = len(history)
            spoken = {'role': 'assistant', 'content': content}
            history.append(spoken)
            dialogue.append(spoken)
            ledger.evidence[str(assistant_ref)] = deepcopy(spoken)
            visible = [{'index': i, **m} for i, m in enumerate(history) if m['role'] in ('user', 'assistant') and m.get('content')]
            reply = client.ask(f'{arm}/customer/{step}', [{'role': 'system', 'content': customer_prompt},
                               {'role': 'user', 'content': json.dumps(visible, ensure_ascii=False)}], max_tokens=512)
            customer = {'role': 'user', 'content': reply.get('content') or ''}
            if not customer['content']:
                raise ValueError('empty customer reply')
            user_ref = len(history)
            history.append(customer)
            dialogue.append(customer)
            ledger.evidence[str(user_ref)] = deepcopy(customer)
            semantics_input = {'case': ledger.view(), 'assistant_proposal': content, 'customer_reply': customer['content'],
                               'observed_order': ledger.orders[ledger.order_id],
                               'cached_products': {pid: {'name': p['name'], 'variants': [
                                   {'item_id': v['item_id'], 'options': v['options']} for v in p['variants'].values()]}
                                   for pid, p in ledger.products.items()}}
            parsed = parse(client.ask(f'{arm}/semantics/{step}', [{'role': 'system', 'content': CONFIRM},
                           {'role': 'user', 'content': packed(semantics_input)}], max_tokens=1000)['content'])
            if parsed.get('changes'):
                ledger.apply_changes(parsed['changes'], user_ref)
            accepted = None
            if parsed['approved'] is True and not parsed.get('changes'):
                try:
                    accepted = ledger.confirm(parsed['proposal'], parsed['stated_difference'], user_ref, assistant_ref)
                    confirmations.append(accepted)
                except (ValueError, KeyError, TypeError) as exc:
                    accepted = {'accepted': False, 'error': str(exc)}
            row.update(customer=customer, semantic_parse=parsed, confirmation_binding=accepted,
                       semantic_sources=[assistant_ref, user_ref])
            latest = {'user_message': customer['content'], 'source': user_ref, 'confirmation_binding': accepted}
        row['state_after'] = ledger.snapshot()
        steps.append(row)
        save(output / f'{arm}_trajectory.json', {'arm': arm, 'steps': steps, 'history': history, 'stop': stop})
        print(f'{arm} step {step}: {tcs[0]["function"]["name"] if tcs else "communicate"}', flush=True)
        if stop != 'step_limit':
            break
    result = {'arm': arm, 'steps': len(steps), 'stop': stop, 'executions': executions,
              'final_state': ledger.snapshot(), 'confirmation_history': ledger.old_confirmations,
              **evaluate(tools, case, executions, confirmations)}
    save(output / f'{arm}_result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    from checks import offline
    case = read(SOURCE / 'scenario.json')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = HERE / ('selfcheck' if args.check else 'results') / stamp
    output.mkdir(parents=True)
    save(output / 'offline_check.json', offline(case))
    print('Offline checks passed.', flush=True)
    before = protected()
    save(output / 'protected_before.json', before)
    save(output / 'scenario.json', case)
    if args.check:
        save(output / 'protected_verification.json', {'unchanged': before == protected(), 'files': len(before)})
        print(output, flush=True)
        return
    snapshot = output / 'snapshot'
    snapshot.mkdir()
    for name in ('run.py', 'ledger.py', 'checks.py', 'README.md', '设计说明.md'):
        shutil.copy2(HERE / name, snapshot / name)
    shutil.copy2(ROOT / 'exp2layer/llm.py', snapshot / 'llm.py')
    old_metadata = read(SOURCE / 'metadata.json')
    customer_prompt = old_metadata['customer_prompt']
    save(output / 'metadata.json', {'model': MODEL, 'temperature': 0, 'thinking': False, 'retries': 0,
         'actor_max_tokens': 1600, 'task_count': 1, 'repetitions': 1, 'arm_order': list(ARMS),
         'source_scenario': str(SOURCE / 'scenario.json'), 'source_scenario_sha256': sha(SOURCE / 'scenario.json'),
         'snapshot_sha256': {p.name: sha(p) for p in snapshot.iterdir()},
         'policy_sha256': sha(DATA / 'policy.md'), 'tools': schemas(tools_new()),
         'actor_prompt': ACTOR, 'bootstrap_prompt': BOOT, 'confirmation_prompt': CONFIRM, 'customer_prompt': customer_prompt,
         'comparison': 'same semantic adapter/gates/tools, direct raw history versus hybrid typed compact context',
         'semantic_bootstrap': 'one shared call; no gold values passed to any model'})
    client = Client(output)
    results, error = [], None
    try:
        initial = Ledger(case['shared_history'])
        semantics = parse(client.ask('shared/semantics/bootstrap', [{'role': 'system', 'content': BOOT},
                          {'role': 'user', 'content': packed(bootstrap_input(case, initial))}], max_tokens=1400)['content'])
        save(output / 'bootstrap_semantics.json', semantics)
        # Validate shared semantic output before starting either arm.
        bootstrap(case, semantics)
        for arm in ARMS:
            results.append(execute(arm, case, semantics, client, output, customer_prompt))
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        client.close()
        after = protected()
        save(output / 'protected_verification.json', {'unchanged': before == after, 'files': len(before),
             'changed_paths': [p for p in before.keys() | after.keys() if before.get(p) != after.get(p)]})
        save(output / 'results.json', results)
        save(output / 'run_status.json', {'complete': len(results) == 2 and error is None,
             'error': error, 'calls': len(client.rows)})
    print(output, flush=True)
    if error:
        raise SystemExit(error)
    assert before == after


if __name__ == '__main__':
    main()
