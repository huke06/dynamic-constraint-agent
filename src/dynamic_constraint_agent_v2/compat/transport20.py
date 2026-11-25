import json,time
from copy import deepcopy
import baseline_runner as b
from logging16 import diagnostic
AGENT_ROLES={'cognitive','semantic','evidence','unified'}
class Transport:
 def __init__(self,out):
  out.mkdir(parents=True,exist_ok=True);self.sdk=b.DeepSeek(model=b.MODEL,timeout=60);self.branch=None;self.world=None;self.calls=[];self.stream=(out/'model_calls.jsonl').open('w',encoding='utf-8');self.events=(out/'request_events.jsonl').open('w',encoding='utf-8')
 def request(self,messages,role='cognitive',trigger='unified_next_work',tools=None,max_tokens=1700):
  for attempt in range(2):
   if role in AGENT_ROLES:
    if self.world.remaining_budget['calls']<=0 or self.world.remaining_budget['tokens']<=0:raise RuntimeError('agent_budget_exhausted')
    self.world.remaining_budget['calls']-=1
   row={'branch':self.branch,'role':role,'trigger_reason':trigger,'attempt':attempt+1,'retry_rule':'one identical retry for transport/timeout/429/5xx only','messages':deepcopy(messages),'tools':deepcopy(tools),'usage':None,'status':'failed','started':time.time(),'temperature':0,'thinking':False,'max_tokens':max_tokens};start=time.perf_counter();self.events.write(json.dumps({'event':'request_started',**row},ensure_ascii=False)+'\n');self.events.flush();retry=False
   try:
    kw={'model':b.MODEL,'messages':messages,'temperature':0,'max_tokens':max_tokens,'extra_body':{'thinking':{'type':'disabled'}}}
    if tools:kw.update(tools=tools,tool_choice='auto')
    r=self.sdk.client.chat.completions.create(**kw);row['response']=r.model_dump(exclude_none=True);row['usage']=row['response'].get('usage');row['provider_request_id']=getattr(r,'_request_id',None);row['status']='success'
    if role in AGENT_ROLES:
     if row['usage']is None:self.world.unknown_usage+=1
     else:self.world.remaining_budget['tokens']-=row['usage']['total_tokens']
   except Exception as ex:
    row['diagnostic']=diagnostic(ex,getattr(self.sdk,'secret',None));d=row['diagnostic'];retry=attempt==0 and (d['kind']in ('network_error','request_timeout') or d.get('status_code')in (408,429,500,502,503,504))
    if role in AGENT_ROLES:self.world.unknown_usage+=1
   finally:
    row['seconds']=time.perf_counter()-start;self.calls.append(row);self.stream.write(json.dumps(row,ensure_ascii=False)+'\n');self.stream.flush();self.events.write(json.dumps({'event':'request_finished','branch':self.branch,'role':role,'status':row['status'],'usage':row['usage'],'diagnostic':row.get('diagnostic'),'retry_next':retry},ensure_ascii=False)+'\n');self.events.flush()
   if row['status']=='success':return row['response']
   if not retry:raise RuntimeError(row['diagnostic']['kind'])
   time.sleep(1)
 def json(self,messages,role,trigger,max_tokens=1700):
  r=self.request(messages,role,trigger,max_tokens=max_tokens)
  try:
   text=r['choices'][0]['message']['content'].strip()
   if text.startswith('```'):text=text.split('\n',1)[1].rsplit('```',1)[0]
   d=json.loads(text)
   if not isinstance(d,dict):raise ValueError('object required')
   return d
  except Exception:
   self.events.write(json.dumps({'event':'response_parse_error','branch':self.branch,'role':role,'response_id':r.get('id')})+'\n');self.events.flush();raise RuntimeError('response_parse_error') from None
 def official_completion(self,**kw):
  from litellm import ModelResponse
  return ModelResponse(**self.request(kw['messages'],'cognitive','official_next_message',kw.get('tools')))
 def install(self):
  import tau2.utils.llm_utils as lu
  lu.completion=self.official_completion;lu.get_response_cost=lambda response:None
 def close(self):self.stream.close();self.events.close()
