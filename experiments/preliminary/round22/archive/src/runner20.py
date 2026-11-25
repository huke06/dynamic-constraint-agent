import sys,json,time
sys.dont_write_bytecode=True
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from construct20 import R,read,save,sha
from world20 import World,dump
from transport20 import Transport,AGENT_ROLES
from prompts20 import DECISION,SEMANTIC,UNIFIED,QUESTION
from exchange_core import packed
POLICY=(R/'configs/official_policy.md').read_text('utf-8')
def model(t,w,role,trigger,system,payload):return t.json([{'role':'system','content':system},{'role':'user','content':packed(payload)}],role,trigger)
def validate_job(w,d):
 if not d.get('expected') or not d.get('reason'):raise ValueError('Work needs explicit evidence basis and expected completion.')
 if not all(isinstance(i,int) and 0<=i<len(w.history) for i in d.get('evidence_refs',[])):raise ValueError('Evidence refs must be valid integer history indices.')
 k=d['work_type'];obj=d['object']
 if k=='clarify' and obj not in w.cfg['scope']:raise ValueError('Clarification object must be an original scope item.')
 if k in ('prepare','confirm','submit','stop') and obj!=w.cfg['order_id']:raise ValueError('Combined plan work object is the exact order.')
def semantic(w,t,trace,trigger='new_user_reply_requires_semantics'):
 before=w.export();result=model(t,w,'semantic',trigger,SEMANTIC,w.local())
 try:w.apply(result)
 except ValueError as ex:w.feedback.append({'kind':'semantic_rejection','reason':str(ex),'output':result})
 trace.append({'module':'semantic_update','trigger_reason':trigger,'model_output':result,'before':before,'after':w.export()});return result
def question(w,t,d,trace):
 i=d['object'];v=d['parameters']['variant_id'];payload={'work_instruction':d,'original_item':w.item(i),'offered_variant':w.variant(i,v),'latest_request':w.history[w.permission_sources[i]],'evidence_ref':w.core.product_refs.get(w.item(i)['product_id'])};result=model(t,w,'semantic','clarification_text_needed_for_selected_item',QUESTION,payload);trace.append({'module':'semantic_question','trigger_reason':'clarification_text_needed_for_selected_item','model_output':result,'visible_input':payload})
 if result.get('offered_variant_id')!=v:raise ValueError('Semantic execution changed the selected offer.')
 return result['question']
def do(w,d,trace,q=None,trigger='model_selected_work'):
 validate_job(w,d);e=w.perform(d,q);e.update(module='program_execution',trigger_reason=trigger);trace.append(e)
 if w.event_export:trace.append({'module':'public_change','snapshot':w.event_export});w.event_export=None
 return e
def automatic(w,trace):
 if w.pending or w.needs_review:return False
 missing=[w.item(i)['product_id'] for i in w.cfg['scope'] if not w.product(i)]
 if missing:
  for p in dict.fromkeys(missing):do(w,{'work_type':'query','object':p,'parameters':{},'evidence_refs':[],'expected':'formal_product_observation','reason':'Known product ID and missing catalogue make acquisition determinate.'},trace,trigger='known_query_parameters_missing_evidence')
  return True
 if any(w.stock(i)is not True for i in w.cfg['scope']):return False
 if not w.current_plan():do(w,{'work_type':'prepare','object':w.cfg['order_id'],'parameters':{},'evidence_refs':[],'expected':'current_combined_proposal','reason':'All current item parameters/stock known; calculation is deterministic.'},trace,trigger='all_parameters_determined_compute_combined_plan');return True
 if not w.current_auth():do(w,{'work_type':'confirm','object':w.cfg['order_id'],'parameters':{},'evidence_refs':[],'expected':'actual_user_reply','reason':'Current complete proposal is ready; ask user directly.'},trace,trigger='program_plan_ready_direct_confirmation');return True
 do(w,{'work_type':'submit','object':w.cfg['order_id'],'parameters':{},'evidence_refs':[],'expected':'one_registered_exchange','reason':'Current parsed full-plan authorization and all program checks satisfied.'},trace,trigger='current_authorization_allows_deterministic_submission');return True
def rollout(cfg,version,group,n,t,out):
 w=World(cfg,version,t);t.branch=n;t.world=w;trace=[];error=None;start=time.perf_counter();save(out/(n+'_start.json'),w.export());initial=True;repeated={}
 try:
  for tick in range(40):
   if w.writes or w.stopped:break
   if min(w.remaining_budget.values())<=0:error='budget_exhausted';break
   if group=='ondemand':
    if w.pending:
     semantic(w,t,trace)
     if w.pending or w.needs_review:
      repeated['unresolved_semantics']=repeated.get('unresolved_semantics',0)+1
      if repeated['unresolved_semantics']>=3:error='repeated_unresolved_semantics';break
     else:repeated['unresolved_semantics']=0
     continue
    if not initial and automatic(w,trace):continue
    d=model(t,w,'cognitive','initial_goal_work_selection' if initial else 'multiple_options_or_unmet_permission',DECISION+'\n'+POLICY,w.state());trace.append({'module':'cognitive_decision','trigger_reason':'initial_goal_work_selection' if initial else 'multiple_options_or_unmet_permission','model_output':d,'visible_state':w.state()});initial=False
    if d['work_type']=='analyze':semantic(w,t,trace,'local_conflict_requires_interpretation');continue
    q=question(w,t,d,trace) if d['work_type']=='clarify' else None;e=do(w,d,trace,q)
   else:
    before=w.export();d=model(t,w,'unified','unified_decision_semantics_execution_entry',UNIFIED+'\n'+POLICY,w.state());trace.append({'module':'unified_decision','trigger_reason':'unified_decision_semantics_execution_entry','model_output':d,'visible_state':w.state()})
    try:w.apply(d)
    except ValueError as ex:w.feedback.append({'kind':'semantic_rejection','reason':str(ex),'output':d});continue
    e=do(w,d,trace,d.get('question'))
   if not e['allowed']:
    key=packed([e['job']['work_type'],e['job']['object'],e['rejection_reason']]);repeated[key]=repeated.get(key,0)+1
    if repeated[key]>=3:error='repeated_same_rejected_work';break
   save(out/(n+'_trajectory.json'),trace)
  if not(w.writes or w.stopped):error=error or 'loop_limit_without_terminal'
 except Exception as ex:
  from logging16 import sanitize
  error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'module':'failure','error':error,'state':w.export()})
 save(out/(n+'_trajectory.json'),trace);save(out/(n+'_final.json'),w.export());result={'id':n,'task_id':cfg['task_id'],'group':group,'version':version,'tier':cfg['tier'],'error':error,'writes':len(w.writes),'event_triggered':w.change is not None,'wall_seconds':time.perf_counter()-start};print(result,flush=True);return result
def run_stage1(pilot=False, pilot_name='pilot02'):
 fpath=R/'configs/freeze_stage1.json'
 if not pilot:assert all(sha(R/k)==v for k,v in read(fpath)['files'].items())
 out=R/('results/'+pilot_name if pilot else 'results/stage1');out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);results={}
 for tid in (('0',) if pilot else ('0','58','95','106')):
  for ver in (('changed',) if pilot else ('stable','changed')):
   for rep in ((1,) if pilot else (1,2)):
    for g in (('unified','ondemand') if rep==1 else ('ondemand','unified')):
     n=f't{tid}_{ver}_r{rep}_{g}';results[n]=rollout(read(R/f'configs/stage1/{tid}/case.json'),ver,g,n,t,out);save(out/'results.json',results)
 t.close()
def freeze():
 from tests20 import check
 save(R/'configs/offline.json',check());files={str(p.relative_to(R)):sha(p) for folder in ('src','configs') for p in (R/folder).rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name not in ('freeze_stage1.json','freeze_stage2.json')};oldpath=R.parent/'19_官方Agent基线与上下文精简';old=read(oldpath/'configs/freeze.json')['read_only_sources'];old.update({str(p):sha(p) for p in oldpath.rglob('*') if p.is_file() and '__pycache__'not in p.parts});save(R/'configs/freeze_stage1.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files,'read_only_sources':old})
if __name__=='__main__':{'pilot':lambda:run_stage1(True),'stage1':run_stage1,'freeze':freeze}[sys.argv[1]]()
