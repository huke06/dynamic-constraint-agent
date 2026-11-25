"""Synthetic transport failures; no online requests and no credentials logged."""
from types import SimpleNamespace as NS
from unittest.mock import patch
from construct20 import R,save
from transport20 import Transport
from logging16 import diagnostic

def check():
 checks={};root=R/'results/offline_logging';root.mkdir(exist_ok=True)
 class NetworkError(Exception):pass
 class ServiceError(Exception):
  status_code=503;request_id='synthetic-request-503';response=NS(headers={})
 checks['timeout_separate']=diagnostic(TimeoutError())['kind']=='request_timeout'
 checks['network_separate']=diagnostic(NetworkError())['kind']=='network_error'
 checks['service_status_request_id']=diagnostic(ServiceError())['status_code']==503 and diagnostic(ServiceError())['request_id']=='synthetic-request-503'
 checks['summary_redacted']='sk-secret'not in diagnostic(NetworkError('api_key=sk-secret'))['summary']
 for scenario,seq in [('retry',[TimeoutError('synthetic'),{}]),('parse',[{'not_json':True}])]:
  def create(**kwargs):
   value=seq.pop(0)
   if isinstance(value,Exception):raise value
   return NS(model_dump=lambda **kwargs:{'id':'synthetic','model':'synthetic','choices':[{'message':{'content':'not JSON' if value else '{}'}}]})
  fake=NS(client=NS(chat=NS(completions=NS(create=create))),secret=None)
  with patch('transport20.b.DeepSeek',return_value=fake),patch('transport20.time.sleep'):
   t=Transport(root/scenario);t.branch='synthetic';t.world=NS(remaining_budget={'calls':40,'tokens':180000},unknown_usage=0)
   try:t.json([{'role':'user','content':'synthetic'}],'unified','offline_logging_test')
   except RuntimeError:pass
   if scenario=='retry':
    checks['identical_one_retry']=len(t.calls)==2 and t.calls[0]['messages']==t.calls[1]['messages']
    checks['failed_and_no_returned_usage_unknown']=all(x['usage']is None for x in t.calls) and t.world.unknown_usage==2
    checks['unified_attempts_debit_budget']=t.world.remaining_budget['calls']==38
   else:checks['parse_error_no_retry']=len(t.calls)==1 and 'response_parse_error'in(root/scenario/'request_events.jsonl').read_text('utf-8')
   t.close()
 assert all(checks.values()),checks
 save(root/'CHECKS.json',{'passed':True,'checks':checks,'online_requests':0});return checks

if __name__=='__main__':print(check())
