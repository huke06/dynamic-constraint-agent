"""Provider/logging boundary only. Official LLMAgent and generate remain unmodified."""
import json,time
from copy import deepcopy
import baseline_runner as b
from logging16 import diagnostic,sanitize
class Transport:
 def __init__(self,out):
  out.mkdir(parents=True,exist_ok=True);self.sdk=b.DeepSeek(model=b.MODEL,timeout=60);self.calls=[];self.stream=(out/'model_calls.jsonl').open('w',encoding='utf-8');self.events=(out/'request_events.jsonl').open('w',encoding='utf-8');self.branch=None;self.world=None
 def request(self,messages,tools=None,category='agent',max_tokens=1300):
  if category=='agent':
   if self.world.remaining_budget['agent_calls']<=0 or self.world.remaining_budget['agent_tokens']<=0:raise RuntimeError('agent_request_budget_exhausted')
   self.world.remaining_budget['agent_calls']-=1
  row={'branch':self.branch,'category':category,'messages':deepcopy(messages),'tools':deepcopy(tools),'model':b.MODEL,'temperature':0,'thinking':False,'max_tokens':max_tokens,'sdk_retries':0,'application_retries':0,'usage':None,'status':'failed','started':time.time()};start=time.perf_counter();self.events.write(json.dumps({'event':'request_started',**row},ensure_ascii=False)+'\n');self.events.flush()
  try:
   kw={'model':b.MODEL,'messages':messages,'temperature':0,'max_tokens':max_tokens,'extra_body':{'thinking':{'type':'disabled'}}}
   if tools:kw.update(tools=tools,tool_choice='auto')
   res=self.sdk.client.chat.completions.create(**kw);row['response']=res.model_dump(exclude_none=True);row['usage']=row['response'].get('usage');row['provider_request_id']=getattr(res,'_request_id',None);row['status']='success'
   if category=='agent':
    if row['usage'] is None:self.world.remaining_budget['unknown_usage_attempts']=self.world.remaining_budget.get('unknown_usage_attempts',0)+1
    else:self.world.remaining_budget['agent_tokens']-=row['usage']['total_tokens']
   return row['response']
  except Exception as ex:
   row['diagnostic']=diagnostic(ex,getattr(self.sdk,'secret',None));raise RuntimeError(row['diagnostic']['kind']) from None
  finally:
   row['seconds']=time.perf_counter()-start;self.calls.append(row);self.stream.write(json.dumps(row,ensure_ascii=False)+'\n');self.stream.flush();self.events.write(json.dumps({'event':'request_finished','branch':self.branch,'category':category,'status':row['status'],'usage':row['usage'],'diagnostic':row.get('diagnostic')},ensure_ascii=False)+'\n');self.events.flush()
 def official_completion(self,**kwargs):
  from litellm import ModelResponse
  return ModelResponse(**self.request(kwargs['messages'],kwargs.get('tools')))
 def install(self):
  import tau2.utils.llm_utils as lu
  lu.completion=self.official_completion
  # Provider alias has no verified monetary price mapping; do not invent dollar costs.
  lu.get_response_cost=lambda response:None
 def close(self):self.stream.close();self.events.close()
