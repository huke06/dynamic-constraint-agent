import sys,json,hashlib,time
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import baseline_runner as b
import logging16
from world18 import World
from construct18 import read,save,sha
R=Path(__file__).resolve().parent.parent
class Client:
 def __init__(self,out):
  out.mkdir(parents=True,exist_ok=True);self.client=b.DeepSeek(model=b.MODEL,timeout=60);self.rows=[];self.stream=(out/'model_calls.jsonl').open('w',encoding='utf-8');self.request_events=(out/'request_events.jsonl').open('w',encoding='utf-8')
 ask=logging16.ask
 def close(self):self.stream.close();self.request_events.close()
def messages(w,group):
 prompts=read(R/'configs/prompts.json');payload={'interaction_history':w.history,'remaining_budget':w.remaining_budget}
 if group!='free':payload['framework_state']=w.visible_state()
 if group=='framework':payload['candidate_work']=w.candidates()
 return [{'role':'system','content':prompts['common']+'\n'+prompts[group]+'\n'+(R/'configs/official_policy.md').read_text('utf-8')},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}]
def roll(w,group,name,client,out):
 save(out/(name+'_start.json'),w.export());trace=[];error=None
 for turn in range(12):
  if w.writes or w.stopped:break
  if min(w.remaining_budget.values())<=0: error='budget_exhausted';break
  before=w.export()
  try:
   d=client.ask(name,'agent','controller',messages(w,group),max_tokens=1300,case=w)
   if not isinstance(d.get('action'),str) or not isinstance(d.get('reason'),str) or not isinstance(d.get('claims'),list):raise ValueError('Action/reason/claims schema required.')
   e=w.execute(d);e['turn']=turn;trace.append(e)
   if w.event_export:
    save(out/(name+'_event_snapshot.json'),w.event_export);w.event_export=None
  except Exception as ex:
   error=logging16.sanitize(ex,getattr(client.client,'secret',None));trace.append({'turn':turn,'request_or_schema_error':error,'before':before,'after':w.export()})
  save(out/(name+'_trajectory.json'),trace)
 if not(w.writes or w.stopped):error=error or 'decision_limit_without_terminal_result'
 save(out/(name+'_trajectory.json'),trace);save(out/(name+'_final.json'),w.export());return {'id':name,'group':group,'terminal':bool(w.writes or w.stopped),'error':error,'event_triggered':bool(w.event),'steps':w.steps,'attempted_decisions':len(trace),'writes':len(w.writes)}
def freeze():
 from tests18 import check
 from check_additional18 import check as additional
 save(R/'configs/offline.json',check());save(R/'configs/additional_offline.json',additional());files={str(p.relative_to(R)):sha(p) for folder in ('src','configs') for p in (R/folder).rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='freeze.json'}
 protected={}
 for num in range(1,18):
  folder=next(p for p in R.parent.iterdir() if p.is_dir() and p.name.startswith(f'{num:02}_'))
  protected.update({str(p):sha(p) for p in folder.rglob('*') if p.is_file() and '__pycache__'not in p.parts})
 for p in (b.DATA/'db.json',b.DATA/'tasks.json',b.DATA/'policy.md',b.REPO/'src/tau2/domains/retail/tools.py',Path('D:/experimentn/exp2layer/llm.py')):protected[str(p)]=sha(p)
 old10=R.parent/'10_程序事实核验与续行验证/results/20261123T001740331845Z/freeze.json'
 for name in read(old10)['protected']:
  if '申报' in name and Path(name).suffix.lower() in ('.docx','.md'):protected[name]=sha(Path(name))
 save(R/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files,'read_only_sources':protected})
def execute():
 f=read(R/'configs/freeze.json');assert all(sha(R/p)==v for p,v in f['files'].items());out=R/'results/main';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});client=Client(out);results={}
 for tid in read(R/'configs/tasks.json'):
  cfg=read(R/f'configs/tasks/{tid}/adapted.json')
  for version in ('stable','changed'):
   for rep in (1,2):
    for group in (('free','framework') if rep==1 else ('framework','free')):
     n=f't{tid}_{version}_r{rep}_{group}';results[n]=roll(World(cfg,version),group,n,client,out);save(out/'results.json',results);print(json.dumps(results[n]),flush=True)
 client.close();save(out/'finished.json',{'utc':datetime.now(timezone.utc).isoformat(),'frozen_unchanged':all(sha(R/p)==v for p,v in f['files'].items())})
def diagnostic():
 f=read(R/'configs/freeze.json');assert all(sha(R/p)==v for p,v in f['files'].items());out=R/'results/exploratory';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat(),'not_primary_experiment':True});client=Client(out);results={}
 for tid in ('6','75'):
  src=R/f'results/main/t{tid}_changed_r1_framework_event_snapshot.json'
  if not src.exists():results[tid]={'not_started':'source event not reached'};continue
  snap=read(src);save(out/f't{tid}_common_snapshot.json',snap)
  for group in ('state_direct','framework'):
   n=f'diag_t{tid}_{group}';w=World.restore(snap);results[n]=roll(w,group,n,client,out);save(out/'results.json',results);print(json.dumps(results[n]),flush=True)
 client.close()
if __name__=='__main__':{'freeze':freeze,'execute':execute,'diagnostic':diagnostic}[sys.argv[1]]()
