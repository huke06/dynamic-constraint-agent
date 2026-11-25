import json,time
from copy import deepcopy
from world18 import World as OldWorld,dump
from exchange_core import packed
class World(OldWorld):
 def export(self):
  d=super().export();d['pending_raw_evidence']=deepcopy(getattr(self,'raw_evidence',[]));return d
 @classmethod
 def restore(cls,x):
  w=super().restore(x);w.raw_evidence=deepcopy(x.get('pending_raw_evidence',[]));return w
 def trigger(self):
  if self.version!='changed' or self.event:return
  before=self.visible_state();kind=self.cfg['change_type']
  if kind=='resource':
   self.tools.db.products[self.cfg['product_id']].variants[self.cfg['target']].available=False
   args={'product_id':self.cfg['product_id']};result=dump(self.tools.get_product_details(**args));text='Public inventory update from the simulated retail environment: '+packed({'tool':'get_product_details','arguments':args,'result':result});self.history.append({'role':'user','content':text});self.core.observe('get_product_details',args,result,len(self.history)-1)
  else:
   text=self.cfg['change_message'];self.history.append({'role':'user','content':text});ref=len(self.history)-1
   if kind=='requirement':self.set_requirement(self.cfg['fallback'],ref)
   else:
    self.withdrawn=True;self.permission_source=ref
    if 'authorization'in self.core.records:self.core.records['authorization']['status']='stale'
  self.user.invalidate();self.event={'type':kind,'trigger':'actual complete-plan approval before submission','source_ref':len(self.history)-1,'public_content':text,'before':before,'after':self.visible_state()};self.event_export=self.export()
 def execute(self,d):
  action=d.get('action');p=d.get('parameters',{})
  if action=='evidence':
   before=self.export();refs=p.get('refs',[]);records=[{'ref':int(r),'record':deepcopy(self.history[int(r)])} for r in refs if 0<=int(r)<len(self.history)];self.raw_evidence=records;self.steps+=1;self.remaining_budget['work_steps']-=1
   return {'decision':d,'before':before,'check':{'allowed':True,'action':'evidence','actual_tool':None},'result':records,'after':self.export()}
  if action not in ('clarify','confirm'):
   e=super().execute(d)
   if action=='query' and e['check']['allowed']:
    self.raw_evidence=[{'ref':self.core.product_refs[self.cfg['product_id']],'record':deepcopy(self.history[self.core.product_refs[self.cfg['product_id']]])}];e['after']=self.export()
   return e
  before=self.export();ar=ur=None;error=None;result=None;allowed=False;started=time.perf_counter()
  try:
   if self.withdrawn:raise ValueError('Current exchange request was withdrawn.')
   if action=='confirm':
    args=p['arguments'];q=self.check_args(args)
    if not self.plan or q['fingerprint']!=self.plan['fingerprint']:raise ValueError('Prepare the current complete proposal first.')
    text='Please independently approve this exact complete exchange proposal: '+packed({'arguments':args,'rows':q['rows'],'difference':q['difference'],'payment_method':self.core.users[self.cfg['user_id']]['payment_methods'][self.cfg['payment_method_id']]})+'. These are all exchange items. Approve this proposal before submission.'
   else:
    vid=p['variant_id'];prod=self.core.products[self.cfg['product_id']]
    if vid==self.desired or vid not in prod['variants']:raise ValueError('Clarification must name a different existing alternative specification.')
    text=f"The requested item {self.desired} exists and its latest observed available value is {packed(prod['variants'][self.desired]['available'])}. Alternative {vid} has options {packed(prod['variants'][vid]['options'])}, price {prod['variants'][vid]['price']}, and observed available {packed(prod['variants'][vid]['available'])}. You have not accepted it. Would you accept this alternative specification? This is not final transaction approval."
   ar=len(self.history);self.history.append({'role':'assistant','content':text});rec=self.user.respond(text,ar);ur=rec['user_ref'];result=rec
   if action=='confirm' and rec['approved_complete_plan']:self.core.confirm(args,q['difference'],ur,ar)
   if rec['trigger_due']:self.trigger()
   self.steps+=1;self.remaining_budget['work_steps']-=1;allowed=True
  except (ValueError,KeyError) as ex:error=str(ex);self.observation('operation_rejected',{'action':action,'parameters':p},{'error':error,'executed':False})
  check={'action':action,'parameters':deepcopy(p),'allowed':allowed,'reason':error,'actual_tool':None};self.checks.append(check)
  if self.event and not before['event']:self.event_export=self.export()
  return {'decision':deepcopy(d),'before':before,'check':check,'result':result,'assistant_ref':ar,'user_ref':ur,'after':self.export(),'wall_seconds':time.perf_counter()-started}
 def compact(self):
  cfg=self.cfg;prod=self.core.products[cfg['product_id']];v=prod['variants'][self.desired];ready=self.candidates();pending={c['action']:{k:val for k,val in c['preconditions'].items() if val is not True} for c in ready if not c['ready']};records=self.core.records;affected={k:{'status':x['status'],'sources':x['sources']} for k,x in records.items() if x['status']=='stale'}
  related=[]
  if v['available'] is not True:
   vs=[x for x in prod['variants'].values() if x['available'] is True and x['item_id']!=cfg['item_id'] and x['item_id']!=self.desired];vs.sort(key=lambda x:(sum(x['options'].get(k)!=val for k,val in v['options'].items()),x['item_id']));related=deepcopy(vs[:3])
  plan=None
  if self.plan:plan={'arguments':self.plan['arguments'],'difference':self.plan['difference'],'fingerprint':self.plan['fingerprint'],'valid_for_current_goal':self.plan['arguments']==self.args() and v['available'] is True}
  cands=[{'action':c['action'],'ready':c['ready'],'preconditions':c['preconditions']} for c in ready];cands.append({'action':'evidence','ready':True,'parameters':{'refs':'evidence index IDs'},'effect':'read selected original records once, not repeated entire history'})
  return {'current_goal':{'order_id':cfg['order_id'],'item_id':cfg['item_id'],'product_id':cfg['product_id'],'payment_method_id':cfg['payment_method_id'],'desired_variant':self.desired,'withdrawn':self.withdrawn,'permission_condition':{'recorded':not self.withdrawn,'requires':'observed stock true','observed_stock':v['available'],'effective':not self.withdrawn and v['available'] is True},'permission_source_ref':self.permission_source,'permission_quote':self.history[self.permission_source]['content']},'current_change':{'type':self.event['type'],'source_ref':self.event.get('source_ref',self.event.get('history_length',len(self.history))-1)} if self.event else None,'affected_judgments':affected,'missing_preconditions':pending,'current_proposal':plan,'current_authorization':self.authorize_current(),'business_result':{'written':bool(self.writes),'order_status':self.core.orders[self.cfg['order_id']]['status']},'related_variants':[deepcopy(v)]+related,'default_arguments':self.args(),'candidates':cands,'evidence_index':{'identity':self.core.records['identity']['sources'],'order':self.core.records['order:'+cfg['order_id']]['sources'],'payment':self.core.records['payment']['sources'],'catalog':self.core.product_refs[cfg['product_id']],'user':self.permission_source},'recent_work_feedback':[{'action':c.get('action'),'parameters':c.get('parameters'),'executed':c.get('allowed'),'reason':c.get('reason')} for c in self.checks[-3:]],'latest_formal_inventory':{'source_ref':self.core.product_refs[cfg['product_id']],'result_is_known':type(v['available'])is bool,'current_requested_stock':v['available'],'a_repeat_query_is_not_a_prerequisite':True},'last_feedback':deepcopy(self.history[-1]) if self.history[-1]['role']=='user' and not self.history[-1]['content'].startswith('Public inventory update') else None,'requested_raw_records':getattr(self,'raw_evidence',[]),'remaining_budget':self.remaining_budget}
