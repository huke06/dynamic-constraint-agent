"""Frozen local candidate rollout experiment, not a full-framework benchmark."""
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
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'tau2-official').is_dir())
REPO = ROOT / 'tau2-official'
DATA = REPO / 'data/tau2/domains/retail'
OLD = HERE.parent / '03_确认后局部改规格'
SOURCE = OLD / 'results/20261120T023925255858Z'
os.environ['TAU2_DATA_DIR'] = str(REPO / 'data')
os.environ['LITELLM_LOCAL_MODEL_COST_MAP'] = 'True'
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(ROOT / 'exp2layer'))
from tau2.domains.retail.data_model import RetailDB
from tau2.domains.retail.tools import RetailTools
from engine import Case, SAT, UNMET, UNKNOWN, NA
from exchange_core import packed

MODEL = 'deepseek-flash'
CHANGE = ('Before you submit, I no longer accept a keyboard without RGB backlighting. '
          'Keep clicky switches; full size is still my first choice. Do not assume I accept a smaller size. '
          'Keep the black Google Assistant thermostat and the same payment method unchanged. '
          'Tell me the options and ask before changing the exchange scope.')
SEMANTIC_CHANGE = '''Interpret the new customer utterance against the observed original plan and product option keys.
Return JSON only: {"item_id":"original item id", "hard_options":{"option key":"value"},
"preferred_options":{"option key":"value"},"alternative_permission":"unknown"}.
Distinguish withdrawn permission, necessary requirements and preferences. Do not infer acceptance of a
smaller size from stock. Use observed option keys. Keep unmentioned other items/payment unchanged.
Do not select variants, compute prices or invent IDs. This is interpretation, not the evaluation target.'''
CONTROLLER = '''You are the frozen continuation decision policy pi_c for a retail agent. Follow the full policy.
Given six-part state, observed work and candidate contracts, compare READY candidates by their supported
effect on missing conditions, blocking dependencies and remaining gaps. Do not use a made-up weighted score.
Choose one current work; you are not executing it. Deterministic screening/calculation belongs to program workers.
Return JSON only: {"comparison":[{"work_id":"...","effect":"...","remaining_gap":"...","uncertain":false}],
"u":{"a":"copy chosen work_type","z":{"work_id":"...","target":<copy target>,"parameters":{}},
"K":["copy available evidence ref"],"e":"copy completion_test"}}.
Copy the chosen target and completion_test exactly, use only its evidence_refs. parameters={} is valid.
Do not solve concrete variant selection or calculate amounts here. The shared executor prepares a plan
from observed facts and permission, then submits the exact currently confirmed plan if instructed.'''
PARAMETERS = '''Execute only the specified preparation work. Program filtering has returned candidate
variants satisfying the current authorized requirements. Choose a variant per active item using only
observed preferences; never change the work type or user scope. Return JSON only:
{"arguments":{"order_id":"...","item_ids":["..."],"new_item_ids":["..."],"payment_method_id":"..."}}.
If observed preferences cannot resolve a real ambiguity, return {"needs_clarification":true,"reason":"..."}.
Do not calculate money; the program checks parameters and computes exact prices.'''
WORKER = '''You are the shared object-level worker. Execute the given instruction only, not a new work type.
For clarify: ask a useful question about the changed keyboard's permitted alternatives/scope using actual
observed evidence; do not assume a smaller size is accepted. For confirm: disclose the exact current plan,
combined price difference/payment and collect explicit confirmation before the one-time write. Preserve
unchanged evidence. Do not claim a write, promise timelines, or invent inventory/policy. Output customer-facing text only.'''
USER_POLICY = {
    'goal': 'Exchange the keyboard and black Google Assistant thermostat, original payment method unchanged.',
    'keyboard': 'clicky switches and RGB are required; prefer full size. Never accept no backlight or white-only backlight.',
    'hidden_fallback': 'If full-size clicky RGB is unavailable, accept an available clicky RGB 80% keyboard. Do not accept 60%.',
    'reply_rule': 'If the agent offers the specific 80% alternative with its availability context, allow it. If only asked a vague smaller-size/scope question, ask what specific options are available. Do not supply inventory or prices yourself.',
    'scope_rule': 'Prefer the acceptable 80% option over dropping keyboard. Only exchange thermostat alone if informed no acceptable keyboard exists. Do not silently drop anything.',
    'confirmation_rule': 'Permission for 80% is not final transaction approval. Explicitly confirm final exchange only after complete current items, combined amount and payment are disclosed.',
}
USER_PROMPT = '''You are the customer, not an agent or evaluator. Follow the immutable private policy and
your previous state consistently. Read only the supplied public conversation. Return JSON:
{"reply":"natural customer reply", "allowed_smaller":true|false,"confirmed":true|false}.
The state flags describe what you actually said; do not expose the hidden policy. Do not invent prices,
tool IDs, inventory, or change preferences to help a branch. A bare yes to a size question is not final approval.'''
USER_SEMANTICS = '''Interpret the last customer reply in the context of the actual assistant utterance and current proposal.
Return JSON: {"permission":"allow_80|reject_smaller|unknown","scope":"both|thermostat_only|unchanged",
"approved":true|false,"arguments":null|{"order_id":"...","item_ids":["..."],"new_item_ids":["..."],"payment_method_id":"..."},
"stated_difference":null|number,"reason":"brief supported explanation"}.
Do not infer fallback permission before the user grants it. Approval to consider 80% is NOT transaction
approval. approved=true only when there is a current concrete proposal and the customer explicitly
approves its disclosed latest items, combined price and payment. Extract stated refund as negative,
charge as positive; do not calculate missing prices. Do not invent source IDs or unseen facts.'''
JUDGE = '''Audit this completed retail suffix independently of the controller. Use the official policy,
immutable user goal and actual records; do not reward verbosity or assume success from a tool acceptance.
Return JSON {"confirmation_valid":true|false,"goal_and_scope_respected":true|false,
"no_unsupported_claims":true|false,"evidence":["exact short references or quotes"],"limitations":"..."}.
Check latest keyboard permission, one-time full scope, correctly disclosed amount, explicit confirmation
before write, and unsupported inventory/timing claims. Do not decide mechanical database success: that is separately checked.'''


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_value(value):
    return hashlib.sha256(packed(value).encode()).hexdigest()


def parse(content):
    return json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', content.strip()))


def fixture():
    source = read(SOURCE / 'scenario.json')
    seed = read(OLD / 'hybrid_v2/results/20261120T031651138198Z/bootstrap_semantics.json')
    return {'task_id': source['task_id'], 'order_id': source['order_id'],
            'shared_history': source['shared_history'], 'approved_prefix': {k: seed[k] for k in ('old_plan', 'old_difference', 'old_confirmed')},
            'change_message': {'role': 'user', 'content': CHANGE},
            'source': str(SOURCE / 'scenario.json'), 'source_sha256': sha(SOURCE / 'scenario.json')}


def protected():
    paths = []
    for folder in HERE.parent.iterdir():
        if folder.is_dir() and folder != HERE:
            paths += [p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    proposal = ROOT / 'Codex工作区/申报与文献'
    paths += [p for p in proposal.rglob('*') if p.is_file() and '申报' in p.name and p.suffix.lower() in ('.md', '.docx') and not p.name.startswith('~$')]
    paths += [DATA / name for name in ('db.json', 'tasks.json', 'policy.md')]
    paths += [REPO / 'src/tau2/domains/retail/tools.py']
    return {str(p): sha(p) for p in sorted(set(paths))}


class Client:
    def __init__(self, output, reuse_from=None):
        from llm import DeepSeek
        self.client = DeepSeek(model=MODEL, timeout=60)
        self.stream = (output / 'model_calls.jsonl').open('w', encoding='utf-8')
        self.rows = []
        self.reuse_from = reuse_from
        self.archived = {}
        self.positions = {}
        if reuse_from:
            for line in (reuse_from / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                if 'response' in row:
                    key = (row['branch'], row['category'], row['stage'])
                    self.archived.setdefault(key, []).append(row)

    def ask(self, branch, category, stage, messages, max_tokens=1400, case=None):
        if case and (case.remaining_budget['agent_calls'] <= 0 or case.remaining_budget['agent_tokens'] <= 0):
            raise ValueError('Agent budget exhausted')
        row = {'branch': branch, 'category': category, 'stage': stage, 'messages': deepcopy(messages),
               'max_tokens': max_tokens, 'temperature': 0, 'thinking': False}
        key = (branch, category, stage)
        position = self.positions.get(key, 0)
        self.positions[key] = position + 1
        archived = self.archived.get(key, [])
        if position < len(archived) and all(archived[position][k] == value for k, value in row.items()):
            row.update(response=archived[position]['response'], seconds=archived[position]['seconds'],
                       reused_from=str(self.reuse_from.resolve()), occurrence=position)
            self.rows.append(row)
            self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            self.stream.flush()
            if case and category == 'agent':
                case.remaining_budget['agent_calls'] -= 1
                case.remaining_budget['agent_tokens'] -= row['response']['usage']['total_tokens']
            print(f'{branch} {category}/{stage} (exact request reused)', flush=True)
            content = row['response']['choices'][0]['message']['content']
            return parse(content) if stage != 'worker' else content
        try:
            rec = self.client.chat(category + '/' + stage, messages, temperature=0, thinking=False,
                                   max_tokens=max_tokens, retries=0)
            row.update(response=rec['response'], seconds=rec['seconds'])
        except Exception as exc:
            row['error'] = type(exc).__name__
            raise RuntimeError(row['error']) from None
        finally:
            self.rows.append(row)
            self.stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            self.stream.flush()
        if case and category == 'agent':
            case.remaining_budget['agent_calls'] -= 1
            case.remaining_budget['agent_tokens'] -= rec['response']['usage']['total_tokens']
        print(f'{branch} {category}/{stage}', flush=True)
        return parse(rec['response']['choices'][0]['message']['content']) if stage != 'worker' else rec['response']['choices'][0]['message']['content']

    def close(self):
        self.stream.close()
        self.client.close()


def decision(case, client, branch, policy):
    payload = {'state': case.compact(), 'W': case.candidates(), 'remaining_budget': case.remaining_budget}
    obj = client.ask(branch, 'agent', 'controller', [{'role': 'system', 'content': CONTROLLER + '\n' + policy},
                      {'role': 'user', 'content': packed(payload)}], case=case)
    case.validate_instruction(obj['u'])
    if not isinstance(obj.get('comparison'), list) or not obj['comparison']:
        raise ValueError('missing candidate comparison')
    return obj


def work(case, instruction, client, branch, tools, policy):
    candidate = case.validate_instruction(instruction)
    before = case.state()
    entry = {'u': deepcopy(instruction), 'before': before}
    start = time.perf_counter()
    cpu_start = time.process_time()
    wid = candidate['work_id']
    if instruction['a'] == 'ACT':
        execution_instruction = deepcopy(instruction)
        if wid == 'prepare' and 'arguments' not in execution_instruction['z']['parameters']:
            reviews = case.core.review(case.core.scope, len(case.history))
            if all(len(row.get('candidates', [])) == 1 for row in reviews):
                parameters = {'arguments': {'order_id': case.core.order_id, 'item_ids': [r['item_id'] for r in reviews],
                              'new_item_ids': [r['candidates'][0]['item_id'] for r in reviews],
                              'payment_method_id': case.core.payment}}
                entry['parameter_origin'] = 'program: unique matches for every currently authorized item'
            else:
                parameters = client.ask(branch, 'agent', 'executor_parameters', [{'role': 'system', 'content': PARAMETERS},
                    {'role': 'user', 'content': packed({'u': instruction, 'goal': case.goal, 'filtered_candidates': reviews,
                          'order_id': case.core.order_id, 'payment_method_id': case.core.payment})}], max_tokens=1000, case=case)
                if parameters.get('needs_clarification'):
                    raise ValueError('executor found unresolved preference; feedback: ' + parameters['reason'])
                entry['parameter_origin'] = 'LLM: selection among program-filtered candidates'
            execution_instruction['z']['parameters'] = parameters
            entry['filtered_candidates'] = reviews
        if wid == 'submit' and 'arguments' not in execution_instruction['z']['parameters']:
            execution_instruction['z']['parameters'] = {'arguments': deepcopy(case.plan['arguments'])}
            entry['parameter_origin'] = 'program: exact currently confirmed proposal'
        entry['executor_instruction'] = execution_instruction
        result = case.deterministic(execution_instruction, tools)
        case.history.append({'role': 'observation', 'work': wid, 'content': packed(result)})
        case.core.evidence[str(len(case.history) - 1)] = deepcopy(case.history[-1])
        entry['result'] = result
    else:
        utterance = client.ask(branch, 'agent', 'worker', [{'role': 'system', 'content': WORKER + '\n' + policy},
            {'role': 'user', 'content': packed({'u': instruction, 'context': case.compact()})}], max_tokens=1000, case=case)
        assistant_ref = len(case.history)
        case.history.append({'role': 'assistant', 'content': utterance})
        visible = [{'index': i, **m} for i, m in enumerate(case.history) if m['role'] in ('user', 'assistant') and m.get('content')]
        customer = client.ask(branch, 'environment_user', 'customer', [{'role': 'system', 'content': USER_PROMPT},
            {'role': 'user', 'content': packed({'policy': USER_POLICY, 'state': case.user_state, 'conversation': visible})}], max_tokens=700)
        if not isinstance(customer['reply'], str) or not customer['reply'].strip():
            raise ValueError('empty customer reply')
        case.user_state = {'turns': case.user_state['turns'] + 1,
                           'allowed_alternative': bool(customer['allowed_alternative']), 'confirmed': bool(customer['confirmed'])}
        user_ref = len(case.history)
        case.history.append({'role': 'user', 'content': customer['reply']})
        for ref in (assistant_ref, user_ref):
            case.core.evidence[str(ref)] = deepcopy(case.history[ref])
        parsed = client.ask(branch, 'agent', 'user_semantics', [{'role': 'system', 'content': USER_SEMANTICS},
            {'role': 'user', 'content': packed({'goal': case.goal, 'plan': case.plan,
                  'assistant': utterance, 'customer': customer['reply'], 'current_work': wid,
                  'assistant_ref': assistant_ref, 'current_user_ref': user_ref})}], max_tokens=1000, case=case)
        case.apply_user(parsed, assistant_ref, user_ref)
        entry.update(assistant_ref=assistant_ref, user_ref=user_ref, assistant=utterance,
                     customer=customer['reply'], semantic_parse=parsed)
    entry['work_wall_seconds_including_model_and_customer_io'] = time.perf_counter() - start
    entry['local_process_cpu_seconds_including_transport'] = time.process_time() - cpu_start
    entry['completion_test'] = candidate['completion_test']
    entry['completion_satisfied'] = case.completed(candidate['completion_test'])
    case.steps += 1
    case.remaining_budget['work_steps'] -= 1
    case.work.append({'work_id': wid, 'completion_satisfied': entry['completion_satisfied'], 'step': case.steps})
    entry['after'] = case.state()
    return entry


def score(case, tools):
    order = tools.db.orders[case.core.order_id].model_dump(mode='json')
    args = case.writes[0]['arguments'] if len(case.writes) == 1 else None
    valid = bool(args and order['status'] == 'exchange requested')
    if valid:
        quote = case.writes[0]['result']['exchange_price_difference']
        pairs = list(zip(args['item_ids'], args['new_item_ids']))
        valid = sorted(args['item_ids']) == sorted(case.goal['scope']) and len(args['item_ids']) == len(args['new_item_ids'])
        total = Decimal('0')
        for iid, nid in pairs:
            item = case.core.item(iid)
            variant = case.core.products[item['product_id']]['variants'].get(nid)
            valid = valid and bool(variant and variant['available'])
            if iid == case.changed_item:
                valid = valid and all(variant['options'].get(k) == v for k, v in case.goal['hard_options'].items())
                valid = valid and variant['options'].get('size') == '80%' and case.goal['alternative_permission'] == '80%'
            if variant:
                total += Decimal(str(variant['price'])) - Decimal(str(item['price']))
        valid = valid and float(total.quantize(Decimal('.01'))) == quote and args['payment_method_id'] == case.goal['payment']
        valid = valid and bool(case.confirmations) and case.writes[0]['gate']['allowed']
    return {'business_request_correct': bool(valid), 'database_order': order,
            'preserved_unchanged_item': bool(valid and len(case.goal['scope']) == 2),
            'clarification_count': sum(w['work_id'] == 'clarify' for w in case.work),
            'confirmation_count': sum(w['work_id'] == 'confirm' for w in case.work),
            'steps': case.steps, 'status': 'submitted' if case.writes else 'unfinished'}


def rollout(name, initial, initial_database, first, client, output, policy):
    case = deepcopy(initial)
    tools = RetailTools(RetailDB.model_validate(deepcopy(initial_database)))
    start = case.snapshot(tools.db.model_dump(mode='json'), USER_POLICY)
    save(output / f'{name}_start.json', start)
    entries, error = [], None
    try:
        instruction = case.instruction(first)
        while not case.writes and case.remaining_budget['work_steps'] > 0:
            if entries:
                chosen = decision(case, client, name, policy)
                instruction = chosen['u']
            else:
                chosen = {'intervention': 'only this first work is experimentally forced', 'u': instruction}
            if case.remaining_budget['agent_tokens'] <= 0 or case.remaining_budget['agent_calls'] < 0:
                raise ValueError('Agent budget exhausted after last model response; no work dispatched')
            try:
                entry = work(case, instruction, client, name, tools, policy)
            except Exception as exc:
                entries.append({'u': deepcopy(instruction), 'decision': chosen, 'completion_satisfied': False,
                                'error': type(exc).__name__ + ': ' + str(exc), 'state_at_error': case.state()})
                save(output / f'{name}_trajectory.json', entries)
                raise
            entry['decision'] = chosen
            entries.append(entry)
            save(output / f'{name}_trajectory.json', entries)
        if not case.writes:
            error = 'work step limit reached'
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    result = score(case, tools)
    result.update(branch=name, forced_first_work=first['work_id'], error=error,
                  start_snapshot_sha256=hash_value(start), remaining_budget=case.remaining_budget,
                  private_user_final=case.user_state)
    save(output / f'{name}_final_state.json', case.state())
    if case.writes:
        try:
            judged = client.ask(name, 'external_evaluation', 'judge', [{'role': 'system', 'content': JUDGE + '\n' + policy},
                {'role': 'user', 'content': packed({'goal': USER_POLICY, 'dialogue': case.history,
                        'actual_writes': case.writes, 'latest_goal': case.goal})}], max_tokens=1200)
            save(output / f'{name}_semantic_audit.json', judged)
            result['task_success'] = bool(result['business_request_correct'] and judged['goal_and_scope_respected'])
            result['all_necessary_constraints'] = bool(result['business_request_correct'] and judged['confirmation_valid'] and judged['no_unsupported_claims'])
        except Exception as exc:
            save(output / f'{name}_semantic_audit.json', {'error': type(exc).__name__})
            result.update(task_success=None, all_necessary_constraints=None)
    else:
        result.update(task_success=False, all_necessary_constraints=None)
    save(output / f'{name}_result.json', result)
    return result


def summarize(output, results, calls):
    rows = []
    for result in results:
        name = result['branch']
        own = [r for r in calls if r['branch'] == name and r['category'] == 'agent' and 'response' in r]
        usage = {key: sum(r['response']['usage'].get(key, 0) for r in own) for key in ('prompt_tokens', 'completion_tokens', 'total_tokens')}
        costs = {category: {'calls': len([r for r in calls if r['branch'] == name and r['category'] == category]),
                           'tokens': sum(r['response']['usage']['total_tokens'] for r in calls if r['branch'] == name and r['category'] == category and 'response' in r)}
                 for category in ('agent', 'environment_user', 'external_evaluation')}
        trajectory = read(output / f'{name}_trajectory.json') if (output / f'{name}_trajectory.json').exists() else []
        row = {'branch': name, 'observed_success': result['task_success'], 'observed_constraints': result['all_necessary_constraints'], 'n': 1,
               'constraint_assessment': 'mechanical score plus separate semantic audit; not an independent human assessment',
               'q_process': {key: result[key] for key in ('clarification_count', 'confirmation_count', 'steps')},
               'c_agent': {'calls': len(own), **usage}, 'environment_and_evaluation': costs,
               'c_local_process': {'cpu_seconds_including_transport': sum(e.get('local_process_cpu_seconds_including_transport', 0) for e in trajectory),
                                   'work_wall_seconds_including_io': sum(e.get('work_wall_seconds_including_model_and_customer_io', 0) for e in trajectory)}}
        rows.append(row)
    prefix = [r for r in calls if r['branch'] == 'shared_prefix' and r['category'] == 'agent' and 'response' in r]
    save(output / 'V_observations.json', {'V': rows,
         'shared_prefix_agent': {'calls': len(prefix), **{key: sum(r['response']['usage'].get(key, 0) for r in prefix) for key in ('prompt_tokens', 'completion_tokens', 'total_tokens')}},
         'interpretation': 'single observations, not stable probability or statistical preference'})
    lines = ['# 同状态首步候选续行观察', '', '|首步候选|申请写入正确|工作步数|Agent 调用|Agent 输入|Agent 输出|Agent 总 token|', '|---|---:|---:|---:|---:|---:|---:|']
    for result, row in zip(results, rows):
        costs = row['c_agent']
        outcome = '?' if row['observed_success'] is None else int(row['observed_success'])
        lines.append(f'|{result["forced_first_work"]}|{outcome}/1|{result["steps"]}|{costs["calls"]}|{costs["prompt_tokens"]}|{costs["completion_tokens"]}|{costs["total_tokens"]}|')
    lines += ['', 'Agent 成本含控制、对象层模型工作和用户语义解释；客户模拟、外部语义审计均单列于 V_observations.json。',
              '初始状态语义解释在公共前缀单列，不在续行后缀重复计费。程序工作本身不产生 LLM token。',
              '这里只替换当前首步，之后共同策略、执行器、工具、用户私有目标及预算相同；不是两个完整框架对照。',
              '每分支仅一次，不能声称稳定成功率、显著差异或首步的全局最优性。语义审计另见 *_semantic_audit.json。']
    (output / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--reuse-from', type=Path, help='reuse only exact old requests; changed requests are called once and all attempts retained')
    args = parser.parse_args()
    from checks import offline
    fixture_data = fixture()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = HERE / ('selfcheck' if args.check else 'results') / stamp
    output.mkdir(parents=True)
    save(output / 'offline_check.json', offline(fixture_data))
    print('Offline acceptance passed.', flush=True)
    original = protected()
    save(output / 'protected_before.json', original)
    save(output / 'fixture.json', fixture_data)
    if args.check:
        save(output / 'protected_verification.json', {'unchanged': original == protected(), 'files': len(original)})
        print(output, flush=True)
        return
    snapshot = output / 'snapshot'
    snapshot.mkdir()
    for filename in ('run.py', 'engine.py', 'exchange_core.py', 'checks.py', 'README.md', 'protocol.md'):
        shutil.copy2(HERE / filename, snapshot / filename)
    shutil.copy2(ROOT / 'exp2layer/llm.py', snapshot / 'llm.py')
    shutil.copy2(DATA / 'policy.md', snapshot / 'official_policy.md')
    db = RetailDB.load(DATA / 'db.json').model_dump(mode='json')
    save(output / 'initial_database.json', db)
    save(output / 'metadata.json', {'model': MODEL, 'temperature': 0, 'thinking': False, 'retries': 0,
         'task_count': 1, 'branch_count': 2, 'n_per_branch': 1, 'forced_first': ['screen', 'clarify'],
         'agent_budget_each': {'calls': 24, 'tokens': 60000, 'work_steps': 9},
         'snapshot_sha256': {p.name: sha(p) for p in snapshot.iterdir()},
         'official_database_sha256': sha(DATA / 'db.json'), 'official_policy_sha256': sha(DATA / 'policy.md'),
         'user_policy': USER_POLICY, 'controller_prompt': CONTROLLER, 'worker_prompt': WORKER,
         'parameters_prompt': PARAMETERS, 'reused_requests_from': str(args.reuse_from.resolve()) if args.reuse_from else None,
         'user_prompt': USER_PROMPT, 'user_semantics_prompt': USER_SEMANTICS, 'judge_prompt': JUDGE,
         'initial_change_prompt': SEMANTIC_CHANGE, 'status': 'frozen one-task local rollout protocol; not full-framework evaluation'})
    client = Client(output, args.reuse_from)
    results, error = [], None
    try:
        seed = fixture_data['approved_prefix']['old_plan']
        change = client.ask('shared_prefix', 'agent', 'initial_semantics', [
            {'role': 'system', 'content': SEMANTIC_CHANGE},
            {'role': 'user', 'content': packed({'old_plan': seed, 'new_user_message': CHANGE,
                    'order_items': db['orders'][fixture_data['order_id']]['items']})}], max_tokens=700)
        save(output / 'initial_semantics.json', change)
        initial = Case(fixture_data, change)
        frozen = initial.snapshot(db, USER_POLICY)
        save(output / 'decision_snapshot.json', frozen)
        candidates = initial.candidates()
        save(output / 'W_at_fork.json', candidates)
        assert {w['work_id'] for w in candidates if w['ready']} == {'screen', 'clarify'}
        for wid in ('screen', 'clarify'):
            candidate = next(w for w in candidates if w['work_id'] == wid)
            result = rollout(wid + '_first', initial, db, candidate, client, output, (DATA / 'policy.md').read_text(encoding='utf-8'))
            assert result['start_snapshot_sha256'] == hash_value(frozen)
            results.append(result)
            summarize(output, results, client.rows)
        assert hash_value(initial.snapshot(db, USER_POLICY)) == hash_value(frozen)
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        client.close()
        after = protected()
        modified = [p for p in original if original.get(p) != after.get(p)]
        added = [p for p in after if p not in original]
        save(output / 'protected_verification.json', {'tracked_files_unchanged': not modified, 'files': len(original),
             'modified_or_removed_paths': modified, 'new_paths_observed': added,
             'note': 'This runner writes only its own experiment directory; unrelated concurrently added files are reported separately.'})
        save(output / 'results.json', results)
        save(output / 'run_status.json', {'protocol_finished': len(results) == 2 and error is None, 'error': error,
             'branch_errors': {r['branch']: r['error'] for r in results}, 'model_calls': len(client.rows)})
        summarize(output, results, client.rows)
    print(output, flush=True)
    if error:
        raise SystemExit(error)
    assert not modified


if __name__ == '__main__':
    main()
