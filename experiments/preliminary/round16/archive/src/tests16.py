import io,json
from types import SimpleNamespace
def check():
 import experiment16 as e
 import logging16 as log
 class ServiceError(Exception):status_code=503;request_id='test-request-id';response=SimpleNamespace(headers={'retry-after':'1'})
 def fake(mode):
  def create(**kw):
   if mode=='timeout':raise TimeoutError('timeout bearer sk-SECRET')
   if mode=='network':raise ConnectionError('network sk-SECRET')
   if mode=='service':raise ServiceError('api_key=sk-SECRET')
   body={'choices':[{'message':{'content':'not json' if mode=='parse' else '{}'}}]}
   return SimpleNamespace(model_dump=lambda **kw:body,_request_id='response-test-id')
  return SimpleNamespace(client=SimpleNamespace(client=SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create))),secret='sk-SECRET'),rows=[],stream=io.StringIO(),request_events=io.StringIO())
 expected={'timeout':'request_timeout','network':'network_error','service':'service_error','parse':'response_parse_error'}
 diagnostics=[]
 for mode,kind in expected.items():
  obj=fake(mode)
  try:log.ask(obj,'test','agent','controller',[]);raise AssertionError('error accepted')
  except RuntimeError:pass
  row=obj.rows[-1];assert row['diagnostic']['kind']==kind and row['usage'] is None and 'sk-SECRET'not in json.dumps(row);diagnostics.append(row['diagnostic'])
 assert diagnostics[2]['status_code']==503 and diagnostics[2]['request_id']=='test-request-id'
 a=e.load('unknown_out');b=e.load('unknown_in');assert a.state()==b.state() and a.compact()==b.compact()
 for state,want in [('unknown_out',False),('unknown_in',True)]:
  c=e.load(state);tools=e.b.RetailTools(e.b.RetailDB.model_validate(e.environment(state)));w=next(w for w in c.candidates() if w['work_id']=='inventory');c.deterministic(c.instruction(w),tools)
  assert c.core.products['8940227892']['variants']['3892645120']['available'] is want
  assert (c.goal['alternative_permission']=='3892645120') is want
  if want:
   prepare=next(w for w in c.candidates() if w['work_id']=='prepare');args={'order_id':c.core.order_id,'item_ids':[c.changed_item],'new_item_ids':['3892645120'],'payment_method_id':c.core.payment};c.deterministic(c.instruction(prepare,{'arguments':args}),tools);assert str(c.plan['quote']['difference'])=='175.09'
   assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
 c=e.load('known_out')
 try:e.shared.decide # Program rejection is tested directly without model sampling.
 except Exception:pass
 submit=next(w for w in c.candidates() if w['work_id']=='submit')
 try:c.validate_instruction(c.instruction(submit));raise AssertionError('submit accepted')
 except e.shared.repairs12.Rejected as ex:assert ex.feedback['unmet_preconditions']
 return {'passed':True,'model_calls':0,'logging_cases':diagnostics,'tests':['timeout/network/service/parse distinguished and sanitized','status/request ID retained','unknown initial public states and candidate menus identical','real query reveals false vs true','only true activates original variant permission','original 10x quote 175.09 and independent authorization required','program rejection distinguished from request failure']}
