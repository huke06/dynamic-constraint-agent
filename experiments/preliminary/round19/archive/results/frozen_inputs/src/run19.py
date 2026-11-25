import sys,json,hashlib
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from construct18 import R,read,save,sha
from world19 import World,dump
from user19 import User
from exchange_core import packed
from transport19 import Transport
from tau2.agent.llm_agent import LLMAgent
from tau2.data_model.message import AssistantMessage,UserMessage,ToolMessage,ToolCall,MultiToolMessage
def typed(m):
 if m['role']=='user':return UserMessage(role='user',content=m['content'])
 if m['role']=='tool':return ToolMessage(role='tool',id=m['tool_call_id'],content=m['content'])
 return AssistantMessage(role='assistant',content=m.get('content'),tool_calls=[ToolCall(id=t['id'],name=t['function']['name'],arguments=json.loads(t['function']['arguments'])) for t in m.get('tool_calls',[])] or None)
def native_check(w,args):
 valid=False
 try:valid=w.user.authorization(args)
 except (KeyError,ValueError):pass
 return {'active_request':not w.withdrawn,'current_spec_scope_payment':args==w.args(),'independent_user_authorization':valid,'all_valid':bool(not w.withdrawn and args==w.args() and valid)}
def native(w,tc,framework=False):
 before=w.export();check=native_check(w,tc.arguments) if tc.name=='exchange_delivered_order_items' else None;error=None;result=None
 try:
  if framework and tc.name=='exchange_delivered_order_items':
   result=w.execute({'action':'submit','parameters':{'arguments':tc.arguments},'reason':'native tool request','claims':[]});result.update(native_tool=tc.name,parameters=deepcopy(tc.arguments),policy_check_without_interception=check,actual_native_executed=result['check']['allowed']);return result
  result=dump(w.tools.use_tool(tc.name,**tc.arguments))
  ref=len(w.history);w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)});w.core.observe(tc.name,tc.arguments,result,ref)
  if tc.name=='exchange_delivered_order_items':w.writes.append({'arguments':deepcopy(tc.arguments),'result':result,'independent_authorization_check':check,'history_ref':ref})
 except Exception as ex:
  error=str(ex);result={'error':error};w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)})
 w.steps+=1;w.remaining_budget['work_steps']-=1;w.checks.append({'action':'native:'+tc.name,'parameters':deepcopy(tc.arguments),'allowed':error is None,'reason':error})
 if framework:w.raw_evidence=[{'ref':len(w.history)-1,'record':deepcopy(w.history[-1])}]
 return {'native_tool':tc.name,'parameters':tc.arguments,'before':before,'policy_check_without_interception':check,'actual_native_executed':error is None,'result':result,'native_error':error,'after':w.export()}
def fw_messages(w,mode):
 prompts=read(R/'configs/prompts19.json')
 if mode=='original':payload={'interaction_history':w.history,'remaining_budget':w.remaining_budget,'framework_state':w.visible_state(),'candidate_work':w.candidates()}
 else:payload=w.compact()
 return [{'role':'system','content':prompts['framework']+'\n'+(R/'configs/official_policy.md').read_text('utf-8')},{'role':'user','content':packed(payload)}]
def schemas(w):return [t.openai_schema for t in w.tools.get_tools().values()]
def roll(w,group,name,t,out,mode='compact',stop_after_write=False):
 t.branch=name;t.world=w;w.user=User(w,t);w.raw_evidence=[];trace=[];error=None;save(out/(name+'_start.json'),w.export())
 if group=='official':
  agent=LLMAgent(tools=list(w.tools.get_tools().values()),domain_policy=(R/'configs/official_policy.md').read_text('utf-8'),llm='deepseek-flash',llm_args={'temperature':0,'max_tokens':1300,'num_retries':0});hist=[typed(m) for m in w.history];state=agent.get_init_state(hist[:-1]);incoming=hist[-1]
 for turn in range(12):
  if w.stopped or (stop_after_write and w.writes):break
  if w.remaining_budget['work_steps']<=0 or w.remaining_budget['agent_calls']<=0 or w.remaining_budget['agent_tokens']<=0:error='budget_exhausted';break
  try:
   if group=='official':
    before=w.export();msg,state=agent.generate_next_message(incoming,state);api={'role':'assistant','content':msg.content}
    if msg.tool_calls:api['tool_calls']=[{'id':tc.id,'type':'function','function':{'name':tc.name,'arguments':packed(tc.arguments)}} for tc in msg.tool_calls]
    ar=len(w.history);w.history.append(api)
    if msg.tool_calls:
     ts=[]
     for tc in msg.tool_calls:
      e=native(w,tc);e.update(turn=turn,assistant_message=msg.model_dump(mode='json'),assistant_ref=ar);trace.append(e);ts.append(ToolMessage(role='tool',id=tc.id,content=packed(e['result']),error=e['native_error']is not None))
     incoming=MultiToolMessage(role='tool',tool_messages=ts)
    else:
     rec=w.user.respond(msg.content or '',ar);w.steps+=1;w.remaining_budget['work_steps']-=1
     if rec['trigger_due']:w.trigger()
     if rec['terminal']:w.stopped=True
     e={'turn':turn,'assistant_message':msg.model_dump(mode='json'),'assistant_ref':ar,'before':before,'user_record':rec,'after':w.export()};trace.append(e)
     if rec['trigger_due']:
      state.messages.append(UserMessage(role='user',content=rec['reply']));incoming=UserMessage(role='user',content=w.event['public_content'])
     else:incoming=UserMessage(role='user',content=rec['reply'])
   else:
    before=w.export();res=t.request(fw_messages(w,mode),schemas(w));w.raw_evidence=[];message=res['choices'][0]['message']
    if message.get('tool_calls'):
     for tc in message['tool_calls']:
      obj=ToolCall(id=tc['id'],name=tc['function']['name'],arguments=json.loads(tc['function']['arguments']));w.history.append({'role':'assistant','content':message.get('content'),'tool_calls':[tc]});e=native(w,obj,framework=True);trace.append(e)
    else:
     d=json.loads(message['content']);prior=native_check(w,d['parameters']['arguments']) if d['action']=='submit' else None;e=w.execute(d);e.update(turn=turn,independent_authorization_check=prior);trace.append(e)
     if d['action']=='stop' and e['check']['allowed']:
      text='The exchange request is registered; the order status is exchange requested.' if w.writes else 'I will stop the exchange and keep your original order unchanged.';ar=len(w.history);w.history.append({'role':'assistant','content':text});e['closing_text']=text;e['after']=w.export()
   if w.event_export:save(out/(name+'_event_snapshot.json'),w.event_export);w.event_export=None
   save(out/(name+'_trajectory.json'),trace)
  except Exception as ex:
   from logging16 import sanitize
   error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'turn':turn,'request_or_program_error':error,'before':w.export()});break
 if not w.stopped and not(stop_after_write and w.writes):error=error or 'turn_limit_without_terminal'
 save(out/(name+'_trajectory.json'),trace);save(out/(name+'_final.json'),{'world':w.export(),'controlled_user':w.user.export()});return {'id':name,'group':group,'mode':mode,'error':error,'writes':len(w.writes),'stopped':w.stopped,'event_triggered':bool(w.event),'operations':w.steps}
def pilot():
 out=R/'results/pilot01';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);t.install();results={}
 for tid,ver in [('6','stable'),('27','changed')]:
  n=f'pilot_t{tid}_{ver}';results[n]=roll(World(read(R/f'configs/tasks/{tid}/adapted.json'),ver),'official',n,t,out);save(out/'results.json',results);print(results[n],flush=True)
 t.close()
def pilot_framework():
 out=R/('results/pilot03' if (R/'results/pilot02/started.json').exists() else 'results/pilot02');out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);n='pilot_t27_compact_framework';result=roll(World(read(R/'configs/tasks/27/adapted.json'),'changed'),'framework',n,t,out);save(out/'results.json',{n:result});t.close();print(result)
def freeze():
 from tests19 import check
 save(R/'configs/offline.json',check());files={str(p.relative_to(R)):sha(p) for folder in ('src','configs') for p in (R/folder).rglob('*') if p.is_file() and '__pycache__'not in p.parts and p.name!='freeze.json'}
 previous=R.parent/'18_动态约束下完整框架对照';old=read(previous/'configs/freeze.json')['read_only_sources'];old.update({str(p):sha(p) for p in previous.rglob('*') if p.is_file() and '__pycache__'not in p.parts});old.update({str(p):sha(p) for p in (Path('D:/experimentn/tau2-official/src/tau2/agent/llm_agent.py'),Path('D:/experimentn/tau2-official/src/tau2/utils/llm_utils.py'))});save(R/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files,'read_only_sources':old})
def execute():
 f=read(R/'configs/freeze.json');assert all(sha(R/p)==v for p,v in f['files'].items());out=R/'results/main';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);t.install();results={}
 for tid in read(R/'configs/tasks.json'):
  for ver in ('stable','changed'):
   for rep in (1,2):
    for group in (('official','framework') if rep==1 else ('framework','official')):
     n=f't{tid}_{ver}_r{rep}_{group}';results[n]=roll(World(read(R/f'configs/tasks/{tid}/adapted.json'),ver),group,n,t,out);save(out/'results.json',results);print(results[n],flush=True)
 t.close();save(out/'finished.json',{'utc':datetime.now(timezone.utc).isoformat()})
def diagnostic():
 f=read(R/'configs/freeze.json');assert all(sha(R/p)==v for p,v in f['files'].items());out=R/'results/context';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);results={}
 for tid in ('27','75'):
  for mode in ('original','compact'):
   w=World.restore(read(R/f'configs/snapshots/task{tid}.json'));w.remaining_budget={'agent_calls':24,'agent_tokens':60000,'work_steps':9};n=f'cost_t{tid}_{mode}';results[n]=roll(w,'framework',n,t,out,mode=mode,stop_after_write=True);save(out/'results.json',results);print(results[n],flush=True)
 t.close()
if __name__=='__main__':{'pilot':pilot,'pilot_framework':pilot_framework,'freeze':freeze,'execute':execute,'diagnostic':diagnostic}[sys.argv[1]]()
