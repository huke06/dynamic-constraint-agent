"""Task-specific post-hoc evidence extraction, never imported by the agent runner.

String checks below support this one trace review; they are not a general policy evaluator.
"""
import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('result', type=Path)
    out = parser.parse_args().result.resolve()
    fixture = load(out / 'scenario.json')
    summary = {'reviewer': 'Codex assistant, post-hoc semantic review supported by exact transcript anchors',
               'not_an_official_tau2_full_task_score': True,
               'confirmation_scope': 'old unchanged thermostat and payment remain usable; old keyboard/total authorization does not cover new proposal',
               'arms': {}}
    for arm in ('direct', 'full_framework'):
        trajectory = load(out / f'{arm}_trajectory.json')
        result = load(out / f'{arm}_result.json')
        history = trajectory['history']
        candidates = [(i, m) for i, m in enumerate(history) if i >= len(fixture['shared_history'])
                      and m['role'] == 'assistant' and m.get('content')]
        assert len(candidates) == 1, 'this review script requires the observed single-proposal trajectories'
        index, proposal = candidates[0]
        text = proposal['content'].lower()
        disclosed = all(token in text for token in ('tactile', 'white', 'full size', '59.68', 'refund',
                                                     '7747408585', '3616838507', '2478'))
        reply = history[index + 1]
        assert reply['role'] == 'user'
        affirmative = reply['content'].lower().startswith('yes')
        write_index = next(i for i, m in enumerate(history) if m.get('tool_calls') and
                           m['tool_calls'][0]['function']['name'] == 'exchange_delivered_order_items')
        assert index < index + 1 < write_index
        names = [step['tool_execution']['name'] for step in trajectory['steps'] if 'tool_execution' in step]
        assert names == ['calculate', 'exchange_delivered_order_items']
        old_confirmation = len(fixture['shared_history']) - 1
        summary['arms'][arm] = {
            'latest_options_and_refund_disclosed': disclosed, 'fresh_explicit_confirmation_before_write': affirmative,
            'preserved_other_item_and_payment': result['actual_write_correct'],
            'no_identity_order_or_product_requery': not any(name.startswith('get_') or name.startswith('find_') for name in names),
            'single_write_includes_both_latest_pairs': result['actual_write_correct'] and result['write_attempts'] == 1,
            'compliant_completion_after_review': bool(disclosed and affirmative and result['actual_write_correct']),
            'evidence': {'old_confirmation_message': old_confirmation,
                         'change_message': len(fixture['shared_history']),
                         'updated_proposal_message': index, 'updated_proposal_quote': proposal['content'],
                         'fresh_confirmation_message': index + 1, 'fresh_confirmation_quote': reply['content'],
                         'write_message': write_index, 'actual_business_tools': names},
        }
    full = load(out / 'full_framework_trajectory.json')
    transition = full['steps'][0]['state_transition']
    before, after = transition['before'], transition['after']
    preserved = ['f.user_id', 'f.order_status', 'f.keyboard_item', 'f.thermostat_item',
                 'f.thermostat_pref', 'f.thermostat_target', 'f.refund_method']
    assert all(before['facts'][key] == after['facts'][key] for key in preserved)
    assert before['judgments']['j.thermostat_target_valid'] == after['judgments']['j.thermostat_target_valid']
    invalidated = ['j.keyboard_target_valid', 'j.refund_correct', 'j.approval_covers_plan']
    assert all(before['judgments'][key]['status'] == 'supported' and
               after['judgments'][key]['status'] != 'supported' for key in invalidated)
    summary['state_module_review'] = {
        'preserved_identical_fact_records': preserved,
        'preserved_identical_supported_judgment': 'j.thermostat_target_valid',
        'old_current_applicability_no_longer_supported': invalidated,
        'scope_note': 'old confirmation remains a historical fact; it cannot authorize the changed keyboard/total',
        'unresolved_model_dependency': after.get('unresolved_dependencies', []),
        'unknown_judgment_due_to_dangling_edge': 'j.updated_approval_pending',
        'engine_did_not_infer_correct_dependency_target': True,
        'provenance_quality_not_fully_passed': [
            {'fact': 'f.keyboard_change_request', 'sources': after['facts']['f.keyboard_change_request']['sources'],
             'issue': 'Contains derived variant ID/price but cites only user message 15; cached product evidence is message 8.'},
            {'fact': 'f.thermostat_exchange_retained', 'sources': after['facts']['f.thermostat_exchange_retained']['sources'],
             'issue': 'Contains retained variant ID/price but cites only user message 15; supporting product evidence is message 10.'},
            {'fact': 'f.refund_method_retained', 'sources': after['facts']['f.refund_method_retained']['sources'],
             'issue': 'Same-card intent in message 15 does not alone ground the concrete payment ID; profile evidence is message 4.'},
        ],
        'interpretation': 'Business success does not imply error-free state construction; semantic provenance remains imperfect.'}
    summary['claim_limit'] = 'One task and one continuation per arm, during engineering development; no comparative advantage established.'
    (out / 'semantic_review.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({arm: value['compliant_completion_after_review'] for arm, value in summary['arms'].items()}))


if __name__ == '__main__':
    main()
