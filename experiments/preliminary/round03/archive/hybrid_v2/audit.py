"""No-API exact replay, evidence checks and token accounting for this one case."""
from copy import deepcopy
import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import run
from ledger import Ledger, packed


class Replay:
    def __init__(self, rows):
        self.rows = {row['kind']: row for row in rows}
        self.used = []

    def ask(self, kind, messages, tool_schemas=None, max_tokens=1200):
        row = self.rows[kind]
        assert row['messages'] == messages, kind + ': messages differ'
        assert row['tools'] == tool_schemas, kind + ': tools differ'
        assert row['max_tokens'] == max_tokens
        self.used.append(kind)
        return deepcopy(row['response']['choices'][0]['message'])


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    output = parser.parse_args().result.resolve()
    meta = run.read(output / 'metadata.json')
    case = run.read(output / 'scenario.json')
    rows = [json.loads(line) for line in (output / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    for name, expected in meta['snapshot_sha256'].items():
        assert run.sha(output / 'snapshot' / name) == expected
    for name in ('run.py', 'ledger.py', 'checks.py'):
        assert run.sha(run.HERE / name) == meta['snapshot_sha256'][name]
    assert run.sha(Path(meta['source_scenario'])) == meta['source_scenario_sha256']
    protected = run.read(output / 'protected_before.json')
    assert all(run.sha(Path(path)) == expected for path, expected in protected.items())
    original_meta = run.read(run.SOURCE / 'metadata.json')
    assert all(run.sha(Path(path)) == expected for path, expected in original_meta['official_source_sha256'].items())
    replay = Replay(rows)
    semantics = run.parse(replay.ask('shared/semantics/bootstrap', [
        {'role': 'system', 'content': run.BOOT},
        {'role': 'user', 'content': packed(run.bootstrap_input(case, Ledger(case['shared_history'])))}], max_tokens=1400)['content'])
    replay_output = output / 'audit_replay'
    replay_output.mkdir(exist_ok=True)
    results, semantic_evidence = [], {}
    for arm in run.ARMS:
        result = run.execute(arm, case, semantics, replay, replay_output, meta['customer_prompt'])
        assert json.loads(packed(result)) == run.read(output / f'{arm}_result.json')
        trajectory = run.read(output / f'{arm}_trajectory.json')
        assert trajectory == run.read(replay_output / f'{arm}_trajectory.json')
        initial = run.read(output / f'{arm}_initial_state.json')['semantic_transition']
        changed = semantics['changes'][0]['item_id']
        preserved = [iid for iid in semantics['old_plan']['item_ids'] if iid != changed]
        assert initial['before']['identity'] == initial['after']['identity']
        for iid in preserved:
            for prefix in ('requirement:', 'match:', 'delta:', 'confirmation:'):
                assert initial['before'][prefix + iid] == initial['after'][prefix + iid]
        assert initial['after']['confirmation:' + changed]['status'] == 'stale'
        assert initial['after']['authorization']['status'] == 'stale'
        accepted = [step for step in trajectory['steps'] if step.get('confirmation_binding', {}).get('accepted')]
        evidence = []
        for step in accepted:
            refs = step['semantic_sources']
            evidence.append({'sources': refs,
                             'assistant_quote': trajectory['history'][refs[0]]['content'],
                             'customer_quote': trajectory['history'][refs[1]]['content'],
                             'raw_semantic_changes': step['semantic_parse']['changes'],
                             'effective_changes': step['effective_semantic_changes']})
        semantic_evidence[arm] = evidence
        results.append({key: result[key] for key in ('arm', 'steps', 'actual_write_correct', 'compliant_completion',
                                                    'write_attempts', 'rejected_write_attempts')})
    assert set(replay.used) == {row['kind'] for row in rows}
    costs, actor_details = {}, []
    actor_schemas = []
    for row in rows:
        group, category = row['kind'].split('/')[:2]
        key = group + '/' + category
        cost = costs.setdefault(key, {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'seconds': 0})
        cost['calls'] += 1
        usage = row['response']['usage']
        for field in ('prompt_tokens', 'completion_tokens'):
            cost[field] += usage.get(field, 0)
        cost['seconds'] += row['seconds']
        assert 'private_evaluation' not in packed(row['messages'])
        if category == 'actor':
            actor_schemas.append(row['tools'])
            actor_details.append({'kind': row['kind'], 'prompt_tokens': usage['prompt_tokens'],
                                  'message_characters': len(packed(row['messages'])),
                                  'message_roles': [m['role'] for m in row['messages']]})
        if row.get('reused_from'):
            archived = [json.loads(line) for line in (Path(row['reused_from']) / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
            source = next(r for r in archived if r['kind'] == row['kind'])
            assert all(row[key] == source[key] for key in ('messages', 'tools', 'temperature', 'thinking', 'max_tokens', 'response'))
    assert all(s == actor_schemas[0] == meta['tools'] for s in actor_schemas)
    # All development attempts remain visible; deduplicate reused provider responses.
    development = {}
    for log in sorted((run.HERE / 'results').glob('*/model_calls.jsonl')):
        for line in log.read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            if 'response' in row:
                development[row['response']['id']] = row['response']['usage']
    report = {'status': 'passed', 'results': results, 'exact_model_request_and_program_replay': True,
              'same_schemas_policy_and_gate_both_arms': True,
              'no_private_target_in_model_requests': True, 'protected_files_unchanged': len(protected),
              'model_costs': costs, 'actor_details': actor_details, 'semantic_evidence': semantic_evidence,
              'state_maintenance_llm_calls_after_tools': 0,
              'reused_responses': sum(bool(row.get('reused_from')) for row in rows),
              'new_api_responses_in_this_continuation': sum(not row.get('reused_from') for row in rows),
              'development_unique_responses_all_attempts': len(development),
              'development_total_tokens_all_attempts': sum(usage['total_tokens'] for usage in development.values()),
              'note': 'Program replay is deterministic verification, not extra model samples. Semantic approval evidence still needs transcript review.'}
    run.save(output / 'audit.json', report)
    print(json.dumps({key: value for key, value in report.items() if key not in ('semantic_evidence', 'actor_details')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
