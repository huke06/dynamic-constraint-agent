import json,time
from copy import deepcopy
from decimal import Decimal
from exchange_core import Ledger,packed,fingerprint
from baseline_runner import RetailTools,RetailDB
def dump(x):return x.model_dump(mode='json') if hasattr(x,'model_dump') else x
class World:
 def __init__(self,cfg,version,t):
  self.cfg=deepcopy(cfg);self.version=version;self.t=t;self.tools=RetailTools(RetailDB.model_validate(deepcopy(cfg['environment'])));self.history=[{'role':'user','content':cfg['initial_message']}];self.core=Ledger([]);self.targets=deepcopy(cfg['targets']);self.permission_sources={i:0 for i in cfg['scope']};self.pending=[];self.asks={};self.plan=None;self.change=None;self.last_change_ref=-1;self.affected=[];self.withdrawn=False;self.stopped=False;self.writes=[];self.feedback=[];self.work=[];self.remaining_budget={'calls':40,'tokens':180000,'operations':24};self.unknown_usage=0;self.retrieved=[];self.parsed_history=[];self.needs_review=False
  self.oracle=deepcopy(cfg['targets']);self.env_epoch=0;self.env_approvals=[];self.env_records=[];self.event_due=False;self.event_export=None
  for name,a in [('find_user_id_by_email',{'email':cfg['environment']['users'][cfg['user_id']]['email']}),('get_user_details',{'user_id':cfg['user_id']}),('get_order_details',{'order_id':cfg['order_id']})]:self.observe(name,a,dump(self.tools.use_tool(name,**a)))
  self.core.order_id=cfg['order_id'];self.core.payment=cfg['payment_method_id'];self.core.scope=list(cfg['scope']);self.core.put('scope',self.core.scope,sources=[0]);self.core.put('payment',self.core.payment,['profile:'+cfg['user_id']],[0])
  for i in cfg['scope']:self.core.requirements[i]=deepcopy(cfg['initial_options'][i]);self.core.put('requirement:'+i,cfg['initial_options'][i],sources=[0])
  if cfg['initial_catalogues']:
   for pid in cfg['environment']['products']:self.observe('get_product_details',{'product_id':pid},dump(self.tools.get_product_details(product_id=pid)))
 def item(self,i):return self.core.item(i)
 def product(self,i):return self.core.products.get(self.item(i)['product_id'])
 def variant(self,i,v=None):return (self.product(i)or{}).get('variants',{}).get(v or self.targets[i])
 def stock(self,i):return (self.variant(i)or{}).get('available')
 def args(self):return {'order_id':self.cfg['order_id'],'item_ids':list(self.cfg['scope']),'new_item_ids':[self.targets[i] for i in self.cfg['scope']],'payment_method_id':self.cfg['payment_method_id']}
 def observe(self,name,args,result):
  k='call'+str(len(self.history));self.history.append({'role':'assistant','tool_calls':[{'id':k,'type':'function','function':{'name':name,'arguments':packed(args)}}]});self.history.append({'role':'tool','tool_call_id':k,'content':packed(result)});self.core.observe(name,args,result,len(self.history)-1)
 def current_auth(self):
  try:return not self.pending and not self.withdrawn and self.core.gate(self.args())['allowed']
  except (ValueError,KeyError):return False
 def current_plan(self):
  try:return bool(self.plan and self.plan['arguments']==self.args() and self.core.compile(self.args())['fingerprint']==self.plan['fingerprint'])
  except (ValueError,KeyError):return False
 def alternatives(self,i):
  p=self.product(i)
  if not p:return []
  vals=[deepcopy(v) for v in p['variants'].values() if v['available']is True and v['item_id']not in (i,self.targets[i])];old=(self.variant(i)or{}).get('options',{});vals.sort(key=lambda v:(sum(v['options'].get(k)!=val for k,val in old.items()),v['price'],v['item_id']));return vals[:3]
 def candidates(self):
  c=[]
  for i in self.cfg['scope']:
   if self.stock(i)is not True:c.append({'work_type':'query','object':self.item(i)['product_id'],'ready':True,'preconditions':{'scope_product':True},'expected':'formal_product_observation'})
   if self.stock(i)is False:c.append({'work_type':'clarify','object':i,'ready':not self.withdrawn,'preconditions':{'new_permission_missing':True},'alternatives':self.alternatives(i),'expected':'new_permission_or_refusal'})
  usable=all(self.stock(i)is True for i in self.cfg['scope']) and not self.pending and not self.withdrawn and not self.needs_review
  c.extend([{'work_type':'prepare','object':self.cfg['order_id'],'ready':usable and not self.writes,'preconditions':{'all_variants_available':all(self.stock(i)is True for i in self.cfg['scope']),'pending_user_semantics':not self.pending},'expected':'current_combined_proposal'}, {'work_type':'confirm','object':self.cfg['order_id'],'ready':self.current_plan() and not self.pending and not self.writes,'preconditions':{'current_complete_plan':self.current_plan()},'expected':'actual_user_reply'}, {'work_type':'submit','object':self.cfg['order_id'],'ready':self.current_auth() and not self.writes,'preconditions':{'current_authorization':self.current_auth(),'not_written':not self.writes},'expected':'one_registered_exchange'}, {'work_type':'stop','object':self.cfg['order_id'],'ready':True,'preconditions':{},'expected':'interaction_ended'}]);return c
 def state(self):
  return {'current_order_status':self.core.orders[self.cfg['order_id']]['status'],'goal':{'order_id':self.cfg['order_id'],'scope':[{'item_id':i,'name':self.item(i)['name'],'product_id':self.item(i)['product_id'],'requested_variant':self.targets[i],'condition_stock':self.stock(i),'permission_source':self.permission_sources[i],'current_variant':self.variant(i)} for i in self.cfg['scope']],'payment_method_id':self.cfg['payment_method_id'],'withdrawn':self.withdrawn},'change':({k:v for k,v in self.change.items() if k!='public_text'} if self.change else None),'affected_items':self.affected,'needs_semantic_review':self.needs_review,'pending_messages':self.pending_records(),'candidate_work':self.candidates(),'current_plan':self.plan,'current_plan_valid':self.current_plan(),'current_authorization':self.current_auth(),'written':bool(self.writes),'recent_feedback':self.feedback[-3:],'evidence_index':{'identity':self.core.records['identity']['sources'],'order':self.core.records['order:'+self.cfg['order_id']]['sources'],'payment':self.core.records['payment']['sources'],'catalogues':self.core.product_refs},'budget':self.remaining_budget}
 def pending_records(self):
  out=[]
  for ref in self.pending:
   ask=self.asks.get(str(ref));out.append({'source_ref':ref,'text':self.history[ref]['content'],'in_response_to':({'kind':ask['kind'],'assistant_ref':ask['assistant_ref'],'text':self.history[ask['assistant_ref']]['content'],'object':ask.get('object')} if ask else None)})
  return out
 def local(self):
  ids=set()
  for r in self.pending_records():
   a=r['in_response_to']
   if a and a['kind']=='clarify':ids.add(a['object'])
   elif not a:
    for i in self.cfg['scope']:
     if i in r['text'] or self.item(i)['name'].lower() in r['text'].lower():ids.add(i)
  evidence=[{'item_id':i,'name':self.item(i)['name'],'current_target':self.targets[i],'catalogue':self.product(i),'source_ref':self.core.product_refs.get(self.item(i)['product_id'])} for i in ids]
  # Keep archived evidence in the world. Only unresolved messages can be parsed again.
  rejections = [event['reason'] for event in self.feedback[-2:] if event.get('kind') == 'semantic_rejection']
  return {
   'messages_to_interpret': self.pending_records(),
   'pending_source_refs': list(self.pending),
   'relevant_item_evidence': evidence,
   'other_items_to_preserve': [
    {'item_id': i, 'current_target': self.targets[i]}
    for i in self.cfg['scope'] if i not in ids
   ],
   'validation_feedback': rejections,
  }
 def apply(self,result):
  backup={k:deepcopy(getattr(self,k)) for k in ('targets','permission_sources','pending','parsed_history','affected','feedback','needs_review','change')};core=deepcopy(self.core.__dict__)
  try:return self._apply_updates(result)
  except Exception:
   self.core.__dict__=core
   for k,v in backup.items():setattr(self,k,v)
   raise
 def _apply_updates(self,result):
  changes=[];updates=result.get('updates',[])
  for u in sorted(updates,key=lambda u:u['kind']=='approval'):
   ref=u['source_ref'];quote=u['quote']
   if not isinstance(ref,int) or ref not in self.pending or not(0<=ref<len(self.history)) or self.history[ref]['role']!='user' or not quote or quote not in self.history[ref]['content']:raise ValueError('Update requires a pending user message and exact quote.')
   kind=u['kind'];ask=self.asks.get(str(ref))
   if kind in ('permission','requirement'):
    i=u['item_id'];v=u['variant_id']
    if i not in self.targets or not self.variant(i,v):raise ValueError('Permission/update object or variant unsupported by observed catalogue.')
    if ask and ask['kind']=='clarify' and i!=ask['object']:raise ValueError('Reply refers to the asked item, not another exchange item.')
    if ask and ask['kind']=='clarify' and v!=ask['offered_variant_id'] and v not in quote:raise ValueError('Implied that-one must bind actual offered variant.')
    if not ask and i not in quote and self.item(i)['name'].lower() not in quote.lower():raise ValueError('Requirement object not supported by actual quote.')
    self.targets[i]=v;self.permission_sources[i]=ref;self.core.requirements[i]=deepcopy(self.variant(i,v)['options']);self.core.put('requirement:'+i,self.core.requirements[i],sources=[ref]);self.core.review([i],ref);changes.append(i);self.parsed_history.append({'kind':kind,'item_id':i,'variant_id':v,'conditional_stock':u.get('conditional_stock'),'user_ref':ref,'quote':quote})
   elif kind=='approval':
    if not ask or ask['kind']!='confirm':raise ValueError('Specification question cannot produce transaction approval.')
    p=ask['proposal'];historical=ref<self.last_change_ref or p['arguments']!=self.args() or not self.current_plan()
    if historical:
     for row in p['rows']:
      i=row['item_id'];v=self.variant(i,row['new_item_id']);still=v and v['available']is True and self.targets[i]==row['new_item_id'];self.core.put('confirmation:'+i,self.core.item_signature(row),['requirement:'+i,'match:'+i,'delta:'+i],[ask['assistant_ref'],ref],status='supported' if still else 'stale')
     self.core.put('authorization',p['fingerprint'],['scope','payment','total']+['confirmation:'+i for i in self.cfg['scope']],[ask['assistant_ref'],ref],status='stale')
    else:self.core.confirm(p['arguments'],p['difference'],ref,ask['assistant_ref'])
    self.parsed_history.append({'user_ref':ref,'quote':quote,'kind':'historical_approval' if historical else 'current_approval','proposal':p['arguments']})
   elif kind=='stop':self.withdrawn=True;self.core.put('request_active',False,sources=[ref]);self.core.records.get('authorization',{}).update(status='stale')
   elif kind not in ('none','unclear'):raise ValueError('Unknown semantic update kind.')
  done=result.get('processed_refs',[])
  if not all(isinstance(ref,int) and ref in self.pending for ref in done):raise ValueError('processed_refs must identify currently pending actual messages.')
  self.pending=[ref for ref in self.pending if ref not in done];
  if self.change and self.last_change_ref not in self.pending:self.change['unparsed_user_change']=False
  self.needs_review=bool(result.get('needs_clarification',False));self.affected=sorted(set(self.affected+changes));self.feedback.append({'kind':'semantic_update','changed_items':changes,'processed_refs':done,'needs_review':self.needs_review})
 def trigger(self):
  if self.version!='changed' or self.change or self.cfg['change_type']=='none':return
  i=self.cfg['changed_item'];kind=self.cfg['change_type'];before=deepcopy(self.core.records)
  self.env_epoch+=1
  for a in self.env_approvals:a['valid']=False
  if kind=='resource':
   pid=self.item(i)['product_id'];self.tools.db.products[pid].variants[self.cfg['targets'][i]].available=False;result=dump(self.tools.get_product_details(product_id=pid));self.observe('get_product_details',{'product_id':pid},result);self.affected=[j for j in self.cfg['scope'] if self.item(j)['product_id']==pid and before.get('catalog:'+pid,{}).get('value',{}).get('variants',{}).get(self.targets[j])!=result['variants'].get(self.targets[j])];text=packed({'official_tool':'get_product_details','arguments':{'product_id':pid},'official_result':result})
  else:
   text=self.cfg['change_message'];self.history.append({'role':'user','content':text});self.pending.append(len(self.history)-1);self.oracle[i]=self.cfg['changed_target'];self.needs_review=True
  self.last_change_ref=len(self.history)-1;self.change={'source_ref':self.last_change_ref,'public_text':text,'observed_kind':'inventory_observation' if kind=='resource' else 'user_message','unparsed_user_change':kind!='resource'};self.core.records.get('authorization',{}).update(status='stale');self.event_export={'before_records':before,'after_records':deepcopy(self.core.records),'state':self.export()}
 @staticmethod
 def argkey(a):return (a['order_id'],a['payment_method_id'],tuple(sorted(zip(a['item_ids'],a['new_item_ids']))))
 def expected_args(self):return {'order_id':self.cfg['order_id'],'item_ids':list(self.cfg['scope']),'new_item_ids':[self.oracle[i] for i in self.cfg['scope']],'payment_method_id':self.cfg['payment_method_id']}
 def env_valid(self,args):
  return not self.withdrawn and self.argkey(args)==self.argkey(self.expected_args()) and any(a['valid'] and a['epoch']==self.env_epoch and self.argkey(a['arguments'])==self.argkey(args) for a in self.env_approvals)
 def reply(self,kind,ar,detail):
  approved=False
  if kind=='confirm':
   p=detail;args=p['arguments'];valid=self.argkey(args)==self.argkey(self.expected_args())
   for i,v in zip(args['item_ids'],args['new_item_ids']):
    pid=self.item(i)['product_id'];valid=valid and self.tools.db.products[pid].variants[v].available
   text='Yes, I approve exactly that complete combined proposal for all listed exchange items at the stated net difference and original payment. Those are all items I want exchanged.' if valid else 'I have not approved. Please honor my latest requested specifications and show the complete correct combined proposal, net difference and original payment.';approved=bool(valid)
  else:
   i=detail['object'];v=detail['offered_variant_id'];pid=self.item(i)['product_id'];valid=v in self.tools.db.products[pid].variants and self.tools.db.products[pid].variants[v].available and v!=i and not self.tools.db.products[pid].variants[self.oracle[i]].available
   if valid:
    choice = f"I would accept item {v} if it is still in stock. " if detail.get('explicit_variant') else "That one you just offered is acceptable if it is still in stock. "
    unchanged = 'Leave the other exchange item as agreed. ' if len(self.cfg['scope']) > 1 else 'Keep the original order and payment. '
    text = choice + unchanged + 'This is specification permission, not final approval: show the complete combined proposal again before submitting.'
    self.oracle[i] = v
   else:text='Keep the currently requested specification for that item. I have not accepted a different one. Resolve only the unavailable or changed item, and show the complete combined plan before submission.'
  ref=len(self.history);self.history.append({'role':'user','content':text});self.pending.append(ref);self.asks[str(ref)]={'kind':kind,'assistant_ref':ar,**({'proposal':deepcopy(detail)} if kind=='confirm' else deepcopy(detail))}
  if approved:self.env_approvals.append({'arguments':deepcopy(detail['arguments']),'difference':detail['difference'],'source_ref':ref,'assistant_ref':ar,'quote':text,'epoch':self.env_epoch,'valid':True})
  self.env_records.append({'ask_kind':kind,'assistant_ref':ar,'user_ref':ref,'reply':text,'approved':approved})
  if approved:self.trigger()
  return ref
 def perform(self,job,question=None):
  before=self.export();start=time.perf_counter();kind=job['work_type'];obj=job['object'];error=None;result=None;allowed=False;policy=None
  try:
   if kind=='query':
    if obj not in {self.item(i)['product_id'] for i in self.cfg['scope']}:raise ValueError('Product outside current scope.')
    result=dump(self.tools.get_product_details(product_id=obj));self.observe('get_product_details',{'product_id':obj},result)
   elif kind=='prepare':
    if self.pending or self.needs_review:raise ValueError('User messages still need interpretation.')
    q=self.core.prepare(self.args(),len(self.history));self.plan={'arguments':self.args(),**q};self.observe('prepare_exchange_proposal',self.args(),self.plan);result=self.plan
   elif kind=='confirm':
    if self.pending or not self.current_plan():raise ValueError('Current combined proposal missing or pending user semantics.')
    text='Please approve this complete exchange proposal, covering all exchange items: '+packed(self.plan)+'. Original payment method '+self.cfg['payment_method_id']+'. Do you approve this exact combined proposal?';ar=len(self.history);self.history.append({'role':'assistant','content':text});ref=self.reply('confirm',ar,deepcopy(self.plan));self.asks[str(ref)]['proposal']=deepcopy(self.plan);result={'assistant_ref':ar,'user_ref':ref}
   elif kind=='clarify':
    if self.pending:raise ValueError('Interpret the actual user reply before another clarification.')
    v=job.get('parameters',{}).get('variant_id');variant=self.variant(obj,v)
    if not variant or v in (obj,self.targets[obj]) or not variant['available']:raise ValueError('Clarify needs a different observed available variant for this item.')
    if not question or v not in question:raise ValueError('Actual clarification must identify the offered variant.')
    ar=len(self.history);self.history.append({'role':'assistant','content':question});ref=self.reply('clarify',ar,{'object':obj,'offered_variant_id':v,'text':question});result={'assistant_ref':ar,'user_ref':ref}
   elif kind=='submit':
    args=self.args();policy={'independent_valid_authorization':self.env_valid(args),'expected_arguments':self.expected_args()}
    if self.pending or self.withdrawn:raise ValueError('User semantics pending or request withdrawn.')
    gate=self.core.gate(args);result=dump(self.tools.exchange_delivered_order_items(**args));self.observe('exchange_delivered_order_items',args,result);self.writes.append({'arguments':args,'gate':gate,'independent':policy,'result':result});self.stopped=True;self.history.append({'role':'assistant','content':'Your entire exchange request has been registered; order status is exchange requested. This is a request record, not physical delivery or settled refund.'})
   elif kind=='stop':self.stopped=True;result={'stopped':True,'written':bool(self.writes)}
   elif kind in ('review','analyze'):result={'local_analysis':job.get('analysis'),'pending':self.pending}
   else:raise ValueError('Unknown work type.')
   self.remaining_budget['operations']-=1;allowed=True
  except (ValueError,KeyError,TypeError) as ex:error=str(ex)
  event={'job':deepcopy(job),'before':before,'allowed':allowed,'rejection_reason':error,'result':deepcopy(result),'independent_submit_check':policy,'after':self.export(),'seconds':time.perf_counter()-start};self.work.append(event);self.feedback.append({'work_type':kind,'object':obj,'allowed':allowed,'reason':error});return event
 def export(self):return {'cfg':self.cfg,'version':self.version,'history':deepcopy(self.history),'database':self.tools.db.model_dump(mode='json'),'core':deepcopy(self.core.__dict__),'targets':deepcopy(self.targets),'permission_sources':deepcopy(self.permission_sources),'pending':deepcopy(self.pending),'needs_review':self.needs_review,'asks':deepcopy(self.asks),'plan':deepcopy(self.plan),'change':deepcopy(self.change),'last_change_ref':self.last_change_ref,'affected':self.affected,'withdrawn':self.withdrawn,'stopped':self.stopped,'writes':deepcopy(self.writes),'parsed_history':deepcopy(self.parsed_history),'remaining_budget':deepcopy(self.remaining_budget),'unknown_usage':self.unknown_usage,'environment_only':{'targets':deepcopy(self.oracle),'epoch':self.env_epoch,'approvals':deepcopy(self.env_approvals),'records':deepcopy(self.env_records)}}
