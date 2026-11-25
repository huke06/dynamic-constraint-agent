import sys,json,hashlib,shutil,traceback
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import experiment13 as base
import interface14
interface14.install()
b=base.b;shared=base.shared
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def offline():
 from tests14 import check
 save(ROOT/'configs/offline.json',check())
def freeze():
 offline();files={str(p.relative_to(ROOT)):sha(p) for folder in ('src','configs') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='freeze.json'}
 save(ROOT/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files})
def execute():
 out=ROOT/'results/batch01';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();f=read(ROOT/'configs/freeze.json');assert all(sha(ROOT/p)==v for p,v in f['files'].items());save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()})
 client=interface14.Client(out,read(ROOT/'configs/private_responses.json'));b.WORKER=shared.old.WORKER;b.USER_PROMPT=shared.old.USER_PROMPT;b.USER_SEMANTICS=shared.SEMANTICS
 cfg=shared.old.load('52')['config'];policy=(HERE/'scenarios/official_policy.md').read_text('utf-8');db=read(HERE/'scenarios/initial_database.json');results={}
 for mode in ('accept','reject','ambiguous'):
  for group in ('direct','candidate'):
   n=f't52_r1_{mode}_{group}';c=base.load_start();tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)));entries=[];feedback=[];error=None;client.private_branches[n]=mode
   save(out/(n+'_start.json'),c.snapshot(db,{'source':'event-triggered controlled response table external to Agent state; branch selected only in simulator'}))
   try:
    for turn in range(12):
     if c.writes or getattr(c,'user_declined',False) or c.remaining_budget['work_steps']<=0:break
     try:decision,u=shared.decide(c,client,n,group,policy,feedback)
     except Exception as ex:
      detail=getattr(ex,'feedback',{'error':str(ex)});entries.append({'turn':turn,'before':c.state(),'rejection':str(ex),'selected_work_feedback':detail,'repeat_of_previous_rejection':bool(entries and entries[-1].get('selected_work_feedback')==detail)});feedback=[detail];save(out/(n+'_trajectory.json'),entries);continue
     if u['z']['work_id']=='clarify':base.recovery13.begin(c)
     e=shared.old.work(c,u,client,n,tools,policy);e.update(turn=turn,decision=decision)
     if u['z']['work_id']=='clarify':e['clarification_resolution']=deepcopy(getattr(c,'last_clarification_outcome',None))
     entries.append(e);feedback=[{'work':u['z']['work_id'],'completed':e['completion_satisfied'],'result':e.get('result'),'current_reply_clarification':e.get('clarification_resolution')}];save(out/(n+'_trajectory.json'),entries)
    if not c.writes and not getattr(c,'user_declined',False):error='work/decision budget exhausted'
   except Exception as ex:error=type(ex).__name__+': '+str(ex);entries.append({'error':error,'state_at_error':c.state(),'traceback':traceback.format_exc()})
   done=[e for e in entries if 'u'in e];r=shared.old.scores(c,tools,cfg,done)
   r.update(error=error,branch=n,start_sha256=b.hash_value(read(out/(n+'_start.json'))),user_declined=getattr(c,'user_declined',False),clarification_outcomes=getattr(c,'clarification_outcomes',[]))
   save(out/(n+'_trajectory.json'),entries);save(out/(n+'_final_state.json'),c.state());save(out/(n+'_database.json'),tools.db.model_dump(mode='json'));save(out/(n+'_result.json'),r);results[n]=r;save(out/'results.json',results);print(n,'write',r['R_write'],'declined',r['user_declined'],'error',error,flush=True)
 client.close();save(out/'integrity.json',{'frozen_unchanged':all(sha(ROOT/p)==v for p,v in f['files'].items())})
if __name__=='__main__':{'offline':offline,'freeze':freeze,'execute':execute}[sys.argv[1]]()
