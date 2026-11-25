"""Add only an unknown-stock adjacent state; reuse frozen common policy."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
from engine import Case
import baseline_runner as base
from exchange_core import packed

HERE = Path(__file__).resolve().parent
KNOWN = HERE.parent / '04_同状态候选续行/results/20261120T041352631194Z'
ORIGINAL_WORK = base.work


def adjacent_fixture(known_fixture, initial_semantics):
    result = deepcopy(known_fixture)
    iid = initial_semantics['item_id']
    order_item = next(item for item in base.read(KNOWN / 'initial_database.json')['orders'][result['order_id']]['items'] if item['item_id'] == iid)
    pid = order_item['product_id']
    hard, preferred = initial_semantics['hard_options'], initial_semantics['preferred_options']
    interventions = []
    pending = {}
    for index, message in enumerate(result['shared_history']):
        for tc in message.get('tool_calls', []):
            pending[tc['id']] = tc['function']
        if message['role'] != 'tool':
            continue
        function = pending[message['tool_call_id']]
        if function['name'] != 'get_product_details' or json.loads(function['arguments'])['product_id'] != pid:
            continue
        observed = json.loads(message['content'])
        for vid, variant in observed['variants'].items():
            hard_match = all(variant['options'].get(k) == value for k, value in hard.items())
            preferred_match = all(variant['options'].get(k) == value for k, value in preferred.items())
            if hard_match and not preferred_match and variant['available'] is True:
                variant['available'] = None
                interventions.append({'message_index': index, 'product_id': pid, 'variant_id': vid,
                                      'field': 'available', 'before': True, 'after': None})
        message['content'] = json.dumps(observed, ensure_ascii=False)
    if len(interventions) != 1:
        raise ValueError('expected exactly one relevant available-alternative stock observation to mask')
    # This is an explicitly controlled observation view, not a claimed real tool response.
    return result, {'type': 'epistemic_intervention', 'changes': interventions,
                    'database_changed': False,
                    'construction': 'Mask one availability observation consistently before constructing all caches and judgments; metadata/options/prices remain visible. Official query later returns the unmodified database.'}


def work(case, instruction, client, branch, tools, policy):
    if instruction['z']['work_id'] != 'inventory':
        return ORIGINAL_WORK(case, instruction, client, branch, tools, policy)
    candidate = case.validate_instruction(instruction)
    before = case.state()
    wall, cpu = time.perf_counter(), time.process_time()
    result = case.deterministic(instruction, tools)
    case.history.append({'role': 'observation', 'work': 'inventory', 'content': packed(result)})
    case.core.evidence[str(len(case.history) - 1)] = deepcopy(case.history[-1])
    entry = {'u': deepcopy(instruction), 'before': before, 'executor_instruction': deepcopy(instruction),
             'result': result, 'completion_test': candidate['completion_test'],
             'completion_satisfied': case.completed(candidate['completion_test']),
             'work_wall_seconds_including_model_and_customer_io': time.perf_counter() - wall,
             'local_process_cpu_seconds_including_transport': time.process_time() - cpu}
    case.steps += 1
    case.remaining_budget['work_steps'] -= 1
    case.work.append({'work_id': 'inventory', 'completion_satisfied': entry['completion_satisfied'], 'step': case.steps})
    entry['after'] = case.state()
    return entry


# One executor wrapper extends the old capability set only for actual missing inventory.
# Known-state execution and all LLM prompts remain byte-for-byte compatible.
base.work = work
base.Case = Case


def load_anchor():
    meta = base.read(KNOWN / 'metadata.json')
    for key, actual in (('controller_prompt', base.CONTROLLER), ('worker_prompt', base.WORKER),
                        ('user_policy', base.USER_POLICY), ('user_prompt', base.USER_PROMPT),
                        ('user_semantics_prompt', base.USER_SEMANTICS), ('judge_prompt', base.JUDGE),
                        ('parameters_prompt', base.PARAMETERS)):
        if meta[key] != actual:
            raise ValueError('frozen common policy changed: ' + key)
    if base.sha(base.DATA / 'db.json') != meta['official_database_sha256'] or base.sha(base.DATA / 'policy.md') != meta['official_policy_sha256']:
        raise ValueError('official world or rules changed since known-state anchor')
    return meta, base.read(KNOWN / 'fixture.json'), base.read(KNOWN / 'initial_semantics.json'), base.read(KNOWN / 'initial_database.json')


def compare(output, results):
    anchor = base.read(KNOWN / 'V_observations.json')
    current = base.read(output / 'V_observations.json')
    known = {row['branch']: row for row in anchor['V']}
    unknown = {row['branch']: row for row in current['V']}
    if len(unknown) != 2:
        return
    k_delta = known['screen_first']['c_agent']['total_tokens'] - known['clarify_first']['c_agent']['total_tokens']
    u_delta = unknown['inventory_first']['c_agent']['total_tokens'] - unknown['clarify_first']['c_agent']['total_tokens']
    equal_observed_quality = all(row['observed_success'] is True and row['observed_constraints'] is True
                                 for row in list(known.values()) + list(unknown.values()))
    report = {'known_state_source': str(KNOWN), 'known_state': anchor, 'unknown_state': current,
              'all_cells_pass_observed_task_and_constraint_checks': equal_observed_quality,
              'token_difference_evidence_first_minus_clarify_first': {'known': k_delta, 'unknown': u_delta,
                                                                  'difference_of_observed_differences': u_delta - k_delta},
              'caution': 'One observation per state/action. Evidence-first is cached screening in known state, real acquisition in unknown state. This tests a state-dependent work family, not the identical low-level action or a statistically estimated interaction.'}
    base.save(output / 'adjacent_comparison.json', report)
    lines = ['# 一个相邻库存证据状态的续行比较', '',
             '|状态|首步|任务观察|步数|Agent 调用|Agent token|', '|---|---|---:|---:|---:|---:|']
    for label, rows in [('已有库存证据（旧锚点）', known), ('替代品库存未知（新增）', unknown)]:
        for name, row in rows.items():
            success = '?' if row['observed_success'] is None else int(row['observed_success'])
            first = {'screen_first': '先整理缓存', 'inventory_first': '先查库存', 'clarify_first': '先问接受范围'}[name]
            lines.append(f'|{label}|{first}|{success}/1|{row["q_process"]["steps"]}|{row["c_agent"]["calls"]}|{row["c_agent"]["total_tokens"]}|')
    lines += ['', f'“库存依据优先 − 先澄清”的 Agent token 差：已知状态 {k_delta:+d}，未知状态 {u_delta:+d}。',
              f'各格是否都通过本次目标/约束检查：{equal_observed_quality}。如未通过，不按 token 差直接判定首步优劣。',
              '以上仅为本次观察差，不是期望收益、显著性或稳定首步偏好。用户模拟、外部评测不计入 Agent。',
              '旧锚点不重新采样；新增状态仅两个分支。共同策略在旧已知状态下通过原始请求精确回放验证兼容。',
              '环境数据库、用户目标和私有规则相同；仅一个可用替代品的公开库存观察变为未知，实际库存未改。',
              '两个状态下“库存依据优先”的底层工作不同：已知时是程序整理，未知时是官方查询。不能冒称同一个低层动作的严格交互检验。']
    (output / 'adjacent_summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    from checks import offline
    old_meta, fixture, semantics, database = load_anchor()
    adjacent, intervention = adjacent_fixture(fixture, semantics)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = HERE / ('selfcheck' if args.check else 'results') / stamp
    output.mkdir(parents=True)
    base.save(output / 'offline_check.json', offline(fixture, adjacent, intervention, semantics, database, output))
    print('Adjacent-state offline acceptance passed; no new model calls in checks.', flush=True)
    original = base.protected()
    base.save(output / 'protected_before.json', original)
    base.save(output / 'fixture.json', adjacent)
    base.save(output / 'intervention.json', intervention)
    base.save(output / 'initial_semantics.json', semantics)
    base.save(output / 'initial_database.json', database)
    if args.check:
        after = base.protected()
        base.save(output / 'protected_verification.json', {'tracked_files_unchanged': all(after.get(p) == h for p, h in original.items()), 'files': len(original)})
        print(output, flush=True)
        return
    snapshot = output / 'snapshot'
    snapshot.mkdir()
    for filename in ('run.py', 'engine.py', 'baseline_runner.py', 'baseline_engine.py', 'exchange_core.py', 'checks.py', 'README.md', 'protocol.md'):
        shutil.copy2(HERE / filename, snapshot / filename)
    shutil.copy2(base.ROOT / 'exp2layer/llm.py', snapshot / 'llm.py')
    shutil.copy2(base.DATA / 'policy.md', snapshot / 'official_policy.md')
    metadata = deepcopy(old_meta)
    metadata.update(task_count=1, added_states=1, forced_first=['inventory', 'clarify'],
        known_anchor=str(KNOWN), known_anchor_metadata_sha256=base.sha(KNOWN / 'metadata.json'),
        snapshot_sha256={p.name: base.sha(p) for p in snapshot.iterdir()},
        intervention=intervention, reused_requests_from=str(KNOWN),
        status='one added epistemic neighbor, two local rollouts; no new framework arms')
    base.save(output / 'metadata.json', metadata)
    client = base.Client(output, reuse_from=KNOWN)
    results, error = [], None
    try:
        # Same original semantic input, before the inventory intervention is relevant.
        actual_semantics = client.ask('shared_prefix', 'agent', 'initial_semantics', [
            {'role': 'system', 'content': base.SEMANTIC_CHANGE},
            {'role': 'user', 'content': packed({'old_plan': fixture['approved_prefix']['old_plan'],
             'new_user_message': base.CHANGE, 'order_items': database['orders'][fixture['order_id']]['items']})}], max_tokens=700)
        assert actual_semantics == semantics
        initial = Case(adjacent, semantics)
        frozen = initial.snapshot(database, base.USER_POLICY)
        base.save(output / 'decision_snapshot.json', frozen)
        base.save(output / 'W_at_fork.json', initial.candidates())
        assert {w['work_id'] for w in initial.candidates() if w['ready']} == {'inventory', 'clarify'}
        for wid in ('inventory', 'clarify'):
            first = next(w for w in initial.candidates() if w['work_id'] == wid)
            result = base.rollout(wid + '_first', initial, database, first, client, output,
                                  (base.DATA / 'policy.md').read_text(encoding='utf-8'))
            assert result['start_snapshot_sha256'] == base.hash_value(frozen)
            results.append(result)
            base.summarize(output, results, client.rows)
        assert base.hash_value(initial.snapshot(database, base.USER_POLICY)) == base.hash_value(frozen)
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        client.close()
        after = base.protected()
        modified = [p for p in original if after.get(p) != original[p]]
        base.save(output / 'protected_verification.json', {'tracked_files_unchanged': not modified,
            'files': len(original), 'modified_or_removed_paths': modified, 'new_paths_observed': sorted(set(after) - set(original))})
        base.save(output / 'results.json', results)
        base.save(output / 'run_status.json', {'protocol_finished': len(results) == 2 and error is None,
            'error': error, 'branch_errors': {r['branch']: r['error'] for r in results}, 'model_calls': len(client.rows)})
        base.summarize(output, results, client.rows)
        compare(output, results)
    print(output, flush=True)
    if error:
        raise SystemExit(error)
    assert not modified


if __name__ == '__main__':
    main()
