import sys,json,hashlib,shutil,traceback
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import experiment12 as shared
import recovery13
recovery13.install()
import baseline_runner as b
from exchange_core import packed
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
QUOTE='If item 3892645120, the 30MP camera with CF card storage and 10x zoom, is in stock, I accept that variant. I have not accepted any lower-zoom alternative. Please check stock before making a plan.'
def construct():
 c=shared.load_start('52','known');db=read(HERE/'scenarios/initial_database.json');tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)));pid='8940227892';vid='3892645120'
 # Epistemic prefix: catalogue complete, preferred SKU stock not yet observed; alternatives unchanged.
 for i,m in enumerate(c.history):
  if m['role']=='tool':
   value=json.loads(m['content'])
   if isinstance(value,dict) and value.get('product_id')==pid:value['variants'][vid]['available']=None;m['content']=packed(value);c.core.evidence[str(i)]=deepcopy(m)
 c.core.products[pid]['variants'][vid]['available']=None
 ref=len(c.history);c.history.append({'role':'user','content':QUOTE});c.core.evidence[str(ref)]=deepcopy(c.history[-1])
 c.apply_user({'change':{'present':False},'authorization':{'approved':False},'permission_update':{'kind':'grant','variant_id':vid,'source_ref':ref,'source_quote':QUOTE}},ref-1,ref)
 pending=deepcopy(c.conditional_permission);assert pending['sat']=='未知'
 # Real simulated tool invocation, persisted in official envelope consumed by fact replay.
 query_ref=len(c.history);result=tools.get_product_details(product_id=pid).model_dump(mode='json')
 assert vid in result['variants'] and result['variants'][vid]['available'] is False
 assert result['variants']['6384525445']['available'] is True and result['variants']['7255224608']['available'] is True
 c.core.observe('get_product_details',{'product_id':pid},result,query_ref);c.resolve_conditional(query_ref);c.core.review([c.changed_item],query_ref)
 wrapper={'official_tool':'get_product_details','arguments':{'product_id':pid},'official_result':result,'source':query_ref}
 c.history.append({'role':'observation','work':'inventory','content':packed(wrapper)});c.core.evidence[str(query_ref)]=deepcopy(c.history[-1])
 c.permission_history=[pending,deepcopy(c.conditional_permission)];c.screen=None;c.steps=0;c.work=[]
 assert c.conditional_permission['sat']=='未满足' and c.goal['alternative_permission']=='unknown' and c.plan is None and not c.confirmations
 return c,db,{'user_ref':ref,'stock_query_ref':query_ref,'pending_rule':pending,'false_rule':deepcopy(c.conditional_permission),'official_tool_record':wrapper,'public_source':'Adapted public task52 history plus synthetic public conditional user message; no private fallback answer used.'}
def runtime(c):return {'case_fields':{k:deepcopy(v) for k,v in c.__dict__.items() if k!='core'},'ledger_fields':deepcopy(c.core.__dict__)}
def load_start():
 d=read(ROOT/'configs/start.json');c=shared.Case.__new__(shared.Case);c.__dict__.update(deepcopy(d['runtime']['case_fields']));c.core=shared.Ledger.__new__(shared.Ledger);c.core.__dict__.update(deepcopy(d['runtime']['ledger_fields']));assert c.state()==d['state'];return c
def offline():
 from tests13 import check
 save(ROOT/'configs/offline.json',check())
def freeze():
 c,db,evidence=construct();save(ROOT/'configs/start.json',{'state':c.state(),'runtime':runtime(c),'public_agent_view':c.compact()});save(ROOT/'configs/start_evidence.json',evidence)
 offline()
 files={str(p.relative_to(ROOT)):sha(p) for folder in ('src','configs') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='freeze.json'}
 save(ROOT/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files})
def execute():
 out=ROOT/'results/batch01';out.mkdir(exist_ok=True);assert not (out/'started.json').exists();f=read(ROOT/'configs/freeze.json');assert all(sha(ROOT/p)==v for p,v in f['files'].items())
 save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});client=recovery13.Client(out)
 b.WORKER=shared.old.WORKER;b.USER_PROMPT=shared.old.USER_PROMPT;b.USER_SEMANTICS=shared.SEMANTICS
 cfg=shared.old.load('52')['config'];b.USER_POLICY=cfg['private_user_policy'];policy=(HERE/'scenarios/official_policy.md').read_text('utf-8');db=read(HERE/'scenarios/initial_database.json');results={}
 for rep in (1,2):
  for group in (('direct','candidate') if rep==1 else ('candidate','direct')):
   n=f't52_r{rep}_recovery_{group}';c=load_start();tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)));entries=[];feedback=[];error=None
   save(out/(n+'_start.json'),c.snapshot(db,cfg['private_user_policy']))
   try:
    for turn in range(12):
     if c.writes or getattr(c,'user_declined',False) or c.remaining_budget['work_steps']<=0:break
     try:decision,u=shared.decide(c,client,n,group,policy,feedback)
     except Exception as ex:
      detail=getattr(ex,'feedback',{'error':str(ex)});entries.append({'turn':turn,'before':c.state(),'rejection':str(ex),'selected_work_feedback':detail,'repeat_of_previous_rejection':bool(entries and entries[-1].get('selected_work_feedback')==detail)});feedback=[detail];save(out/(n+'_trajectory.json'),entries);continue
     if u['z']['work_id']=='clarify':recovery13.begin(c)
     e=shared.old.work(c,u,client,n,tools,policy);e.update(turn=turn,decision=decision)
     if u['z']['work_id']=='clarify':e['clarification_resolution']=deepcopy(getattr(c,'last_clarification_outcome',None))
     entries.append(e);feedback=[{'work':u['z']['work_id'],'completed':e['completion_satisfied'],'result':e.get('result'),'current_reply_clarification':e.get('clarification_resolution')}];save(out/(n+'_trajectory.json'),entries)
    if not c.writes:error='user_declined' if getattr(c,'user_declined',False) else 'work/decision budget exhausted'
   except Exception as ex:error=type(ex).__name__+': '+str(ex);entries.append({'error':error,'state_at_error':c.state(),'traceback':traceback.format_exc()})
   done=[e for e in entries if 'u'in e];r=shared.old.scores(c,tools,cfg,done);r.update(error=error,branch=n,start_sha256=b.hash_value(read(out/(n+'_start.json'))),clarification_outcomes=getattr(c,'clarification_outcomes',[]),external_evaluation=None,C_consent_semantic=None,strict_pass=False)
   if c.writes:
    try:
     j=client.ask(n,'external_evaluation','judge',[{'role':'system','content':shared.old.JUDGE+'\n'+policy},{'role':'user','content':packed({'goal':cfg['private_user_policy'],'dialogue':[{'index':i,**m} for i,m in enumerate(c.history)],'actual_writes':c.writes,'observed_payment_method':shared.old.methods(c)})}],max_tokens=1400)
     r['external_evaluation']=j;r['C_consent_semantic']=j['consent_valid']
    except Exception as ex:r['evaluation_error']=str(ex)
   save(out/(n+'_trajectory.json'),entries);save(out/(n+'_final_state.json'),c.state());save(out/(n+'_result.json'),r);results[n]=r;save(out/'results.json',results);print(n,'write',r['R_write'],'error',error,flush=True)
 client.close();save(out/'integrity.json',{'frozen_unchanged':all(sha(ROOT/p)==v for p,v in f['files'].items())})
if __name__=='__main__':
 {'freeze':freeze,'offline':offline,'execute':execute}[sys.argv[1]]()
