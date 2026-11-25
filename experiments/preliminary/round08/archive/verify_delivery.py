"""Final integrity/accounting verification, without any model calls."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
batch=HERE/'results/20261122T125916414502Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read(batch/'freeze.json'); summary=read(batch/'summary.json'); review=read(batch/'claim_review.json')
assert all(sha(Path(p))==v for p,v in freeze['protected'].items())
assert all(sha(batch/'frozen'/p)==v for p,v in freeze['files'].items())
assert read(batch/'frozen/offline_check.json')['passed']
assert len(summary['rows'])==16 and sum(r['suffix_started'] for r in summary['rows'])==8
assert sum(r['R_write'] is True for r in summary['rows'])==8
assert sum(r['strict_pass'] is True for r in summary['rows'])==6
assert review['review_count']==16
assert sum(r['status']=='contradiction' for r in review['rows'])==2
assert sum(r['status']=='uncertain' for r in review['rows'])==1
assert sum(p['quality_comparable'] for p in summary['pairs'])==2
for row in summary['rows']:
    name=row['id']; result=read(batch/(name+'_result.json'))
    if not row['suffix_started']:
        assert name.startswith('t70') and result['abort_stage']=='semantic_equivalence_check'
        assert not (batch/(name+'_trajectory.json')).exists()
        continue
    assert name.startswith('t52') and result['abort_stage'] is None and result['error'] is None
    assert all(result[k] is True for k in ('R_write','R_goal','C_hard','C_authorization_program',
        'C_permission_state','C_permission_provenance','C_authorization_provenance','C_consent_semantic'))
    state=read(batch/(name+'_final_state.json')); history=state['F']['dialogue']
    writes=state['P']['writes']; assert len(writes)==1
    write=writes[0]; a=write['arguments']; official=write['result']
    assert a['item_ids']==['5996159312'] and a['new_item_ids']==['6384525445'] and a['payment_method_id']=='paypal_8194385'
    assert official['status']=='exchange requested' and official['exchange_price_difference']==34.07
    assert result['database_order']['exchange_new_items']==a['new_item_ids']
    rule=state['g']['conditional_permission']; confirmation=state['H']['confirmations'][-1]
    assert rule['source_quote'] in history[rule['source']]['content']
    assert confirmation['source_quote'] in history[confirmation['user_ref']]['content']
    assert confirmation['user_ref']>rule['source']
    assert write['gate']['allowed'] and write['gate']['confirmation_sources']==[confirmation['assistant_ref'],confirmation['user_ref']]
    t=read(batch/(name+'_trajectory.json')); assert t[-2]['u']['z']['work_id']=='confirm' and t[-1]['u']['z']['work_id']=='submit'
    current_auth=t[-2]['semantic_parse']['authorization']
    assert current_auth['approved'] and current_auth['source_ref']==confirmation['user_ref']
    assert current_auth['arguments']==a and current_auth['source_quote']==confirmation['source_quote']
    assert not result['redundant_screen_after_permission_or_plan']
    if name.endswith('unknown_clarify'):
        events=result['permission_events']
        assert events[0]['stock'] is None and events[0]['permission']=='unknown'
        assert events[-1]['stock'] is True and events[-1]['permission']=='6384525445'
for pair in summary['pairs']:
    if not pair['quality_comparable']:
        assert all(pair[k] is None for k in ('agent_tokens_evidence_minus_clarify','agent_calls_evidence_minus_clarify',
            'review_calls_evidence_minus_clarify','work_evidence_minus_clarify'))
    else:
        assert pair['task']=='52' and pair['repeat']==2 and pair['starts_equal']
        if pair['state']=='known':
            assert pair['agent_tokens_evidence_minus_clarify']==4092 and pair['work_evidence_minus_clarify']==1
        else:
            assert pair['agent_tokens_evidence_minus_clarify']==-531 and pair['work_evidence_minus_clarify']==0
assert summary['integrity']['responses']==90 and summary['integrity']['unique_response_ids']==90
assert summary['integrity']['overlap_old_ids']==0 and summary['integrity']['replayed']==0
assert summary['category_totals']['agent']['total_tokens']==211736
assert sum(p['total_tokens'] for p in summary['public_prefix'].values())==1510
audit={'artifact_checks_passed':True,'planned_slots':16,'started_suffixes':8,'initialization_aborted_slots':8,
       'independent_initialization_aborts':2,'correct_writes':8,'condition_and_current_authorization_passes':8,
       'raw_strict_passes':6,'fact_review_contradiction_rows':2,'fact_review_uncertain_rows':1,
       'quality_comparable_pairs':2,'responses':90,'old_response_overlap':0,'replayed':0,
       'protected_01_07_and_proposal_unchanged':True,'frozen_bundle_unchanged':True,
       'note':'Artifact checks do not establish general benefit or absence of semantic flaws. Aborts and limitations are retained.'}
(batch/'delivery_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
files={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='delivery_manifest.json'}
(HERE/'delivery_manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
