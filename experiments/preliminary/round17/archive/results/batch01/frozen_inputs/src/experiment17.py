import sys,json,hashlib,traceback,time
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import experiment15 as base
import helmet17
import logging16
logging16.install()
shared=base.shared;b=base.b
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Client(base.interface14.Client):
 def __init__(self,out,responses):super().__init__(out,responses);self.request_events=(out/'request_events.jsonl').open('w',encoding='utf-8')
 def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
  if category=='environment_user':
   wid,c=self.pending[branch];assert c.history[-1]['role']=='assistant'
   stock=c.core.products['8940227892']['variants']['3892645120']['available']
   if wid=='clarify' and stock is None:
    reply={'reply':'Please verify the stock of the 10x variant first. My existing acceptance is conditional on it being in stock; I have not decided to accept a lower-zoom substitute yet.','allowed_alternative':False,'confirmed':False};key='pending_stock_clarification'
   elif wid=='confirm':
    p=c.plan;assert p and p['arguments']['new_item_ids']==[c.goal['alternative_permission']]
    assert c.core.compile(p['arguments'])['fingerprint']==p['quote']['fingerprint']
    reply={'reply':'I explicitly approve this exact complete proposal: '+json.dumps({'arguments':p['arguments'],'difference':p['quote']['difference']},ensure_ascii=False)+'. This is the only exchange item; please submit exactly this plan using my same PayPal account.','allowed_alternative':True,'confirmed':True};key='confirm_current_plan'
   else:return super().ask(branch,category,stage,messages,max_tokens,case)
   row={'branch':branch,'trigger_work':wid,'trigger_assistant_ref':len(c.history)-1,'private_response_key':key,'reply':reply,'model_calls':0};self.events.append(row);self.controlled_stream.write(json.dumps(row,ensure_ascii=False)+'\n');self.controlled_stream.flush();return reply
  return super().ask(branch,category,stage,messages,max_tokens,case)
 def close(self):super().close();self.request_events.close()
def load(state):return helmet17.construct(state)
def environment(state):return helmet17.environment(state)

def offline():
 from tests17 import check
 save(ROOT/'configs/offline.json',check())
def freeze():
 offline();files={str(p.relative_to(ROOT)):sha(p) for folder in ('src','configs') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='freeze.json'};save(ROOT/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files})
def execute():
 out=ROOT/'results/batch01';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();f=read(ROOT/'configs/freeze.json');assert all(sha(ROOT/p)==v for p,v in f['files'].items());save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()})
 client=helmet17.Client(out,{});b.USER_SEMANTICS=shared.SEMANTICS;policy=(HERE/'scenarios/official_policy.md').read_text('utf-8')+'\nCurrent contracts alone define execution gates. Historical compatibility is context only. Not-yet-accepted is not a refusal. Variant permission is not current-plan authorization.';cfg=shared.old.load('70')['config'];results={}
 for state in ('known_out','unknown_out','unknown_in'):
  for rep in (1,2):
   for group in (('direct','candidate') if rep==1 else ('candidate','direct')):
    n=f't70_r{rep}_{state}_{group}';c=load(state);db=environment(state);tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)));entries=[];feedback=[];error=None;client.private_branches[n]='accept'
    # Actual private DB is kept outside the Agent; initial public snapshots are identical for both unknown conditions.
    save(out/(n+'_start.json'),{'state':c.state(),'public_view':c.compact(),'budget':c.remaining_budget});save(out/(n+'_environment.json'),db)
    try:
     for turn in range(12):
      if c.writes or getattr(c,'user_declined',False) or c.remaining_budget['work_steps']<=0:break
      try:decision,u=shared.decide(c,client,n,group,policy,feedback)
      except Exception as ex:
       detail=getattr(ex,'feedback',None);entry={'turn':turn,'before':c.state(),'kind':'program_rejection' if detail else 'request_or_format_failure','diagnostic':detail or {'summary':logging16.sanitize(ex)}};entries.append(entry);feedback=[entry];save(out/(n+'_trajectory.json'),entries);continue
      if u['z']['work_id']=='clarify':base.base.recovery13.begin(c)
      entry=shared.old.work(c,u,client,n,tools,policy);entry.update(turn=turn,decision=decision);entries.append(entry);feedback=[{'work':u['z']['work_id'],'completed':entry['completion_satisfied'],'result':entry.get('result'),'clarification':getattr(c,'last_clarification_outcome',None)}];save(out/(n+'_trajectory.json'),entries)
     if not c.writes:error='no_write_at_budget_or_user_stop'
    except Exception as ex:error=type(ex).__name__+': '+logging16.sanitize(ex);entries.append({'error':error,'state_at_error':c.state()})
    save(out/(n+'_trajectory.json'),entries);save(out/(n+'_final_state.json'),c.state());save(out/(n+'_database.json'),tools.db.model_dump(mode='json'));results[n]={'id':n,'error':error,'writes':c.writes,'steps':c.steps};save(out/'results.json',results);print(n,'writes',len(c.writes),'error',error,flush=True)
 client.close();save(out/'integrity.json',{'frozen_unchanged':all(sha(ROOT/p)==v for p,v in f['files'].items())})
if __name__=='__main__':{'offline':offline,'freeze':freeze,'execute':execute}[sys.argv[1]]()
