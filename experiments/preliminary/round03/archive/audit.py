"""Replay actual free actions; verify fair inputs and report separate model costs."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import run


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    args = parser.parse_args()
    out = args.result.resolve()
    meta = read(out / 'metadata.json')
    variant = read(out / 'scenario.json')
    for name, digest in meta['snapshot_sha256'].items():
        assert run.sha(out / 'snapshot' / name) == digest, name
    for name in ('run.py', 'state.py'):
        assert run.sha(run.HERE / name) == meta['snapshot_sha256'][name]
    for name, digest in meta['official_source_sha256'].items():
        assert run.sha(Path(name)) == digest, name
    calls = [json.loads(line) for line in (out / 'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    costs = {}
    for call in calls:
        group = call['kind'].split('/')[0]
        function = 'actor' if '/actor/' in call['kind'] else ('customer' if '/customer/' in call['kind'] else 'state')
        key = group + '/' + function
        item = costs.setdefault(key, {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'seconds': 0})
        item['calls'] += 1
        usage = call.get('response', {}).get('usage', {})
        for field in ('prompt_tokens', 'completion_tokens'):
            item[field] += usage.get(field, 0) or 0
        item['seconds'] += call.get('seconds', 0)
        assert call['temperature'] == 0 and call['thinking'] is False
        assert 'private_evaluation' not in json.dumps(call['messages']), call['kind']
    initial = variant['shared_history'] + [variant['change_message']]
    shared_digest = hashlib.sha256(json.dumps(variant['shared_history'], ensure_ascii=False).encode()).hexdigest()
    assert shared_digest == meta['shared_prefix_sha256']
    schemas, replayed = [], []
    for arm in run.ARMS:
        trajectory = read(out / f'{arm}_trajectory.json')
        result = read(out / f'{arm}_result.json')
        history = deepcopy(initial)
        tools = run.new_tools()
        executed = []
        state = run.EvidenceState()
        if arm == 'full_framework':
            prefix = read(out / 'prefix_state.json')
            seeded = run.EvidenceState()
            assert seeded.apply(prefix['patch'], len(variant['shared_history'])) == prefix
            state.facts = deepcopy(prefix['after']['facts'])
            state.judgments = deepcopy(prefix['after']['judgments'])
        for step in trajectory['steps']:
            assert step['history_before'] == history
            if arm == 'full_framework':
                assert state.apply(step['state_transition']['patch'], len(history)) == step['state_transition']
            actor = next(c for c in calls if c['kind'] == f'{arm}/actor/{step["step"]}')
            assert actor['messages'][1:] == history
            expected_system = run.ACTOR + '\n\n' + (out / 'snapshot' / 'official_policy.md').read_text(encoding='utf-8')
            if arm == 'full_framework':
                expected_system += '\nMaintained evidence state:\n' + json.dumps(state.snapshot(), ensure_ascii=False)
            assert actor['messages'][0]['content'] == expected_system
            assert step['assistant'] == actor['response']['choices'][0]['message']
            schemas.append(actor['tools'])
            msg = step['assistant']
            if msg.get('tool_calls'):
                history.append({'role': 'assistant', 'tool_calls': msg['tool_calls']})
                tc = msg['tool_calls'][0]
                action = step['tool_execution']
                name, arguments = tc['function']['name'], json.loads(tc['function']['arguments'])
                assert name == action['name'] and arguments == action['arguments']
                try:
                    response = run.call(tools, name, arguments)
                    assert action['ok'] and response == action['result']
                except (ValueError, TypeError) as exc:
                    assert not action['ok'] and type(exc).__name__ + ': ' + str(exc) == action['error']
                    response = {'error': action['error']}
                history.append({'role': 'tool', 'tool_call_id': tc['id'], 'content': json.dumps(response, ensure_ascii=False)})
                executed.append(action)
            else:
                history.append({'role': 'assistant', 'content': msg['content']})
                customer = next(c for c in calls if c['kind'] == f'{arm}/customer/{step["step"]}')
                assert customer['messages'][0]['content'] == run.USER
                assert step['customer']['content'] == customer['response']['choices'][0]['message']['content']
                history.append(step['customer'])
        assert trajectory['history'] == history
        for key, value in run.final_score(tools, variant, executed).items():
            assert result[key] == value, (arm, key)
        if arm == 'full_framework':
            final = read(out / 'full_framework_final_state_transition.json')
            assert state.apply(final['patch'], len(history)) == final
            assert result['state_final'] == state.snapshot()
        replayed.append({'arm': arm, 'steps': len(trajectory['steps']), 'actual_write_correct': result['actual_write_correct']})
    assert all(schema == schemas[0] for schema in schemas)
    original = read(out / 'protected_before.json')
    assert all(run.sha(Path(p)) == h for p, h in original.items())
    report = {'status': 'passed', 'replayed': replayed, 'identical_tool_schemas': True,
              'identical_initial_history_and_change': True, 'no_private_evaluation_in_model_requests': True,
              'snapshot_and_official_hashes_verified': True, 'protected_files_unchanged': len(original),
              'model_costs': costs, 'returned_models': sorted({c['response']['model'] for c in calls if 'response' in c})}
    run.save(out / 'audit.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
