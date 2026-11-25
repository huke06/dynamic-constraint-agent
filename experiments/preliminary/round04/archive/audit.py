"""No-API exact request/program replay and same-state experiment audit."""
from copy import deepcopy
import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import run
from engine import Case
from exchange_core import packed


class Recorded:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0

    def ask(self, branch, category, stage, messages, max_tokens=1400, case=None):
        row = self.rows[self.index]
        self.index += 1
        assert (row['branch'], row['category'], row['stage']) == (branch, category, stage)
        assert row['messages'] == messages, (branch, stage, 'request differs')
        assert row['max_tokens'] == max_tokens
        if case and category == 'agent':
            case.remaining_budget['agent_calls'] -= 1
            case.remaining_budget['agent_tokens'] -= row['response']['usage']['total_tokens']
        content = row['response']['choices'][0]['message']['content']
        return content if stage == 'worker' else run.parse(content)


def untimed(value):
    if isinstance(value, dict):
        return {key: untimed(v) for key, v in value.items()
                if key not in ('local_process_cpu_seconds_including_transport', 'work_wall_seconds_including_model_and_customer_io')}
    if isinstance(value, list):
        return [untimed(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    output = parser.parse_args().result.resolve()
    meta = run.read(output / 'metadata.json')
    fixture = run.read(output / 'fixture.json')
    database = run.read(output / 'initial_database.json')
    semantics = run.read(output / 'initial_semantics.json')
    rows = [json.loads(line) for line in (output / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    for name, digest in meta['snapshot_sha256'].items():
        assert run.sha(output / 'snapshot' / name) == digest
    for name in ('run.py', 'engine.py', 'exchange_core.py', 'checks.py'):
        assert run.sha(run.HERE / name) == meta['snapshot_sha256'][name]
    original = run.read(output / 'protected_before.json')
    modified = [path for path, digest in original.items() if not Path(path).exists() or run.sha(Path(path)) != digest]
    assert not modified, modified
    initial = Case(fixture, semantics)
    frozen = initial.snapshot(database, run.USER_POLICY)
    assert frozen == run.read(output / 'decision_snapshot.json')
    for name in ('screen_first', 'clarify_first'):
        assert run.read(output / f'{name}_start.json') == frozen
    assert [w['work_id'] for w in initial.candidates() if w['ready']] == ['screen', 'clarify']
    replay = Recorded(rows)
    recorded_semantics = replay.ask('shared_prefix', 'agent', 'initial_semantics', [
        {'role': 'system', 'content': run.SEMANTIC_CHANGE},
        {'role': 'user', 'content': packed({'old_plan': fixture['approved_prefix']['old_plan'],
            'new_user_message': run.CHANGE, 'order_items': database['orders'][fixture['order_id']]['items']})}], max_tokens=700)
    assert recorded_semantics == semantics
    replay_output = output / 'audit_replay'
    replay_output.mkdir(exist_ok=True)
    verdicts = []
    for wid in ('screen', 'clarify'):
        name = wid + '_first'
        first = next(w for w in initial.candidates() if w['work_id'] == wid)
        result = run.rollout(name, initial, database, first, replay, replay_output,
                             (output / 'snapshot/official_policy.md').read_text(encoding='utf-8'))
        assert json.loads(packed(result)) == run.read(output / f'{name}_result.json')
        expected = run.read(output / f'{name}_trajectory.json')
        actual = run.read(replay_output / f'{name}_trajectory.json')
        assert untimed(actual) == untimed(expected), name
        assert expected[0]['u']['z']['work_id'] == wid
        assert expected[0]['decision']['intervention']
        assert all('comparison' in step['decision'] for step in expected[1:])
        assert all(step['completion_satisfied'] for step in expected)
        for step in expected:
            u = step['u']
            assert set(u) == {'a', 'z', 'K', 'e'}
            assert u['a'] in ('ACT', 'ACQUIRE', 'REASON')
        verdicts.append({'branch': name, 'exact_requests_and_effects_replayed': True,
                         'task_success': result['task_success'], 'constraints_model_audit': result['all_necessary_constraints']})
    assert replay.index == len(rows)
    assert run.hash_value(initial.snapshot(database, run.USER_POLICY)) == run.hash_value(frozen)
    for row in rows:
        if row['category'] == 'agent':
            assert 'hidden_fallback' not in packed(row['messages'])
            assert 'confirmation_rule' not in packed(row['messages'])
        if row.get('reused_from'):
            archived = [json.loads(line) for line in (Path(row['reused_from']) / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
            candidates = [r for r in archived if (r['branch'], r['category'], r['stage']) == (row['branch'], row['category'], row['stage'])]
            source = candidates[row['occurrence']]
            assert all(row[key] == source[key] for key in ('messages', 'max_tokens', 'temperature', 'thinking', 'response'))
    development = {}
    for log in (run.HERE / 'results').glob('*/model_calls.jsonl'):
        for line in log.read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            if 'response' in row:
                development[row['response']['id']] = row
    category_totals = {}
    for row in development.values():
        item = category_totals.setdefault(row['category'], {'calls': 0, 'input_tokens': 0, 'output_tokens': 0})
        item['calls'] += 1
        item['input_tokens'] += row['response']['usage']['prompt_tokens']
        item['output_tokens'] += row['response']['usage']['completion_tokens']
    report = {'status': 'passed', 'same_complete_start_snapshot': True, 'frozen_parent_unchanged_by_branches': True,
              'only_first_work_intervened': True, 'common_policy_and_executor_request_replay': True,
              'snapshots_and_tracked_files_verified': len(original), 'branch_verdicts': verdicts,
              'calls': {category: {'count': len([r for r in rows if r['category'] == category]),
                                   'tokens': sum(r['response']['usage']['total_tokens'] for r in rows if r['category'] == category)}
                        for category in ('agent', 'environment_user', 'external_evaluation')},
              'reused_responses': sum(bool(row.get('reused_from')) for row in rows),
              'development_all_attempts_unique_response_costs': category_totals,
              'limitation': 'No independent human impact annotation; semantic judge reference indices are not assumed correct and require transcript review.'}
    run.save(output / 'audit.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
