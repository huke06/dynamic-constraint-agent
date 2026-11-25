"""Post-freeze semantic annotations only; reads utterances, never computes fact truth."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BATCH=ROOT/'results/20261123T001740331845Z'
OUT=BATCH/'evaluation'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
r=read(OUT/'semantic_review.json')
public=read(BATCH/'frozen/scenarios/public/task70.json')
old_target=public['fixture']['approved_prefix']['old_plan']['new_item_ids'][0]
def add(key,claim,reason,index=None):
    p={'operation':'append' if index is None else 'replace','claim':claim,'reason':reason}
    if index is not None: p['index']=index
    r['utterances'][key]['patches'].append(p)
for key,entry in r['utterances'].items():
    raw=read(OUT/'extractions'/(key+'.json'))
    for i,c in enumerate(raw['claims']):
        q=c.get('quote','')
        if key.startswith('t70') and c.get('kind')=='difference' and ('original $22.55' in q or 'earlier $22.55' in q):
            d=dict(c); d['selector']={'variant_id':old_target}
            add(key,d,'Explicit original/earlier amount refers to previously confirmed public plan, not fallback.',i)
        if key=='t52_r1_known_screen_ref13' and q=='**30MP resolution, CF card storage, and 10x zoom**':
            add(key,{'kind':'nonassertion','quote':q,'reason':'Restates user requested specifications; not itself a negative catalogue assertion.'},'Keep user goal separate from the following available-set assertion.',i)
            add(key,{'kind':'exists','quote':'there is **no item that has all three**','selector':{'options':{'resolution':'30MP','storage':'CF card','zoom':'10x'}},'scope':'available','asserted':False},'Explicit preceding Looking at the available variants restricts this clause to availability.')
        if key=='t52_r1_known_clarify_ref12' and c.get('kind')=='enumeration' and 'only 10x zoom CF card option' in q:
            d=json.loads(json.dumps(c)); d['selector']['options']['resolution']='30MP'
            add(key,d,'Heading explicitly restricts same-product comparison to 30MP resolution and CF storage.',i)
        if key=='t52_r1_unknown_clarify_ref12' and 'there is no single item that has all three' in q:
            add(key,{'kind':'uncertain','quote':q,'reason':'Available-variant introductory scope versus literal no-item wording; catalogue existence vs availability reading not resolved.'},'Preserve genuine scope ambiguity as pending, without using final results to select an interpretation.',i)
    entry['all_clauses_reviewed']=True
add('t70_r1_known_clarify_ref12',{'kind':'difference','quote':'meaning a small refund to your original Visa card (ending 7312) rather than a charge.','asserted':-0.44,'selector':{'variant_id':'1665571435'}},'Refund description refers to immediately preceding explicit -0.44 arithmetic; covers separate refund anchor.')
add('t52_r1_unknown_clarify_ref12',{'kind':'nonassertion','quote':'or possibly 5x if that one turns out to be in stock','reason':'Conditional future alternative, not a current in-stock assertion.'},'Preserve hypothetical clause around in-stock anchor.')
(OUT/'semantic_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print({'utterances_reviewed':len(r['utterances']),'patches':sum(len(e['patches']) for e in r['utterances'].values())})
