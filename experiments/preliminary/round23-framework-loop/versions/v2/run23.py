"""Independent round-23 runner. All formal directories are create-only."""
import os,sys,json,time,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
EXP=Path(__file__).resolve().parent;REPO=EXP.parents[4]
os.environ['DCA_EXPERIMENT_DIR']=str(EXP)
sys.path.insert(0,str(REPO/'src'));sys.path.insert(0,str(REPO/'src/dynamic_constraint_agent_v2/compat'))
from construct20 import read,save,sha
from dynamic_constraint_agent_v2.state_model import BusinessState
from dynamic_constraint_agent_v2.decision import choose
from dynamic_constraint_agent_v2.execution import execute
from runner20 import semantic
from transport20 import Transport
import baseline_runner as b

def job(w,kind,variant=None):
 i=w.cfg['scope'][0]
 return {'work_type':kind,'object':w.item(i)['product_id']if kind=='query'else i if kind in('analyze','clarify')else w.cfg['order_id'],'parameters':{'variant_id':variant}if variant else{},'evidence_refs':[],'expected':'actual defined work result','reason':'predeclared first work for same-state continuation'}

def snapshot(tid,state,t=None):
 cfg=read(EXP/f'configs/tasks/{tid}/case.json');w=BusinessState(cfg,'changed'if tid=='29'else'stable',t);w.policy=(EXP/'configs/official_policy.md').read_text('utf-8');w.initialize_constraints(cfg.get('caps',{}).get(state,10000))
 if tid=='102':
  assert w.perform(job(w,'prepare'))['allowed'];assert w.perform(job(w,'confirm'))['allowed'];ref=w.pending[0];fixture_parse(w)
  if state=='withdrawn':
   ref=len(w.history);w.history.append({'role':'user','content':'I withdraw final transaction approval only. The specification permission remains; ask my fresh complete-plan approval.'});w.core.records['authorization']['status']='stale';w.env_epoch+=1
   for a in w.env_approvals:a['valid']=False
 return w

def fixture_parse(w):
 updates=[]
 for ref in w.pending:
  text=w.history[ref]['content'];ask=w.asks.get(str(ref))
  if ask and ask['kind']=='confirm'and text.startswith('Yes'):updates.append({'kind':'approval','source_ref':ref,'quote':text})
  elif ask and ask['kind']=='clarify'and text.startswith('Replace'):updates.append({'kind':'permission','source_ref':ref,'quote':text,'item_id':ask['object'],'variant_id':ask['offered_variant_id'],'conditional_stock':True})
  elif not ask:updates.append({'kind':'requirement','source_ref':ref,'quote':text,'item_id':w.cfg['scope'][0],'variant_id':w.cfg['changed_target'],'conditional_stock':True})
 w.apply({'updates':updates,'processed_refs':list(w.pending),'needs_clarification':False})

def make_new():
 db=read(b.DATA/'db.json');tasks=read(b.DATA/'tasks.json')
 for tid,oid,scope in [('26','#W5565470',['7602931732','9570044148']),('35','#W8528674',['4716977452','4024196380'])]:
  order=db['orders'][oid];uid=order['user_id'];products={};targets={};opts={}
  for idx,i in enumerate(scope):
   item=next(x for x in order['items']if x['item_id']==i);prod=db['products'][item['product_id']];products[item['product_id']]=prod;vs=sorted([v for v in prod['variants'].values()if v['available']and v['item_id']!=i],key=lambda v:v['price']);v=vs[-1]if idx==0 else vs[0];targets[i]=v['item_id'];opts[i]=v['options']
  i=scope[0];item=next(x for x in order['items']if x['item_id']==i);prod=products[item['product_id']];other=sum(products[next(x['product_id']for x in order['items']if x['item_id']==j)]['variants'][targets[j]]['price']-next(x['price']for x in order['items']if x['item_id']==j)for j in scope[1:]);deltas=sorted(v['price']-item['price']+other for v in prod['variants'].values()if v['available']and v['item_id']not in(i,targets[i]));target_delta=prod['variants'][targets[i]]['price']-item['price']+other;cap=round((deltas[min(2,len(deltas)-1)]+target_delta)/2,2);assert cap<target_delta
  pay=order['payment_history'][0]['payment_method_id'];msg=f"I am {uid}, email {db['users'][uid]['email']}. In delivered order {oid} exchange ONLY this mapping of original items to initially requested replacements: {json.dumps(targets)}. Requested options: {json.dumps(opts)}. Keep all other items and use original payment {pay}. I accept the initially requested specifications ONLY if available within the separately stated whole-amount cap; otherwise discuss feasible alternatives with me. Different specifications require my new permission. Show the complete current proposal for independent final authorization."
  cfg={'task_id':tid,'tier':'independent_controlled_exchange','order_id':oid,'user_id':uid,'scope':scope,'targets':targets,'initial_options':opts,'payment_method_id':pay,'initial_message':msg,'initial_catalogues':True,'change_type':'none','caps':{'conflict':cap,'feasible':10000.0},'states':['conflict','feasible'],'environment':{'orders':{oid:order},'users':{uid:db['users'][uid]},'products':products},'adaptation':'Original task is return business. This explicit two-product exchange is a controlled dynamic-constraint variant derived from its untouched public order. Not an original tau2 benchmark success. These tasks were candidates in round21, not used for debugging/runs before this round.'}
  save(EXP/f'configs/tasks/{tid}/original_task.json',next(t for t in tasks if t['id']==tid));save(EXP/f'configs/tasks/{tid}/subtask.json',{'source_order':oid,'scope':scope,'original_business':'returns','controlled_business':'exchange','other_orders_not_executed':True});save(EXP/f'configs/tasks/{tid}/case.json',cfg);save(EXP/f'configs/tasks/{tid}/dynamic_variant.json',{'variable':'signed combined amount cap','states':cfg['caps'],'all_other_business_facts_same':True})

def rollout(out,tid,state,n,t,first=None,checkpoint=False,group='direct'):
 w=snapshot(tid,state,t);t.world=w;t.branch=n;trace=[];error=None;start=time.perf_counter();save(out/(n+'_start.json'),w.export());save(out/(n+'_visible_start.json'),w.model_state());repeated={}
 try:
  if first:
   v=next(o['variant_id']for o in w.comparison()['negotiable']);d=job(w,first,v if first=='clarify'else None);execute(w,d,t,trace)
  for tick in range(35):
   if w.writes or w.stopped:break
   if min(w.remaining_budget.values())<=0:error='budget_exhausted';break
   if w.pending:
    before=w.export();semantic(w,t,trace);trace.append({'module':'state_constraint_update','before':before,'after':w.export(),'current_model_input':w.model_state()});continue
   before=w.export();d=choose(w,t,group if checkpoint else'direct');trace.append({'module':'cognitive_decision','model_output':d,'state':w.model_state(group=='candidate'if checkpoint else False)});e=execute(w,d,t,trace)
   if w.event_export:trace.append({'module':'public_change','event':w.event_export});w.event_export=None
   if checkpoint:break
   if not e['allowed']:
    k=json.dumps([d,e['reason']],sort_keys=True);repeated[k]=repeated.get(k,0)+1
    if repeated[k]>=3:error='repeated_same_rejection';break
  if not checkpoint and not w.writes:error=error or('justified_stop'if w.stopped else'loop_limit')
 except Exception as ex:
  from logging16 import sanitize
  error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'module':'failure','error':error})
 save(out/(n+'_trace.json'),trace);save(out/(n+'_final.json'),w.export());r={'id':n,'task':tid,'state':state,'first':first,'group':group,'checkpoint':checkpoint,'writes':len(w.writes),'error':error,'seconds':time.perf_counter()-start};print(r,flush=True);return r

def verify_freeze():
 f=read(EXP/'configs/FREEZE.json');assert all(sha(REPO/k)==v for k,v in f['files'].items()),'Frozen input changed'
def freeze():
 assert read(EXP/'results/OFFLINE.json')['passed'];p=EXP/'configs/FREEZE.json';assert not p.exists();files={str(x.relative_to(REPO)):sha(x)for folder in (REPO/'src',REPO/'tests',EXP/'configs')for x in folder.rglob('*')if x.is_file()and'__pycache__'not in x.parts};files[str(Path(__file__).relative_to(REPO))]=sha(Path(__file__));save(p,{'created_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'files':files})
def run_old(name):
 if not name.startswith('pilot'):verify_freeze()
 out=EXP/'results'/name;out.mkdir(exist_ok=False);t=Transport(out);rows=[]
 cases=[('93','conflict','analyze'),('93','feasible','clarify'),('29','dynamic',None),('102','withdrawn',None)]if not name.startswith('pilot')else[('93','conflict','analyze'),('93','feasible','clarify')]
 for tid,state,first in cases:
  for rep in((1,)if name.startswith('pilot')else(1,2)):
   n=f'old_t{tid}_{state}_r{rep}';rows.append(rollout(out,tid,state,n,t,first));save(out/'OUTCOMES.json',rows)
 t.close()
def run_new():
 verify_freeze();assert read(EXP/'results/OLD_GATE.json')['passed'];out=EXP/'results/new01';out.mkdir(exist_ok=False);t=Transport(out);rows=[]
 for tid in('26','35'):
  for state in('conflict','feasible'):
   for rep in(1,2):
    for group in(('direct','candidate')if rep==1 else('candidate','direct')):
     n=f'A_t{tid}_{state}_r{rep}_{group}';rows.append(rollout(out,tid,state,n,t,checkpoint=True,group=group));save(out/'OUTCOMES.json',rows)
 for tid in('26','35'):
  for rep in(1,2):
   for first in(('analyze','clarify')if rep==1 else('clarify','analyze')):
    n=f'B_t{tid}_conflict_r{rep}_{first}';rows.append(rollout(out,tid,'conflict',n,t,first=first));save(out/'OUTCOMES.json',rows)
 t.close()

if __name__=='__main__':
 {'prepare':make_new,'freeze':freeze,'pilot':lambda:run_old('pilot01'),'pilot02':lambda:run_old('pilot02'),'pilot03':lambda:run_old('pilot03'),'old':lambda:run_old('old01'),'new':run_new}[sys.argv[1]]()
