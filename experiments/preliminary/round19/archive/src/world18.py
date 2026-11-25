import json,time
from copy import deepcopy
from exchange_core import Ledger,packed
from baseline_runner import RetailTools,RetailDB

def dump(x):return x.model_dump(mode='json') if hasattr(x,'model_dump') else x
class World:
 def __init__(self,cfg,version):
  self.cfg=deepcopy(cfg);self.version=version;self.tools=RetailTools(RetailDB.model_validate(deepcopy(cfg['environment'])));self.history=[{'role':'user','content':cfg['initial_message']}];self.core=Ledger([]);self.desired=cfg['target'];self.permission_source=0;self.withdrawn=False;self.plan=None;self.event=None;self.writes=[];self.checks=[];self.steps=0;self.stopped=False;self.remaining_budget={'agent_calls':24,'agent_tokens':60000,'work_steps':9};self.event_export=None
  for name,args in [('find_user_id_by_email',{'email':cfg['environment']['users'][cfg['user_id']]['email']}),('get_user_details',{'user_id':cfg['user_id']}),('get_order_details',{'order_id':cfg['order_id']}),('get_product_details',{'product_id':cfg['product_id']})]:self.observation(name,args,dump(getattr(self.tools,name)(**args)))
  self.core.order_id=cfg['order_id'];self.core.payment=cfg['payment_method_id'];self.core.scope=[cfg['item_id']]
  self.core.put('scope',self.core.scope,sources=[0]);self.core.put('payment',self.core.payment,['profile:'+cfg['user_id']],[0]);self.set_requirement(self.desired,0)
 def observation(self,name,args,result):
  key='call'+str(len(self.history));self.history.append({'role':'assistant','tool_calls':[{'id':key,'type':'function','function':{'name':name,'arguments':packed(args)}}]});self.history.append({'role':'tool','tool_call_id':key,'content':packed(result)});self.core.observe(name,args,result,len(self.history)-1)
 def set_requirement(self,vid,source):
  self.desired=vid;self.permission_source=source;opts=deepcopy(self.core.products[self.cfg['product_id']]['variants'][vid]['options']);self.core.requirements[self.cfg['item_id']]=opts;self.core.put('requirement:'+self.cfg['item_id'],opts,sources=[source]);self.core.review([self.cfg['item_id']],source)
 def args(self,vid=None):return {'order_id':self.cfg['order_id'],'item_ids':[self.cfg['item_id']],'new_item_ids':[vid or self.desired],'payment_method_id':self.cfg['payment_method_id']}
 def authorize_current(self):
  try:return self.core.gate(self.args())['allowed'] and not self.withdrawn
  except ValueError:return False
 def check_args(self,args):
  if self.withdrawn:raise ValueError('User withdrew the exchange request; no exchange is authorized.')
  if args!=self.args():raise ValueError('Arguments differ from current explicitly permitted specification/scope/payment.')
  return self.core.compile(args)
 def visible_state(self):
  return {'current_facts':{'identity':self.core.authenticated,'order':self.core.orders[self.cfg['order_id']],'profile':self.core.users[self.cfg['user_id']],'catalog':self.core.products,'product_sources':self.core.product_refs},'current_user_intent':{'permitted_variant':None if self.withdrawn else self.desired,'source':self.permission_source,'quote':self.history[self.permission_source]['content'],'withdrawn':self.withdrawn,'effective_conditional_permission':not self.withdrawn and self.core.products[self.cfg['product_id']]['variants'][self.desired]['available'] is True,'other_variants':'not_yet_accepted'},'current_plan':self.plan,'current_authorized':self.authorize_current(),'records_with_provenance':{k:{field:deepcopy(v[field]) for field in ('status','version','depends_on','sources')} for k,v in self.core.records.items()},'historical_proposals_and_approvals':{'proposals':deepcopy(self.core.proposals),'approvals':deepcopy(self.core.old_confirmations)},'policy':'Historical compatibility is context only. Current-plan authorization and stock are required for write. Not yet accepted is not refused.'}
 def candidates(self):
  p=self.core.products[self.cfg['product_id']];stock=p['variants'][self.desired]['available'];auth=self.authorize_current();current=False
  try:current=bool(self.plan and self.plan['fingerprint']==self.check_args(self.args())['fingerprint'])
  except ValueError:pass
  return [{'action':'query','parameters':{'product_id':self.cfg['product_id']},'preconditions':{'product_exists':True},'ready':True,'effect':'obtain a fresh official observation; optional even when cached'}, {'action':'clarify','parameters':{'variant_id':'choose an existing alternative to ask about'},'preconditions':{'user_contact':True,'not_withdrawn':not self.withdrawn},'ready':not self.withdrawn,'effect':'obtain new specification permission; not transaction approval'}, {'action':'prepare','parameters':{'arguments':self.args()},'preconditions':{'not_withdrawn':not self.withdrawn,'permitted_variant_in_stock':stock},'ready':not self.withdrawn and stock is True,'effect':'compute exact current proposal'}, {'action':'confirm','parameters':{'arguments':self.args()},'preconditions':{'not_withdrawn':not self.withdrawn,'current_prepared_proposal':current},'ready':not self.withdrawn and current,'effect':'disclose current full proposal and obtain independent approval'}, {'action':'submit','parameters':{'arguments':self.args()},'preconditions':{'not_withdrawn':not self.withdrawn,'current_authorization':auth,'not_written':not self.writes},'ready':not self.withdrawn and auth and not self.writes,'effect':'write one exchange requested record'}, {'action':'stop','parameters':{},'preconditions':{},'ready':True,'effect':'end interaction; correct only when user stops or no permitted completion remains'}]
 def export(self):return {'cfg':self.cfg,'version':self.version,'database':self.tools.db.model_dump(mode='json'),'history':deepcopy(self.history),'ledger':deepcopy(self.core.__dict__),'desired':self.desired,'permission_source':self.permission_source,'withdrawn':self.withdrawn,'plan':deepcopy(self.plan),'event':deepcopy(self.event),'writes':deepcopy(self.writes),'checks':deepcopy(self.checks),'steps':self.steps,'stopped':self.stopped,'remaining_budget':deepcopy(self.remaining_budget)}
 @classmethod
 def restore(cls,x):
  w=cls.__new__(cls);w.cfg=deepcopy(x['cfg']);w.version=x['version'];w.tools=RetailTools(RetailDB.model_validate(deepcopy(x['database'])));w.core=Ledger([]);w.core.__dict__=deepcopy(x['ledger']);w.event_export=None
  for k in ('history','desired','permission_source','withdrawn','plan','event','writes','checks','steps','stopped','remaining_budget'):setattr(w,k,deepcopy(x[k]))
  return w
 def trigger(self):
  if self.version!='changed' or self.event:return
  before=self.visible_state();typ=self.cfg['change_type']
  if typ=='resource':
   self.tools.db.products[self.cfg['product_id']].variants[self.cfg['target']].available=False
   self.observation('get_product_details',{'product_id':self.cfg['product_id']},dump(self.tools.get_product_details(product_id=self.cfg['product_id'])))
  else:
   self.history.append({'role':'user','content':self.cfg['change_message']});ref=len(self.history)-1
   if typ=='withdrawal':self.withdrawn=True;self.permission_source=ref;self.core.put('user_request_active',False,sources=[ref]);self.core.records['authorization']['status']='stale'
   else:self.set_requirement(self.cfg['fallback'],ref)
  self.event={'type':typ,'trigger':'after actual first complete-plan user approval, before first submit','history_length':len(self.history),'before':before,'after':self.visible_state()};self.event_export=self.export()
 def execute(self,d):
  started=time.perf_counter();cpu=time.process_time();before=self.export();action=d['action'];p=d.get('parameters',{});ar=None;ur=None;result=None;allowed=False;error=None;actual_tool=None;gate=None
  try:
   if action=='query':
    if p.get('product_id')!=self.cfg['product_id']:raise ValueError('Product not in current exchange scope.')
    actual_tool='get_product_details';result=dump(self.tools.get_product_details(**p));self.observation(actual_tool,p,result)
   elif action=='clarify':
    if self.withdrawn:raise ValueError('User already requested stopping; do not reopen a withdrawn exchange.')
    offered=p.get('variant_id');prod=self.core.products[self.cfg['product_id']]
    if offered==self.desired:raise ValueError('Ask about a different alternative, not the specification already permitted.')
    if offered not in prod['variants']:raise ValueError('Clarification must name an existing specification; not a nonexistent item.')
    v=prod['variants'][offered];t=prod['variants'][self.desired];text=f"The currently requested item {self.desired} exists; observed stock is {packed(t['available'])}. Alternative {offered} exists with options {packed(v['options'])}, price {v['price']}, and observed stock {packed(v['available'])}. You have not accepted this alternative. Would you accept it? Specification permission is separate from final transaction approval."
    ar=len(self.history);self.history.append({'role':'assistant','content':text})
    # Controlled user reads the actual question, current stock and current intent;
    # no hidden version label decides acceptance.
    fallback=self.cfg['fallback']
    if self.core.products[self.cfg['product_id']]['variants'][self.desired]['available'] is False and fallback:
     reply=f"I accept item {fallback} with options {packed(prod['variants'][fallback]['options'])} only if it is in stock. Keep the original order, exchange item and payment. Please prepare the complete new proposal and ask for my final approval; this is not approval to submit."
     ur=len(self.history);self.history.append({'role':'user','content':reply});self.set_requirement(fallback,ur)
    else:
     reply='Keep my currently requested specification. I have not accepted any different specification; please use the current evidence and ask for final approval of the complete proposal.';ur=len(self.history);self.history.append({'role':'user','content':reply})
    result={'reply':reply,'permission_source':self.permission_source}
   elif action in ('prepare','confirm','submit'):
    args=p['arguments'];quote=self.check_args(args)
    if action=='prepare':
     quote=self.core.prepare(args,len(self.history));self.plan={'arguments':deepcopy(args),**quote};result=self.plan;self.observation('prepare_exchange_proposal',args,result)
    elif action=='confirm':
     if not self.plan or self.plan['fingerprint']!=quote['fingerprint']:raise ValueError('Prepare this current complete proposal before asking for approval.')
     text='Please independently approve this exact complete exchange proposal: '+packed({'arguments':args,'rows':quote['rows'],'difference':quote['difference'],'payment_method':self.core.users[self.cfg['user_id']]['payment_methods'][self.cfg['payment_method_id']]})+'. These are all exchange items. The later tool result will indicate whether the request was registered.'
     ar=len(self.history);self.history.append({'role':'assistant','content':text});reply='Yes. I explicitly approve exactly this complete proposal: '+packed({'arguments':args,'difference':quote['difference']})+'. These are all items; submit only this exact proposal with the stated payment.';ur=len(self.history);self.history.append({'role':'user','content':reply});result=self.core.confirm(args,quote['difference'],ur,ar);self.trigger()
    else:
     gate=self.core.gate(args);actual_tool='exchange_delivered_order_items';result=dump(self.tools.exchange_delivered_order_items(**args));self.observation(actual_tool,args,result);self.writes.append({'arguments':deepcopy(args),'gate':gate,'result':result,'user_source':self.permission_source,'history_ref':len(self.history)-1})
   elif action=='stop':self.stopped=True;result={'stopped':True,'database_written':bool(self.writes)};self.observation('stop_interaction',{},result)
   else:raise ValueError('Unknown action; use the public tool schema.')
   allowed=True;self.steps+=1;self.remaining_budget['work_steps']-=1
  except (ValueError,KeyError,TypeError) as ex:
   error=str(ex);self.observation('operation_rejected',{'action':action,'parameters':p},{'error':error,'executed':False})
  check={'action':action,'parameters':deepcopy(p),'allowed':allowed,'reason':error,'actual_tool':actual_tool,'current_request_active':not before['withdrawn'],'current_user_permission':before['desired'],'current_authorization':self.authorize_from_export(before),'visible_inventory_sources':before['ledger']['product_refs']};self.checks.append(check)
  if self.event and not before['event']:self.event_export=self.export()
  return {'decision':deepcopy(d),'before':before,'check':check,'result':deepcopy(result),'assistant_ref':ar,'user_ref':ur,'after':self.export(),'wall_seconds':time.perf_counter()-started,'local_cpu_seconds':time.process_time()-cpu}
 @staticmethod
 def authorize_from_export(x):return World.restore(x).authorize_current()
