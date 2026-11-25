"""Independent post-run scoring and presentation checks; no API calls."""
from post24 import *

def audit():
 checks=[]
 x=read(E/'results/A01/A_t39_r2_official_final.json')
 assert not outcome(x)['correct_registered'] and outcome24(x)['correct_registered'];checks.append('legacy array-order false negative corrected by canonical mapping')
 y=deepcopy(x);a=y['writes'][0]['arguments'];a['item_ids']=a['item_ids'][::-1];a['new_item_ids']=a['new_item_ids'][::-1]
 assert outcome24(y)['correct_registered'];checks.append('joint permutation preserves exchange semantics')
 y=deepcopy(x);a=y['writes'][0]['arguments'];a['new_item_ids']=a['new_item_ids'][::-1]
 assert not outcome24(y)['correct_registered'];checks.append('changed mapping remains wrong')
 y=deepcopy(x)
 for a in y['environment_only']['approvals']:a['valid']=False
 assert not outcome24(y)['correct_registered'];checks.append('historical invalidated authorization cannot pass')
 precision=[]
 for scope,base,tid in [('A01',E,'39'),('A2',E/'versions/a2','43')]:
  x=read(base/f'results/A01/A_t{tid}_r1_framework_start.json');cfg=x['cfg'];cap=Decimal(x['hard_cap']);display=Decimal(f'{cap:.2f}');items={i['item_id']:i for i in cfg['environment']['orders'][cfg['order_id']]['items']};first=cfg['scope'][0];other=sum((Decimal(str(cfg['environment']['products'][items[i]['product_id']]['variants'][cfg['targets'][i]]['price']))-Decimal(str(items[i]['price'])) for i in cfg['scope'][1:]),Decimal('0'));variants=cfg['environment']['products'][items[first]['product_id']]['variants'];flips=[]
  for v in variants.values():
   if not v['available'] or v['item_id']==first:continue
   d=Decimal(str(v['price']))-Decimal(str(items[first]['price']))+other
   if (d<=cap)!=(d<=display):flips.append(v['item_id'])
  assert not flips
  precision.append({'batch':scope,'task':tid,'framework_model_cap':str(cap),'initial_literal_user_cap':str(display),'strict_numeric_input_equality':cap==display,'feasibility_classification_flips_on_observed_variants':flips,'disposition':'explicit input precision limitation; do not use task for clean group effect/cost claims'})
 examples=[json.loads(l) for l in (E/'results/B1/SFT_EXAMPLES.jsonl').read_text('utf-8').splitlines()]
 assert all(c['not_forced'] and all(c['pass_reason'].values()) and 'subsequent_effect' not in c['messages'][1]['content'] for c in examples);checks.append('12 examples exact actual input, no correction, no future evaluation payload')
 for sample in examples:
  p=Path(sample['source_trace']);tr=read(p);ordinal=sum(e['module']=='cognitive_decision' for e in tr[:sample['source_event']]);branch=p.name.removesuffix('_trace.json');cs=[json.loads(l) for l in (p.parent/'model_calls.jsonl').read_text('utf-8').splitlines()];cs=[c for c in cs if c['branch']==branch and c['role']=='cognitive' and c['status']=='success']
  assert cs[ordinal]['response']['id']==sample['source_response_id']
  assert cs[ordinal]['messages']==sample['messages'][:-1]
 checks.append('12 SFT event ordinals match actual response IDs and requests, not merely identical action text')
 # Scope of the B35 configuration is the real frozen visible order, not its name.
 state=next(s for s in read(E/'configs/B/states.json') if s['task']=='35');assert state['priorities']==['color','battery life','water resistance'];checks.append('35 scored against actual visible priority order')
 save(E/'results/POSTRUN_CHECKS.json',{'passed':True,'checks':checks,'precision_limitations':precision,'execution_not_changed':True});print({'passed':True,'checks':len(checks),'precision_limitations':precision})

if __name__=='__main__':audit()
