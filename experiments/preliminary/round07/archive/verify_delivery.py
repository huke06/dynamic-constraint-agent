"""Verify delivered frozen evidence. No model calls or score modification."""
import json,hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
batch=HERE/'results/20261122T123400300210Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(batch/'freeze.json'); summary=read(batch/'summary.json'); review=read(batch/'posthoc_review.json')
assert all(sha(Path(p))==v for p,v in manifest['protected'].items())
assert all(sha(batch/'frozen'/p)==v for p,v in manifest['files'].items())
assert len(summary['rows'])==16
assert sum(x['suffix_started'] for x in summary['rows'])==12
assert sum(x['R_write'] is True for x in summary['rows'])==10
assert sum(x['strict_pass'] is True for x in summary['rows'])==10
assert sum(x['C_permission_state'] is True for x in summary['rows'])==12
assert len(review['claims_findings'])==4
assert len({x['branch'] for x in review['claims_findings']})==3
assert review['payment_worker_utterances_checked']==24 and not review['payment_issues']
assert sum(x['supplementary_quality_comparable'] for x in review['supplementary_pairs'])==3
assert summary['integrity']=={'protected_unchanged_now':True,'frozen_unchanged_now':True,
    'responses':129,'unique_response_ids':129,'overlap_old_ids':0,'replayed':0,'started_paired_starts_equal':True}
for row in summary['rows']:
    name=row['id']
    if not row['suffix_started']:
        assert row['task']=='70' and row['repeat']==2
        assert not (batch/(name+'_trajectory.json')).exists()
        continue
    state=read(batch/(name+'_final_state.json')); result=read(batch/(name+'_result.json'))
    cfg=read(batch/'frozen/scenarios'/('task'+row['task']+'.json'))['config']
    for w in state['P']['writes']:
        args=w['arguments']; official=w['result']
        assert args['item_ids']==[cfg['item_id']] and args['new_item_ids']==[cfg['acceptable_variant']]
        assert args['payment_method_id']==cfg['payment_method']['id']
        assert official['status']=='exchange requested'
        assert official['exchange_price_difference']==(-0.44 if row['task']=='70' else 34.07)
        assert len(state['H']['confirmations'])==1
        confirmation=state['H']['confirmations'][0]
        assert w['gate']['allowed'] and w['gate']['confirmation_sources']==[confirmation['assistant_ref'],confirmation['user_ref']]
        assert state['F']['dialogue'][confirmation['user_ref']]['content'].lower().startswith('yes')
    if result['error']:
        assert 'exact user source quote' in result['error']
        assert not state['P']['writes'] and not state['H']['confirmations']
        assert state['g']['conditional_permission']['sat']=='满足'
assert summary['category_totals']['agent']['total_tokens']==302111
assert sum(x['total_tokens'] for x in summary['public_prefix'].values())==1250
audit={'artifact_checks_passed':True,'planned_slots':16,'started_suffixes':12,'correct_writes':10,
       'quote_validation_failures':2,'unstarted_due_to_shared_initialization':4,
       'original_strict_pass_count':10,'supplementary_claim_issues':4,'affected_branches':3,
       'condition_activation_violations_detected':0,'payment_ending_issues_detected':0,
       'frozen_and_protected_unchanged':True,'replayed':0,
       'note':'This verifies records and accounting, not absence of model/semantic flaws. Those remain in the report.'}
(batch/'delivery_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
files={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='delivery_manifest.json'}
(HERE/'delivery_manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
