"""Module 1: current effective state, constraint judgments and evidence sources."""
from copy import deepcopy
from decimal import Decimal
from world20 import World

class BusinessState(World):
 def initialize_constraints(self,cap=10000):
  self.cap=Decimal(str(cap));self.analysis_results=[];self.loop_events=[]
  self.cap_ref=len(self.history);self.history.append({'role':'user','content':f'Maximum signed combined new-minus-old difference: {self.cap:.2f}. Negative means a required minimum refund. Initial requested options are a preference; different options can be negotiated, but stock and this amount limit are hard. Specification permission is not transaction approval.'})
 def difference(self,variant=None):
  total=Decimal('0')
  for i in self.cfg['scope']:
   v=self.variant(i,variant if i==self.cfg['scope'][0]and variant else None)
   if not v:return None
   total+=Decimal(str(v['price']))-Decimal(str(self.item(i)['price']))
  return total
 def feasible(self,v=None):
  first=self.cfg['scope'][0];v=v or self.targets[first]
  if v==first or not self.variant(first,v)or self.variant(first,v)['available']is not True:return False
  d=self.difference(v)
  return d is not None and d<=self.cap and all(self.stock(i)is True for i in self.cfg['scope'][1:])
 def comparison(self):
  i=self.cfg['scope'][0];p=self.product(i)
  if not p:return {'status':'evidence_insufficient','missing':'formal catalogue/inventory observation','exact_feasible':[],'negotiable':[]}
  current=self.variant(i);exact=[];offers=[]
  for v in sorted(p['variants'].values(),key=lambda v:v['item_id']):
   if v['item_id']==i or not self.feasible(v['item_id']):continue
   row={'variant_id':v['item_id'],'options':v['options'],'price':v['price'],'whole_difference':str(self.difference(v['item_id'])),'source_ref':self.core.product_refs[self.item(i)['product_id']]}
   if v['options']==self.core.requirements[i]:exact.append(row)
   if v['item_id']!=self.targets[i]:offers.append(row)
  return {'status':'exact_feasible'if exact else'no_exact_match','exact_feasible':exact,'negotiable':offers,'empty_exact_set_is_valid':True,'meaning':'negotiable alternatives require NEW user specification permission; neither set grants transaction approval'}
 def candidates23(self):
  i=self.cfg['scope'][0];oid=self.cfg['order_id'];p=self.item(i)['product_id'];c=[{'work_type':'query','object':p,'preconditions':{'scope_product':True},'effect':'formal inventory evidence'},{'work_type':'analyze','object':i,'preconditions':{'catalogue_observed':bool(self.product(i))},'effect':'compare exact feasibility and negotiable options; empty exact result valid'},{'work_type':'prepare','object':oid,'preconditions':{'current_spec_feasible':self.feasible(),'pending_resolved':not self.pending},'effect':'store ONLY feasible current plan; not a diagnostic draft'},{'work_type':'confirm','object':oid,'preconditions':{'current_plan':self.current_plan(),'pending_resolved':not self.pending},'effect':'ask independent complete-plan approval'},{'work_type':'submit','object':oid,'preconditions':{'current_authorization':self.current_auth()},'effect':'native write'}]
  for v in self.comparison()['negotiable']:c.append({'work_type':'clarify','object':i,'parameters':{'variant_id':v['variant_id']},'preconditions':{'observed_available_within_cap':True,'specification_permission_needed':True},'effect':'ask permission for this specific alternative'})
  return sorted(c,key=lambda c:(c['work_type'],c['object'],str(c.get('parameters',{}))))
 def apply(self,result):
  old=dict(self.targets);super().apply(result)
  if old!=self.targets:
   for a in self.analysis_results:a['active']=False;a['invalidated_by']='effective specification update'
 def model_state(self,with_candidates=False):
  objects=[]
  for i in self.cfg['scope']:
   objects.append({'original_item_id':i,'product_id':self.item(i)['product_id'],'purchased':{'variant_id':i,'options':self.item(i)['options'],'price':self.item(i)['price'],'source_refs':self.core.records['order:'+self.cfg['order_id']]['sources']},'initial_request_history_only':{'variant_id':self.cfg['targets'][i],'source_ref':0,'active':self.targets[i]==self.cfg['targets'][i]},'CURRENT_EFFECTIVE_SPECIFICATION':{'variant_id':self.targets[i],'options':self.core.requirements[i],'source_ref':self.permission_sources[i],'literal_user_source':self.history[self.permission_sources[i]]['content'],'stock':self.stock(i),'price':(self.variant(i)or{}).get('price')}})
  comp=self.comparison();missing=[]
  if self.pending:missing.append('interpret actual pending user reply before business work')
  if comp['status']=='evidence_insufficient':missing.append('inventory/catalogue evidence')
  if not self.feasible():missing.append('current requested specification violates stock or signed amount cap; analyze negotiable alternatives or clarify; prepare cannot fix infeasibility')
  if not self.current_plan():missing.append('feasible complete current proposal')
  elif not self.current_auth():missing.append('independent current complete-plan authorization')
  return {'order_id':self.cfg['order_id'],'order_status':self.core.orders[self.cfg['order_id']]['status'],'objects':objects,'hard_constraint':{'max_signed_whole_difference':str(self.cap),'source_ref':self.cap_ref},'current_difference':str(self.difference()),'constraint_judgments':comp,'missing_prerequisites':missing,'pending_user_messages':self.pending_records(),'current_plan':self.plan if self.current_plan()else None,'current_plan_valid':self.current_plan(),'current_full_authorization':self.current_auth(),'payment_method_id':self.cfg['payment_method_id'],'analysis_feedback':[a for a in self.analysis_results if a.get('active',True)][-2:],'execution_feedback':[{'kind':f.get('kind','operation_result'),'work_type':f.get('selected_work',{}).get('work_type',f.get('work_type')),'allowed':f.get('allowed'),'reason':f.get('reason') if not f.get('allowed',False) else None,'historical_not_current_prerequisites':True}for f in self.feedback[-1:]],'authorization_evidence':{'valid_for_current_plan':self.current_auth(),'sources':self.core.records.get('authorization',{}).get('sources',[]),'quoted_user_replies':[{'source_ref':r,'text':self.history[r].get('content')}for r in self.core.records.get('authorization',{}).get('sources',[])if self.history[r]['role']=='user'],'current_bound_arguments':self.args() if self.current_auth()else None},'change':self.change and {k:v for k,v in self.change.items()if k!='public_text'},'evidence_index':self.core.product_refs,'budget':self.remaining_budget,**({'candidate_work':self.candidates23()}if with_candidates else{})}
 def export(self):
  x=super().export();x.update(hard_cap=str(getattr(self,'cap',10000)),analysis_results=deepcopy(getattr(self,'analysis_results',[])),feedback=deepcopy(self.feedback));return x
 def reply(self,kind,ar,detail):
  if kind!='clarify':return super().reply(kind,ar,detail)
  i=detail['object'];v=detail['offered_variant_id'];valid=i==self.cfg['scope'][0]and self.feasible(v)
  text=(f'Replace my CURRENT request for original item {i} with SKU {v}, if available and whole signed difference <= {self.cap:.2f}. This supersedes the previous requested SKU for this item. Other items stay as agreed. This is specification permission only; show the full new proposal for separate final approval.'if valid else'I do not approve that offer. Keep the hard stock and amount conditions; ask about a compliant alternative.')
  ref=len(self.history);self.history.append({'role':'user','content':text});self.pending.append(ref);self.asks[str(ref)]={'kind':'clarify','assistant_ref':ar,**deepcopy(detail)}
  if valid:self.oracle[i]=v
  self.env_records.append({'ask_kind':'clarify','assistant_ref':ar,'user_ref':ref,'reply':text,'approved':False});return ref
