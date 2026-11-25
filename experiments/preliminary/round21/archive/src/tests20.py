from copy import deepcopy
from construct20 import R,read
from world20 import World
from exchange_core import packed
def job(w,k,obj=None,**p):return {'work_type':k,'object':obj or w.cfg['order_id'],'parameters':p,'evidence_refs':[],'expected':'offline check','reason':'fixture'}
def parse_fixture(w):
 updates=[]
 for ref in w.pending:
  a=w.asks.get(str(ref));text=w.history[ref]['content']
  if a and a['kind']=='confirm' and text.startswith('Yes'):updates.append({'kind':'approval','source_ref':ref,'quote':text,'proposal_ref':a['assistant_ref']})
  elif a and a['kind']=='clarify' and text.startswith('That one'):updates.append({'kind':'permission','source_ref':ref,'quote':text,'item_id':a['object'],'variant_id':a['offered_variant_id'],'conditional_stock':True})
  elif not a:updates.append({'kind':'requirement','source_ref':ref,'quote':text,'item_id':w.cfg['changed_item'],'variant_id':w.cfg['changed_target'],'conditional_stock':True})
 return {'updates':updates,'processed_refs':list(w.pending),'needs_clarification':False}
def check():
 checks={}
 from logtests20 import check as check_logging
 checks.update(check_logging())
 for tid in ('0','58','95','106'):
  cfg=read(R/f'configs/stage1/{tid}/case.json');a=World(cfg,'stable',None);w=World(cfg,'changed',None);checks[tid+'_same_public_start']=a.history==w.history and a.state()==w.state();b=cfg['scope'][1];bp=w.item(b)['product_id']
  for x in (a,w):assert x.perform(job(x,'prepare'))['allowed'];assert x.perform(job(x,'confirm'))['allowed']
  checks[tid+'_trigger_after_real_confirmation']=w.change is not None and a.change is None;checks[tid+'_old_auth_blocked']=not w.perform(job(w,'submit'))['allowed'] and not w.writes
  w.apply(parse_fixture(w));checks[tid+'_unaffected_B_still_available']=w.stock(b)is True
  if cfg['change_type']=='resource':
   i=cfg['changed_item'];v=w.alternatives(i)[0]['item_id'];e=w.perform(job(w,'clarify',i,variant_id=v),f'Item {v} is in stock. Would you accept this alternative for item {i}?');checks[tid+'_pronoun_reply_no_sku']=v not in w.history[-1]['content'];checks[tid+'_local_does_not_repeat_B_catalogue']=bp not in packed(w.local());w.apply(parse_fixture(w))
  checks[tid+'_permission_not_transaction_approval']=not w.current_auth();assert w.perform(job(w,'prepare'))['allowed'];assert w.perform(job(w,'confirm'))['allowed'];w.apply(parse_fixture(w));checks[tid+'_new_auth_effective']=w.current_auth();pre=deepcopy(w.core.records);assert w.perform(job(w,'submit'))['allowed'];checks[tid+'_one_write_two_items']=len(w.writes)==1 and len(w.writes[0]['arguments']['item_ids'])==2 and w.writes[0]['independent']['independent_valid_authorization']
  old=next(e for e in [w.event_export] if e)['before_records'];checks[tid+'_B_sources_unchanged']=all(old[k]==pre[k] for k in ('requirement:'+b,'catalog:'+bp,'match:'+b,'delta:'+b,'payment','identity'))
  a.apply(parse_fixture(a));checks[tid+'_stable_one_write']=a.perform(job(a,'submit'))['allowed'] and len(a.writes)==1
 # Every held-out tier task must be constructible; no model debugging on held-outs.
 for cfgrow in read(R/'configs/tasks.json'):
  if cfgrow['stage']=='stage2':
   cfg=read(R/f"configs/stage2/{cfgrow['task_id']}/case.json");x=World(cfg,'changed' if cfgrow['tier']=='dynamic' else 'stable',None);checks[cfgrow['task_id']+'_heldout_constructible']=bool(x.core.authenticated) and len(x.cfg['scope'])==(2 if cfgrow['tier']=='dynamic' else 1)
 checks['distinct_stage1_orders']=len({read(R/f'configs/stage1/{i}/case.json')['order_id'] for i in ('0','58','95','106')})==4
 checks['stage2_not_stage1_task_ids']=not(set(('0','58','95','106'))&{r['task_id'] for r in read(R/'configs/tasks.json') if r['stage']=='stage2'})
 assert all(checks.values()),checks
 return {'passed':True,'model_calls':0,'checks':checks}
if __name__=='__main__':
 from construct20 import save
 save(R/'configs/offline.json',check());print('offline passed')
