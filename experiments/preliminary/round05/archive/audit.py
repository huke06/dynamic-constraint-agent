"""No-API replay of the neighbor, leakage checks and classified cost audit."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import run
from checks import Replay, stock_values
from engine import Case
from exchange_core import packed


def untimed(value):
    if isinstance(value, dict):
        return {k: untimed(v) for k, v in value.items() if k not in (
            'local_process_cpu_seconds_including_transport', 'work_wall_seconds_including_model_and_customer_io')}
    if isinstance(value, list):
        return [untimed(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    output = parser.parse_args().result.resolve()
    base = run.base
    meta = base.read(output / 'metadata.json')
    fixture = base.read(output / 'fixture.json')
    semantics = base.read(output / 'initial_semantics.json')
    database = base.read(output / 'initial_database.json')
    rows = [json.loads(line) for line in (output / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    for name, digest in meta['snapshot_sha256'].items():
        assert base.sha(output / 'snapshot' / name) == digest
    for name in ('run.py', 'engine.py', 'checks.py', 'baseline_runner.py', 'baseline_engine.py', 'exchange_core.py'):
        assert base.sha(run.HERE / name) == meta['snapshot_sha256'][name]
    known_meta, known_fixture, known_semantics, known_database = run.load_anchor()
    assert database == known_database and semantics == known_semantics
    assert meta['user_policy'] == known_meta['user_policy']
    assert meta['snapshot_sha256']['baseline_runner.py'] == known_meta['snapshot_sha256']['run.py']
    assert meta['snapshot_sha256']['baseline_engine.py'] == known_meta['snapshot_sha256']['engine.py']
    assert meta['snapshot_sha256']['exchange_core.py'] == known_meta['snapshot_sha256']['exchange_core.py']
    assert meta['snapshot_sha256']['llm.py'] == known_meta['snapshot_sha256']['llm.py']
    original = base.read(output / 'protected_before.json')
    modified = [path for path, digest in original.items() if not Path(path).exists() or base.sha(Path(path)) != digest]
    assert not modified, modified
    initial = Case(fixture, semantics)
    frozen = initial.snapshot(database, base.USER_POLICY)
    assert frozen == base.read(output / 'decision_snapshot.json')
    intervention = base.read(output / 'intervention.json')
    target = intervention['changes'][0]['variant_id']
    values = stock_values(initial.compact(), target)
    assert values and all(value is None for value in values)
    assert not initial.plan and initial.screen is None
    replay = Replay(rows)
    parsed = replay.ask('shared_prefix', 'agent', 'initial_semantics', [
        {'role': 'system', 'content': base.SEMANTIC_CHANGE},
        {'role': 'user', 'content': packed({'old_plan': known_fixture['approved_prefix']['old_plan'],
             'new_user_message': base.CHANGE, 'order_items': database['orders'][fixture['order_id']]['items']})}], max_tokens=700)
    assert parsed == semantics
    replay_output = output / 'audit_replay'
    replay_output.mkdir(exist_ok=True)
    branch_findings = []
    for wid in ('inventory', 'clarify'):
        name = wid + '_first'
        assert base.read(output / f'{name}_start.json') == frozen
        first = next(w for w in initial.candidates() if w['work_id'] == wid)
        result = base.rollout(name, initial, database, first, replay, replay_output,
                              (output / 'snapshot/official_policy.md').read_text(encoding='utf-8'))
        assert json.loads(packed(result)) == base.read(output / f'{name}_result.json')
        expected = base.read(output / f'{name}_trajectory.json')
        actual = base.read(replay_output / f'{name}_trajectory.json')
        assert untimed(actual) == untimed(expected)
        queries = [e for e in expected if e['u']['z']['work_id'] == 'inventory']
        assert len(queries) == 1
        query = queries[0]
        assert query['result']['official_result']['variants'][target]['available'] is True
        assert all(value is None for value in stock_values(query['before']['F']['catalog'], target))
        assert all(value is True for value in stock_values(query['after']['F']['catalog'], target))
        if name == 'clarify_first' and 'conditional_permission' in query['before']['g']:
            assert query['before']['g']['conditional_permission']['sat'] == '未知'
            assert query['after']['g']['conditional_permission']['sat'] == '满足'
            assert query['after']['g']['alternative_permission'] == '80%'
            assert query['after']['C']['authorization_current']['sat'] != '满足'
        branch_findings.append({'branch': name, 'exact_model_and_program_replay': True,
             'one_official_query': True, 'query_changes_evidence_not_world': True,
             'task_success': result['task_success'], 'constraints_model_check': result['all_necessary_constraints'],
             'all_work_completions_met': all(e['completion_satisfied'] for e in expected)})
    assert replay.index == len(rows)
    assert base.hash_value(initial.snapshot(database, base.USER_POLICY)) == base.hash_value(frozen)
    for row in rows:
        if row['category'] == 'agent':
            assert 'hidden_fallback' not in packed(row['messages']) and 'confirmation_rule' not in packed(row['messages'])
        if row.get('reused_from'):
            archived = [json.loads(line) for line in (Path(row['reused_from']) / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
            matches = [r for r in archived if (r['branch'], r['category'], r['stage']) == (row['branch'], row['category'], row['stage'])]
            source = matches[row['occurrence']]
            assert all(row[key] == source[key] for key in ('messages', 'temperature', 'thinking', 'max_tokens', 'response'))
    development = {}
    new_api = {}
    for log in (run.HERE / 'results').glob('*/model_calls.jsonl'):
        for line in log.read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            if 'response' in row:
                development[row['response']['id']] = row
                if not row.get('reused_from'):
                    new_api[row['response']['id']] = row
    costs = {}
    for row in development.values():
        item = costs.setdefault(row['category'], {'unique_responses': 0, 'input_tokens': 0, 'output_tokens': 0})
        item['unique_responses'] += 1
        item['input_tokens'] += row['response']['usage']['prompt_tokens']
        item['output_tokens'] += row['response']['usage']['completion_tokens']
    paid = {}
    for row in new_api.values():
        item = paid.setdefault(row['category'], {'new_api_responses': 0, 'input_tokens': 0, 'output_tokens': 0})
        item['new_api_responses'] += 1
        item['input_tokens'] += row['response']['usage']['prompt_tokens']
        item['output_tokens'] += row['response']['usage']['completion_tokens']
    report = {'status': 'passed', 'one_observation_intervention': intervention,
        'unchanged_world_goals_user_policy_and_budget': True, 'unknown_fork_start_snapshots_identical': True,
        'known_anchor_exact_replay_requests_without_api': base.read(output / 'offline_check.json')['known_anchor_requests_replayed_without_api'],
        'branch_findings': branch_findings, 'protected_files_verified': len(original),
        'reused_responses': sum(bool(r.get('reused_from')) for r in rows),
        'new_api_responses_in_continuation': sum(not r.get('reused_from') for r in rows),
        'development_deduplicated_costs_including_preserved_failure': costs,
        'new_api_usage_originating_in_this_experiment_directory': paid,
        'cost_origin_note': 'Logical response workload includes the inherited 520-token semantic prefix; new API usage excludes responses reused from the old known-state experiment.',
        'model_identifiers': sorted({r['response'].get('model', '') for r in rows}),
        'system_fingerprints': sorted({r['response'].get('system_fingerprint', '') for r in rows}),
        'limitations': ['Single development observation per cell.', 'Conditional semantic adapter was completed after first failed trial; no frozen independent statistical test.',
                       'Screening known evidence and querying missing evidence are state-dependent different low-level work.', 'No independent human annotation.']}
    base.save(output / 'audit.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
