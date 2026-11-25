"""Replay saved model actions without making API calls; verify frozen evidence."""
import argparse
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    args = parser.parse_args()
    out = args.result.resolve()
    meta = read(out / 'metadata.json')
    for name, expected in meta['snapshot_sha256'].items():
        assert hashlib.sha256((out / 'snapshot' / name).read_bytes()).hexdigest() == expected, name
    source = out / 'snapshot' / 'run.py'
    frozen = {'__file__': str(source), '__name__': 'frozen_audit'}
    exec(compile(source.read_text(encoding='utf-8'), str(source), 'exec'), frozen)
    cases = {c['id']: c for c in read(out / 'snapshot' / 'scenarios.json')}
    episodes = read(out / 'episodes.json')
    traces = [json.loads(line) for line in (out / 'traces.jsonl').read_text(encoding='utf-8').splitlines()]
    assert len({e['episode'] for e in episodes}) == len(episodes) == meta['planned_episodes']
    assert {r['episode'] for r in traces} == {e['episode'] for e in episodes}
    evidence = []
    for episode in episodes:
        env = frozen['Environment'](cases[episode['case']], episode['state'])
        rows = [r for r in traces if r['episode'] == episode['episode']]
        assert [r['step'] for r in rows] == list(range(1, len(rows) + 1))
        for row in rows:
            assert row['messages'] == [
                {'role': 'system', 'content': frozen['SYSTEM']},
                {'role': 'user', 'content': json.dumps(env.payload(episode['arm']), ensure_ascii=False)},
            ]
            assert row['expected'] == env.expected()
            assert row['status'] == 'ok', 'this audit requires a complete successful response log'
            decision = frozen['read_response'](row['response']['choices'][0]['message']['content'])
            assert decision == {'choice': row['choice'], 'reason': row['reason']}
            assert row['correct'] == (row['choice'] in env.expected())
            assert env.execute(row['choice']) == row['tool_result']
            assert env.event(row['step']) == row['external_event']
            assert env.facts == row['facts_after']
        for key, value in env.final_check().items():
            assert episode[key] == value, (episode['episode'], key)
        assert episode['steps'] == len(rows)
        assert episode['correct_steps'] == sum(r['correct'] for r in rows)
        evidence.append({'episode': episode['episode'], **env.final_check()})
    # Exact paired equality in this pilot follows from identical selected tools.
    for case in cases:
        for state in ('unchanged', 'changed'):
            for trial in range(1, meta['trials'] + 1):
                pairs = [[r for r in traces if (r['case'], r['state'], r['trial'], r['arm']) ==
                          (case, state, trial, arm)] for arm in ('direct', 'explicit_impact')]
                assert len(pairs[0]) == len(pairs[1])
                for direct, explicit in zip(*pairs):
                    dp = json.loads(direct['messages'][1]['content'])
                    ep = json.loads(explicit['messages'][1]['content'])
                    ep.pop('依据发生变化、尚待复核的旧判断编号')
                    assert dp == ep
    protected = read(out / 'protected_before.json')
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in protected.items())
    report = {'status': 'passed', 'episodes_replayed': len(episodes), 'calls_replayed': len(traces),
              'snapshot_hashes_verified': True, 'paired_public_inputs_equal_except_impact_list': True,
              'protected_files_unchanged': len(protected), 'final_effect_evidence': evidence}
    (out / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'final_effect_evidence'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
