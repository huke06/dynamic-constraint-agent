"""Auditable semantic-review draft for saved extractions. No fact verdicts or API calls.

Approval means the assistant has read the corresponding sampled utterances; not independent human gold.
"""
import json,re,hashlib,sys,argparse
from pathlib import Path
from copy import deepcopy
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main(batch,out,approve=False):
    results=read(batch/'results.json'); review={'reviewer':'assistant semantic review, not independent human annotation',
        'limits':'Only type/scope/quote/entity annotations; no expected truth or pass/fail overrides. Raw model extractions retained.', 'utterances':{}}
    for name in results:
        if not (batch/(name+'_final_state.json')).exists(): continue
        tid=name.split('_')[0][1:]; public=read(batch/'frozen/scenarios/public'/('task'+tid+'.json'))
        t=read(batch/(name+'_trajectory.json'))
        for e in t:
            if not e.get('assistant'): continue
            text=e['assistant']; ref=e['assistant_ref']; path=out/'extractions'/f'{name}_ref{ref}.json'
            if not path.exists(): continue
            raw=read(path); patches=[]
            for i,c0 in enumerate(raw['claims']):
                c=deepcopy(c0); q=c.get('quote',''); low=q.lower(); reason=None
                if c.get('kind')=='options' and not (c.get('selector') or {}).get('variant_id') and (
                    'you want' in low or 'preferred' in low or 'required' in low):
                    c={'kind':'nonassertion','quote':q,'reason':'Restates user intent, not a property of a named SKU; intent remains separately evaluated.'}; reason='user intent vs tool-SKU options'
                elif c.get('kind')=='maximum' and ('prefer' in low or 'without being asked' in low):
                    c={'kind':'nonassertion','quote':q,'reason':'User preference, not current numerical inventory maximum.'}; reason='preference vs catalogue maximum'
                elif c.get('kind')=='stock' and ('no available' in low or 'no confirmed-available' in low or 'no black + high ventilation + medium' in low):
                    c['kind']='exists'; c['scope']='confirmed_available' if 'confirmed' in low else 'available'; c['asserted']=False
                    reason='negative available-match existence assertion, not stock of an existing SKU'
                elif c.get('kind')=='uncertain' and 'no confirmed-available' in low:
                    c.update(kind='exists',scope='confirmed_available',asserted=False); reason='explicitly confirmed-available set, not catalogue absence'
                elif c.get('kind')=='price' and 'difference' in low:
                    c['kind']='difference'; reason='utterance labels amount a difference, not item price'
                    if 'original exchange you confirmed' in text.lower():
                        c.setdefault('selector',{})['variant_id']=public['fixture']['approved_prefix']['old_plan']['new_item_ids'][0]
                        reason+='; binds the explicitly mentioned previously confirmed plan, not the current fallback'
                elif c.get('kind')=='maximum' and not c.get('field') and 'zoom' in low:
                    c['field']='zoom'; reason='explicit numerical maximum field named in quote'
                if c!=c0: patches.append({'operation':'replace','index':i,'claim':c,'reason':reason})
            # Literal parenthetical disjunction: preserve both asserted alternatives, including low.
            parenthetical='the black/medium options are medium or low ventilation, and those are unavailable anyway'
            if parenthetical in text:
                patches.append({'operation':'append','claim':{'kind':'enumeration','quote':parenthetical,
                    'selector':{'options':{'color':'black','size':'M'}},'scope':'all',
                    'asserted':[{'options':{'ventilation':'medium'}},{'options':{'ventilation':'low'}}]},
                    'reason':'Both alternatives explicitly asserted in parenthetical; raw extraction omitted low.'})
            # Contextually restricted no-item phrases in available-CF paragraph and following CF-only list.
            if 'the 10x zoom variants are currently unavailable:' in text and '30MP / CF card / 10x zoom' in text:
                for i,c0 in enumerate(raw['claims']):
                    if c0.get('kind')=='exists' and 'no item that has all three' in c0.get('quote',''):
                        c=deepcopy(c0); c['scope']='available'
                        patches.append({'operation':'replace','index':i,'claim':c,'reason':'Available-variant paragraph, immediately clarified by explicit unavailable CF10x list; not an absolute nonexistence assertion.'})
                    elif c0.get('kind')=='stock' and 'the 10x zoom variants are currently unavailable' in c0.get('quote',''):
                        c=deepcopy(c0); c.setdefault('selector',{}).setdefault('options',{})['storage']='CF card'
                        patches.append({'operation':'replace','index':i,'claim':c,'reason':'The immediate exhaustive list is CF-card 10x variants; retains that explicit contextual restriction.'})
            # Requests and unconfirmed stock-state descriptions are not factual assertions.
            for line in text.splitlines():
                if (line.strip().startswith('If you\'d like to proceed, please explicitly confirm')
                    or 'whose stock status is unconfirmed' in line):
                    patches.append({'operation':'append','claim':{'kind':'nonassertion' if 'please' in line else 'stock',
                        'quote':line.strip(),**({} if 'please' in line else {'selector':{'variant_id':public['inventory_intervention']['variant_id']},'asserted':'unknown'})},
                        'reason':'Closing confirmation request / explicit unconfirmed stock descriptor; coverage span retained.'})
            review['utterances'][f'{name}_ref{ref}']={'all_clauses_reviewed':approve,'extraction_sha256':sha(path),
                'patches':patches,'note':'Full sampled utterance checked; ambiguous readings are not automatically resolved by final outcome.'}
    (out/'semantic_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'utterances':len(review['utterances']),'patches':sum(len(r['patches']) for r in review['utterances'].values()),'reviewed':approve}))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--batch',type=Path,required=True); p.add_argument('--out',type=Path,required=True); p.add_argument('--reviewed',action='store_true'); a=p.parse_args(); main(a.batch,a.out,a.reviewed)
