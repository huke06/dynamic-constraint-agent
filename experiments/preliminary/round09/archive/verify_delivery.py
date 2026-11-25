"""Artifact integrity and direct trajectory/accounting checks; no model calls."""
import json,hashlib,ast
from pathlib import Path
from input_boundary import validate
HERE=Path(__file__).resolve().parent
batch=HERE/'results/20261122T132951508463Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()).hexdigest()
freeze=read(batch/'freeze.json'); summary=read(batch/'summary.json'); review=read(batch/'claim_review.json')
assert all(sha(Path(p))==v for p,v in freeze['protected'].items())
assert all(sha(batch/'frozen'/p)==v for p,v in freeze['files'].items())
assert read(batch/'frozen/offline_check.json')['passed']
old=HERE.parent/'08_同任务配对复验'
modules=['baseline_engine.py','baseline_runner.py','exchange_core.py','adjacent_reference.py','legacy_engine.py','engine.py','normalization.py','contracts08.py']
assert all(sha(batch/'frozen'/name)==sha(old/name) for name in modules)
oldrun=(old/'run.py').read_text(encoding='utf-8'); newrun=(batch/'frozen/run.py').read_text(encoding='utf-8')
for name in ('work','scores','rollout'):
    prior=next(n for n in ast.parse(oldrun).body if isinstance(n,ast.FunctionDef) and n.name==name)
    current=next(n for n in ast.parse(newrun).body if isinstance(n,ast.FunctionDef) and n.name==name)
    assert ast.get_source_segment(oldrun,prior)==ast.get_source_segment(newrun,current)
assert len(summary['rows'])==16 and all(r['suffix_started'] for r in summary['rows'])
assert sum(r['strict_pass'] is True for r in summary['rows'])==15
assert len(review['rows'])==16 and review['review_count']==32
assert sum(r['status']=='contradiction' for r in review['rows'])==5
assert sum(r['status']=='uncertain' for r in review['rows'])==1
assert len(review['judge_evidence_issues'])==1 and review['judge_evidence_issues'][0]['tool_evidence_verified']
assert sum(p['quality_comparable'] for p in summary['pairs'])==2
for row in summary['rows']:
    name=row['id']; result=read(batch/(name+'_result.json')); state=read(batch/(name+'_final_state.json'))
    start=read(batch/(name+'_start.json')); tid=row['task']; public=read(batch/'frozen/scenarios/public'/('task'+tid+'.json'))
    fixed=read(batch/'frozen/snapshots/public'/f't{tid}_{row["state"]}.json')
    assert start['state']==fixed['state'] and result['start_sha256']==digest(start)
    assert start['remaining_budget']=={'agent_calls':24,'agent_tokens':60000,'work_steps':9}
    target=public['inventory_intervention']['variant_id']; pid=public['product_id']
    assert start['state']['F']['catalog'][pid]['variants'][target]['available'] is (True if row['state']=='known' else None)
    assert start['state']['g']['alternative_permission']=='unknown'
    assert not start['state']['P']['writes'] and not start['state']['H']['confirmations'] and not start['state']['H']['plan']
    assert result['error'] is None and result['abort_stage'] is None
    assert all(result[k] is True for k in ('R_write','R_goal','C_hard','C_authorization_program','C_permission_state',
        'C_permission_provenance','C_authorization_provenance','C_consent_semantic'))
    assert len(state['P']['writes'])==1 and len(state['H']['confirmations'])==1
    write=state['P']['writes'][0]; a=write['arguments']; confirmation=state['H']['confirmations'][0]
    expected='1665571435' if tid=='70' else '6384525445'
    assert a['item_ids']==[public['item_id']] and a['new_item_ids']==[expected]
    assert write['result']['status']=='exchange requested'
    assert write['result']['exchange_price_difference']==(-0.44 if tid=='70' else 34.07)
    assert write['gate']['allowed'] and write['gate']['confirmation_sources']==[confirmation['assistant_ref'],confirmation['user_ref']]
    history=state['F']['dialogue']; rule=state['g']['conditional_permission']
    assert rule['source_quote'] in history[rule['source']]['content']
    assert confirmation['source_quote'] in history[confirmation['user_ref']]['content']
    assert confirmation['user_ref']>rule['source']
    assert all(e['permission']=='unknown' or e['stock'] is True for e in result['permission_events'])
    assert not result['redundant_screen_after_permission_or_plan']
for pair in summary['pairs']:
    assert pair['starts_equal']
    if pair['quality_comparable']:
        assert pair['state']=='known' and pair['repeat']==2 and pair['work_evidence_minus_clarify']==1
        assert pair['agent_calls_evidence_minus_clarify']==1 and pair['review_calls_evidence_minus_clarify']==0
        assert pair['agent_tokens_evidence_minus_clarify']==(5261 if pair['task']=='70' else 3703)
    else:
        assert all(pair[k] is None for k in ('agent_tokens_evidence_minus_clarify','agent_calls_evidence_minus_clarify',
            'review_calls_evidence_minus_clarify','work_evidence_minus_clarify'))
calls=[json.loads(l) for l in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
assert len(calls)==172 and not any(c['stage']=='initial_semantics' or 'reused_from' in c for c in calls)
for c in calls: validate(c['category'],c['stage'],c['messages'])
assert sum(c['category']=='agent' for c in calls)==124
assert summary['integrity']['unique_response_ids']==172 and summary['integrity']['overlap_old_ids']==0
assert summary['category_totals']['agent']['total_tokens']==428067 and not summary['public_prefix']
assert sum(summary['category_totals'][k]['total_tokens'] for k in ('agent','environment_user','external_evaluation'))==573392
audit={'artifact_checks_passed':True,'planned_started':16,'not_started':0,'early_stops':0,'correct_writes':16,
    'goal_condition_and_current_authorization_passes':16,'frozen_strict_passes':15,'supplementary_contradiction_rows':5,
    'supplementary_uncertain_rows':1,'verified_judge_false_negative':1,'quality_comparable_pairs':2,
    'initial_semantic_calls':0,'agent_requests_boundary_checked':124,'responses':172,'old_response_overlap':0,
    'protected_01_08_and_proposal_unchanged':True,'frozen_unchanged':True,'continuation_modules_unchanged_from_08':True,
    'note':'Checks establish artifact fidelity/accounting, not full semantic accuracy or general benefit. Original judge scores and contrary evidence are both retained.'}
(batch/'delivery_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='delivery_manifest.json'}
(HERE/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
