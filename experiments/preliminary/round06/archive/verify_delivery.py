"""Final artifact integrity and direct official-write checks. No API calls."""
import sys
sys.dont_write_bytecode=True
import json
from pathlib import Path
import hashlib

HERE=Path(__file__).resolve().parent
batch=HERE/'results/20261122T121121980510Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read(batch/'freeze.json'); summary=read(batch/'summary.json')
review=read(batch/'posthoc_evidence_review.json')
assert all(sha(Path(p))==value for p,value in freeze['protected'].items())
assert all(sha(batch/'frozen'/p)==value for p,value in freeze['files'].items())
assert len(summary['rows'])==8
assert sum(bool(r['unsupported_payment_description']) for r in review['rows'])==4
assert sum(bool(r['premature_conditional_permission']) for r in review['rows'])==2
assert sum(r['supplementary_no_detected_issue'] for r in review['rows'])==3
for r in summary['rows']:
    name=r['id']; t=read(batch/(name+'_trajectory.json'))
    f=read(batch/(name+'_final_state.json')); result=read(batch/(name+'_result.json'))
    assert len(t)==5 and len(f['P']['writes'])==1 and len(f['H']['confirmations'])==1
    write=f['P']['writes'][0]; a=write['arguments']; official=write['result']
    assert a['item_ids']==['1151293680','4983901480'] and a['new_item_ids']==['2299424241','7747408585']
    assert a['payment_method_id']=='credit_card_9513926'
    assert official['status']=='exchange requested' and official['exchange_price_difference']==-48.31
    assert result['database_order']['exchange_new_items']==a['new_item_ids']
    assert t[3]['u']['z']['work_id']=='confirm' and t[4]['u']['z']['work_id']=='submit'
    assert t[3]['semantic_parse']['approved'] is True and t[3]['customer'].lower().startswith('yes')
    assert write['gate']['allowed'] and write['gate']['confirmation_sources']==[20,21]
    assert a==t[3]['semantic_parse']['arguments'] and a==f['H']['plan']['arguments']
assert all(pair['starts_identical'] for pair in summary['paired_directions'])
fresh=summary['freshness_audit']
assert fresh=={'responses':90,'unique_ids':90,'overlap_old_response_ids':0,'replayed':0}
audit={'passed':True,'protected_old_files_and_proposal_unchanged':True,'frozen_bundle_unchanged':True,
       'new_suffixes':8,'correct_official_writes':8,'fresh_final_confirmations':8,
       'frozen_scores_preserved':True,'supplementary_premature_permission':2,
       'supplementary_wrong_card_description':4,'freshness':fresh,
       'note':'Artifact verification is distinct from absence of model/semantic defects; those defects remain recorded.'}
(batch/'delivery_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file()
          and '__pycache__' not in p.parts and p.name!='delivery_manifest.json'}
(HERE/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
