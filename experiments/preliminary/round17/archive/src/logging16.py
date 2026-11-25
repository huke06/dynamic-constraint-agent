import json,time,re
from copy import deepcopy
import baseline_runner as b
def sanitize(text,secret=None):
 text=str(text)
 if secret:text=text.replace(secret,'[REDACTED]')
 text=re.sub(r'(?i)(bearer\s+|api[_-]?key[=: ]+)[^\s,;]+',r'\1[REDACTED]',text)
 text=re.sub(r'sk-[A-Za-z0-9_-]+','[REDACTED]',text)
 return text[:800]
def diagnostic(ex,secret=None):
 name=type(ex).__name__;status=getattr(ex,'status_code',None);response=getattr(ex,'response',None);headers=getattr(response,'headers',{}) or {}
 if 'timeout' in name.lower() or isinstance(ex,TimeoutError):kind='request_timeout'
 elif status is not None:kind='service_error'
 elif any(w in name.lower() for w in ('connection','network','connecterror')):kind='network_error'
 else:kind='transport_or_client_error'
 return {'kind':kind,'exception_type':name,'summary':sanitize(ex,secret),'status_code':status,'request_id':getattr(ex,'request_id',None) or headers.get('x-request-id') or headers.get('request-id'),'retry_after':headers.get('retry-after')}
def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
 if case and (case.remaining_budget['agent_calls']<=0 or case.remaining_budget['agent_tokens']<=0):raise ValueError('Agent request budget exhausted')
 if case:case.remaining_budget['agent_calls']-=1
 row={'branch':branch,'category':category,'stage':stage,'messages':deepcopy(messages),'max_tokens':max_tokens,'temperature':0,'thinking':False,'retries':0,'started':time.time(),'usage':None}
 started=time.perf_counter();self.request_events.write(json.dumps({'event':'request_started',**row},ensure_ascii=False)+'\n');self.request_events.flush()
 try:
  try:
   response=self.client.client.chat.completions.create(model=b.MODEL,messages=messages,max_tokens=max_tokens,temperature=0,extra_body={'thinking':{'type':'disabled'}})
   row['response']=response.model_dump(exclude_none=True);row['usage']=row['response'].get('usage');row['provider_request_id']=getattr(response,'_request_id',None)
  except Exception as ex:row['diagnostic']=diagnostic(ex,getattr(self.client,'secret',None));raise RuntimeError(row['diagnostic']['kind']) from None
  if case:
   if row['usage'] is not None:case.remaining_budget['agent_tokens']-=row['usage']['total_tokens']
   else:case.remaining_budget['unknown_usage_attempts']=case.remaining_budget.get('unknown_usage_attempts',0)+1
  try:
   text=row['response']['choices'][0]['message']['content'];parsed=text if stage=='worker' else b.parse(text)
   if stage!='worker' and not isinstance(parsed,dict):raise ValueError('JSON response must be an object')
  except Exception as ex:row['diagnostic']={'kind':'response_parse_error','exception_type':type(ex).__name__,'summary':sanitize(ex)};raise RuntimeError('response_parse_error') from None
  row['status']='success';return parsed
 finally:
  row['seconds']=time.perf_counter()-started
  if 'status'not in row:row['status']='failed'
  self.rows.append(row);self.stream.write(json.dumps(row,ensure_ascii=False)+'\n');self.stream.flush()
  self.request_events.write(json.dumps({'event':'request_finished','branch':branch,'stage':stage,'status':row['status'],'diagnostic':row.get('diagnostic'),'usage':row['usage']},ensure_ascii=False)+'\n');self.request_events.flush()
def install():b.Client.ask=ask
