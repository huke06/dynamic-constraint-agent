"""Closeout adapters: immutable v2 exchange executor, native return business,
shared actual-speech responder and source-bound transaction authorization."""
import sys,os,json,time,re,hashlib,importlib.util
from pathlib import Path
from copy import deepcopy
from decimal import Decimal
from collections import Counter
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parents[1];R=E.parents[2]
spec=importlib.util.spec_from_file_location('closeout_a2',R/'experiments/preliminary/round24-official-and-trajectory/versions/a2/src/run24a2.py');a2=importlib.util.module_from_spec(spec);spec.loader.exec_module(a2)
from dynamic_constraint_agent_runtime import choose_dispatch,Dispatch
from construct20 import read,save,sha
from exchange_core import packed
from transport20 import Transport
from runner20 import semantic
from dynamic_constraint_agent_v2.decision import choose
from dynamic_constraint_agent_v2.execution import execute as exchange_execute
from world20 import dump
from tau2.agent.llm_agent import LLMAgent
from tau2.data_model.message import UserMessage,ToolMessage,MultiToolMessage

def money(x):return Decimal(str(x)).quantize(Decimal('.01'))
def key(a):
 pairs=tuple(sorted(zip(a.get('item_ids',[]),a.get('new_item_ids',[])))) if 'new_item_ids' in a else tuple(sorted(a.get('item_ids',[])))
 return (a.get('order_id'),a.get('payment_method_id'),pairs)
def hashed(x):return hashlib.sha256(packed(x).encode()).hexdigest()
def contains(text,quote):
 if not isinstance(quote,str) or not quote:return False
 clean=lambda s:re.sub(r'\s+',' ',re.sub(r'[*_`|]','',s)).strip()
 return quote in text or clean(quote) in clean(text)

EXTRACT='''Extract ONLY the CURRENT ACTUAL assistant question and proposal, not an ideal answer. Return JSON {"kind":"proposal|spec_permission|refund_permission|constraint_question|stop|other","asks":boolean,"question_quote":"exact actual question substring","proposal_quote":"exact full CURRENT proposal substring","item_ids":["current original IDs being returned/exchanged"],"pairs":[{"item_id":"original","new_item_id":"replacement","quote":"exact supporting substring"}],"payment_method_id":"actual ID or null","payment_quote":"exact actual substring","amount":number or null,"amount_quote":"exact actual substring","active_offers":[{"item_id":"original ID for exchange","variant_id":"replacement SKU for exchange","payment_method_id":"for refund-method permission","quote":"exact actual offer+question context","status":"active"}],"rejected_offer_ids":[],"topic":"cap_direction|amount_basis|refund_policy|scope|none","stop_quote":"exact actual termination substring"}. Proposals ask final transaction approval, and must describe the complete current scope, amount and method. Specification/refund-method permission alone is NOT transaction approval. Exchange amount is signed new-minus-old; refund is negative. Return amount is positive sum of purchased line prices. Literal JSON plans and natural-language tables are equally acceptable. Resolve all/that-one only from actual public context. Crucially active_offers contains ONLY options that are still actually being offered in the LAST question; exclude examples, withdrawn/rejected/not-allowed candidates earlier in the speech, even if their IDs are mentioned. If a final question names ONLY X, earlier discussed Y is NOT active. Generic one-of-these questions may use the actual preceding active list. A question about <= cap meaning, amount calculation or refund methods is constraint_question and must not be reinterpreted as an offer/approval. Do not invent quotes or missing facts.'''
RETURN_DECISION='''Choose ONE next business work from CURRENT observed state. Return JSON {"work_type":"query|analyze|clarify|prepare|confirm|submit|stop","object":"order_id except query uses order_id or user_id","parameters":{},"evidence_refs":[integer current history refs],"expected":"specific completion","reason":"grounded current evidence"}. Query parameters are {"tool":"get_order_details|get_user_details"}. Clarify parameters are {"payment_method_id":"observed legal method"}; permission for a refund route is not final transaction approval. Analyze can resolve a user's requested policy comparison and feedback, and is a valid successful result even if current requested method is invalid. Ask actual user permission for a different refund method. Prepare needs observed delivered order, observed profile, current explicit scope and legal method. Confirmation is for the complete current return scope, total and refund method. Only current complete approval permits submit. Stop on actual withdrawal; do not silently return a reduced or old scope. Multiple reasonable steps may exist. A program rejection is feedback, not a reason to repeat unchanged work. Once analysis feedback resolves a comparison, don't re-analyze it indefinitely.'''
RETURN_SEMANTIC='''Interpret ONLY actual pending user replies with exact quote/source_ref. Return JSON {"updates":[{"kind":"approval|scope|refund_permission|withdrawal|unclear","source_ref":integer,"quote":"exact user substring","item_ids":[],"payment_method_id":"if relevant"}],"processed_refs":[integer refs]}. Approval only for a complete-plan approval question; refund method permission is separate. A user's change after old approval makes old approval historical. Preserve unchanged scope/method. Never turn I have not approved or a policy clarification into approval.'''

class Exchange(a2.SharedWorld):
 def observe(self,tool,args,result):
  super().observe(tool,args,result)
  if tool=='get_product_details':
   for record in getattr(self,'analysis_results',[]):record['active']=False;record['invalidated_by']='new formal product observation'
 def comparison(self):
  z=super().comparison()
  if hasattr(self,'cap'):
   current=self.variant(self.cfg['scope'][0]);d=self.difference()
   z.update(current_requested_sku=self.targets[self.cfg['scope'][0]],current_sku_exists=current is not None,current_stock=(current or{}).get('available'),current_whole_difference=str(d),maximum_signed_whole_difference=str(self.cap),conflict_cause='missing_evidence' if current is None else 'stock' if current.get('available') is not True else 'signed_amount_cap' if d is not None and d>self.cap else 'none',comparison_baseline='sum(new replacement price minus ORIGINAL purchased price) across ALL exchange items; not relative to old requested replacements')
  return z
 def reply(self,kind,ar,detail):
  rec=respond(self,self.history[ar]['content'],ar)
  if kind=='confirm':self.asks[str(rec['user_ref'])]={'kind':'confirm','assistant_ref':ar,'proposal':deepcopy(detail)}
  self.sim_records.append(rec);return rec['user_ref']

class ReturnState:
 def __init__(self,cfg,t,group):
  self.cfg=deepcopy(cfg);self.t=t;self.group=group;self.business='return';self.tools=a2.b.RetailTools(a2.b.RetailDB.model_validate(deepcopy(cfg['environment'])));self.history=[{'role':'user','content':cfg['initial_message']}];self.observed={};self.refs={};self.scope=list(cfg['scope']);self.payment=cfg['payment_method_id'];self.sources={'scope':0,'payment':0};self.pending=[];self.asks={};self.plan=None;self.authorization=None;self.analysis_results=[];self.feedback=[];self.writes=[];self.stopped=False;self.withdrawn=False;self.change=None;self.event_export=None;self.env_epoch=0;self.env_approvals=[];self.env_records=[];self.sim_records=[];self.oracle_scope=list(cfg['scope']);self.oracle_payment=cfg['payment_method_id'];self.remaining_budget={'calls':40,'tokens':180000,'operations':24};self.unknown_usage=0;self.parsed_history=[];self.version='changed' if cfg.get('event',{}).get('kind')!='none' else 'stable'
  self.observe('find_user_id_by_email',{'email':cfg['environment']['users'][cfg['user_id']]['email']},dump(self.tools.find_user_id_by_email(email=cfg['environment']['users'][cfg['user_id']]['email'])))
  if not cfg.get('initial_missing'):
   for tool,args in [('get_user_details',{'user_id':cfg['user_id']}),('get_order_details',{'order_id':cfg['order_id']})]:self.observe(tool,args,dump(self.tools.use_tool(tool,**args)))
 def observe(self,tool,args,result):
  ident='env'+str(len(self.history));self.history.append({'role':'assistant','tool_calls':[{'id':ident,'type':'function','function':{'name':tool,'arguments':packed(args)}}]});self.history.append({'role':'tool','tool_call_id':ident,'content':packed(result)});self.observed[tool]=deepcopy(result);self.refs[tool]=len(self.history)-1
 def args(self):return {'order_id':self.cfg['order_id'],'item_ids':list(self.scope),'payment_method_id':self.payment}
 def expected_args(self):return {'order_id':self.cfg['order_id'],'item_ids':list(self.oracle_scope),'payment_method_id':self.oracle_payment}
 def legal_methods(self):
  o=self.observed.get('get_order_details');p=self.observed.get('get_user_details')
  if not o or not p:return []
  original=o['payment_history'][0]['payment_method_id'];return [k for k,v in p['payment_methods'].items() if k==original or v['source']=='gift_card']
 def amount(self,scope=None):
  o=self.observed.get('get_order_details')
  if not o:return None
  items={i['item_id']:i for i in o['items']};scope=self.scope if scope is None else scope
  if any(i not in items for i in scope):return None
  return sum((money(items[i]['price']) for i in scope),Decimal('0')).quantize(Decimal('.01'))
 def feasible(self):
  o=self.observed.get('get_order_details');return bool(o and o['status']=='delivered' and self.scope and len(set(self.scope))==len(self.scope) and self.amount() is not None and self.payment in self.legal_methods() and not self.withdrawn)
 def current_plan(self):return bool(self.plan and self.plan['arguments']==self.args() and self.plan['epoch']==self.env_epoch and self.feasible())
 def current_auth(self):return bool(not self.pending and self.current_plan() and self.authorization and self.authorization['epoch']==self.env_epoch and key(self.authorization['arguments'])==key(self.args()) and not self.withdrawn)
 def env_valid(self,args):return not getattr(self,'oracle_withdrawn',False) and key(args)==key(self.expected_args()) and any(a['valid'] and a['epoch']==self.env_epoch and key(a['arguments'])==key(args) for a in self.env_approvals)
 def model_state(self,candidates=True):
  missing=[]
  for k in ('get_order_details','get_user_details'):
   if k not in self.observed:missing.append(k+' observation missing')
  if not self.feasible():missing.append('current return scope/method/order is not yet feasible')
  if not self.current_plan():missing.append('current complete proposal missing')
  elif not self.current_auth():missing.append('independent current whole-return approval missing')
  if self.withdrawn:missing.append('user withdrew request: stop without writing')
  options=[]
  for k,obj in [('get_order_details',self.cfg['order_id']),('get_user_details',self.cfg['user_id'])]:options.append({'work_type':'query','object':obj,'parameters':{'tool':k},'necessary_precondition':'known public object ID','missing':k not in self.observed})
  for k in ('analyze','prepare','confirm','submit','stop'):options.append({'work_type':k,'object':self.cfg['order_id'],'preconditions':{'analysis_has_order_and_profile':bool(self.legal_methods()),'prepare_feasible':self.feasible(),'confirm_current_plan':self.current_plan(),'submit_current_authorization':self.current_auth(),'stop_on_withdrawal':self.withdrawn}})
  options +=[{'work_type':'clarify','object':self.cfg['order_id'],'parameters':{'payment_method_id':m},'preconditions':{'observed_legal':True,'needs_new_method_permission':m!=self.payment}} for m in self.legal_methods() if m!=self.payment]
  return {'business':'return','order_id':self.cfg['order_id'],'user_id':self.cfg['user_id'],'current_scope':self.scope,'current_refund_method':self.payment,'requirement_sources':{k:{'ref':v,'quote':self.history[v]['content']} for k,v in self.sources.items()},'observed_order':self.observed.get('get_order_details'),'observed_profile':self.observed.get('get_user_details'),'legal_refund_methods':self.legal_methods(),'refund_total':str(self.amount()),'withdrawn':self.withdrawn,'missing_prerequisites':missing,'pending_user_messages':[{'source_ref':r,'text':self.history[r]['content'],'in_response_to':self.asks.get(str(r))} for r in self.pending],'current_plan':self.plan if self.current_plan() else None,'current_full_authorization':self.current_auth(),'authorization_evidence':self.authorization if self.current_auth() else None,'analysis_feedback':[a for a in self.analysis_results if a.get('active',True)][-1:],'execution_feedback':self.feedback[-1:],'evidence_index':self.refs,'budget':self.remaining_budget,**({'candidate_work':options} if candidates else{})}
 def export(self):return {'business':'return','terminal_reason':getattr(self,'terminal_reason',None),'cfg':deepcopy(self.cfg),'history':deepcopy(self.history),'database':self.tools.db.model_dump(mode='json'),'observed':deepcopy(self.observed),'refs':deepcopy(self.refs),'scope':list(self.scope),'payment':self.payment,'pending':list(self.pending),'asks':deepcopy(self.asks),'plan':deepcopy(self.plan),'authorization':deepcopy(self.authorization),'analysis_results':deepcopy(self.analysis_results),'feedback':deepcopy(self.feedback),'parsed_history':deepcopy(self.parsed_history),'withdrawn':self.withdrawn,'stopped':self.stopped,'writes':deepcopy(self.writes),'change':deepcopy(self.change),'remaining_budget':dict(self.remaining_budget),'environment_only':{'scope':list(self.oracle_scope),'payment':self.oracle_payment,'withdrawn':getattr(self,'oracle_withdrawn',False),'epoch':self.env_epoch,'approvals':deepcopy(self.env_approvals),'records':deepcopy(self.env_records)}}
 def trigger(self):
  ev=self.cfg.get('event',{})
  if self.change or ev.get('kind','none')=='none':return
  before=self.export();self.env_epoch+=1
  for a in self.env_approvals:a['valid']=False
  if ev['kind']=='scope':self.oracle_scope=list(ev['item_ids']);text='Before submission, change my return scope to EXACTLY '+packed(self.oracle_scope)+'. Keep the refund method unchanged. Old approval does not authorize this changed complete return; ask for new approval.'
  elif ev['kind']=='payment':self.oracle_payment=ev['payment_method_id'];text='Before submission, change the refund method to '+self.oracle_payment+'. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval.'
  else:self.oracle_withdrawn=True;text='Before submission, I withdraw the ENTIRE return request. Do not register any return; keep the order unchanged. Stop this business now.'
  ref=len(self.history);self.history.append({'role':'user','content':text})
  if self.group=='framework':self.pending.append(ref)
  self.authorization=None;self.change={'kind':ev['kind'],'source_ref':ref,'text':text};self.event_export={'before':before,'after':self.export(),'public_messages':[deepcopy(self.history[ref])]}
 def interpret(self,t,trace):
  before=self.export();backup={k:deepcopy(getattr(self,k)) for k in ('scope','payment','sources','authorization','withdrawn','pending','parsed_history','analysis_results')};result=t.json([{'role':'system','content':RETURN_SEMANTIC},{'role':'user','content':packed({'pending':self.model_state()['pending_user_messages'],'observed_order':self.observed.get('get_order_details'),'legal_methods':self.legal_methods(),'validation_feedback':self.feedback[-1:]})}],'semantic','return_actual_user_reply')
  try:
   for u in result.get('updates',[]):
    ref=u['source_ref'];q=u['quote'];assert ref in self.pending and q and q in self.history[ref]['content'],'exact pending quote required';ask=self.asks.get(str(ref));kind=u['kind']
    if kind=='approval':
     if ask and ask['kind']=='confirm' and ask.get('approved') and ask['epoch']==self.env_epoch and key(ask['arguments'])==key(self.args()) and self.current_plan():self.authorization={'arguments':deepcopy(self.args()),'epoch':self.env_epoch,'source_ref':ref,'quote':q}
    elif kind=='scope':
     ids=u['item_ids'];assert all(i in q for i in ids) and self.amount(ids) is not None,'scope unsupported';self.scope=list(ids);self.sources['scope']=ref;self.authorization=None
    elif kind=='refund_permission':
     method=u['payment_method_id'];assert method in q and method in self.legal_methods(),'legal concrete method quote required';self.payment=method;self.sources['payment']=ref;self.authorization=None
    elif kind=='withdrawal':self.withdrawn=True;self.authorization=None
    if kind in ('scope','refund_permission','withdrawal'):
     for a in self.analysis_results:a['active']=False;a['invalidated_by_user_ref']=ref
    self.parsed_history.append({'source_ref':ref,'kind':kind,'quote':q})
   refs=result.get('processed_refs',[]);assert all(r in self.pending for r in refs);self.pending=[r for r in self.pending if r not in refs]
  except (AssertionError,KeyError,ValueError) as ex:
   for k,v in backup.items():setattr(self,k,v)
   self.feedback.append({'kind':'semantic_rejection','reason':str(ex),'output':result})
  trace.append({'module':'semantic_update','model_output':result,'before':before,'after':self.export()})

def snapshot(cfg,t,group):
 if cfg['business']=='return':return ReturnState(cfg,t,group)
 w=Exchange(cfg,'changed' if cfg.get('change_type')!='none' else 'stable',t);w.group=group;w.business='exchange';w.sim_records=[];w.policy=a2.POLICY;w.initialize_constraints(money(cfg.get('cap',10000)));return w

def actual_method(w):return w.payment if w.business=='return' else w.cfg['payment_method_id']
def visible_order(w):return w.observed.get('get_order_details') if w.business=='return' else w.core.orders.get(w.cfg['order_id'])
def event_epoch(w):return w.env_epoch

def add_reply(w,ar,text,kind,detail=None,approved=False):
 ref=len(w.history);w.history.append({'role':'user','content':text});detail=detail or{}
 if w.group=='framework':w.pending.append(ref)
 if kind in ('confirm','clarify'):
  if w.business=='return':w.asks[str(ref)]={'kind':kind,'assistant_ref':ar,'epoch':w.env_epoch,'approved':approved,**deepcopy(detail)}
  else:w.asks[str(ref)]={'kind':kind,'assistant_ref':ar,**deepcopy(detail)}
 if approved:w.env_approvals.append({'arguments':deepcopy(detail['arguments']),'epoch':w.env_epoch,'valid':True,'source_ref':ref,'assistant_ref':ar,'quote':text})
 w.env_records.append({'kind':kind,'assistant_ref':ar,'user_ref':ref,'reply':text,'approved':approved})
 if approved:w.trigger()
 return {'kind':kind,'reply':text,'user_ref':ref,'approved':approved}

def adjudicate(w,text,ar,p):
 kind=p.get('kind');quote=p.get('question_quote') or'';asks=p.get('asks') and contains(text,quote);scope=w.oracle_scope if w.business=='return' else w.cfg['scope'];method=w.oracle_payment if w.business=='return' else w.cfg['payment_method_id'];order=visible_order(w);checks={}
 if kind=='constraint_question' and asks:
  if w.business=='exchange':answer=f'The signed limit is new minus ORIGINAL purchased prices summed over ALL exchange items, and must be <= {w.cap:.2f}. Negative cap means a MINIMUM refund, not a maximum refund. Current requested whole difference is {w.difference()}. You may compare observed compliant substitutes, but need my concrete specification permission and later independent complete-plan approval.'
  else:answer='Refund only to original payment '+w.cfg['original_payment']+' or an existing gift card. My preferred permitted method is '+w.cfg.get('preferred_payment',w.cfg['original_payment'])+'. Current requested scope is '+packed(w.oracle_scope)+'. The refund total is the sum of original purchased line prices, not replacement prices. Please obtain independent complete approval; this clarification is not approval.'
  return {**add_reply(w,ar,answer,'information'),'extraction':p}
 if kind=='proposal' and asks:
  if w.business=='exchange':
   mapping={}
   for x in p.get('pairs',[]):
    i=x.get('item_id');v=x.get('new_item_id');belongs=[j for j in scope if w.variant(j,v)] if v else[]
    if len(belongs)==1:i=belongs[0]
    if i in scope and v and v in text and (i in text or w.item(i)['name'].lower() in text.lower()):mapping[i]=v
   args={'order_id':w.cfg['order_id'],'item_ids':list(scope),'new_item_ids':[mapping.get(i) for i in scope],'payment_method_id':p.get('payment_method_id')};amount=sum((money(w.variant(i,v)['price'])-money(w.item(i)['price']) for i,v in mapping.items() if w.variant(i,v)),Decimal('0'))
   checks={'complete_scope':set(mapping)==set(scope),'permitted':set(mapping)==set(scope) and all(mapping[i]==w.oracle[i] for i in scope),'stock':set(mapping)==set(scope) and all(w.variant(i,mapping[i]) and w.variant(i,mapping[i])['available'] is True and mapping[i]!=i for i in scope),'cap':amount<=w.cap}
  else:
   ids=p.get('item_ids',[]);args={'order_id':w.cfg['order_id'],'item_ids':ids,'payment_method_id':p.get('payment_method_id')};amount=w.amount(ids);checks={'complete_scope':Counter(ids)==Counter(scope),'legal_method':args['payment_method_id'] in w.legal_methods(),'permitted':args['payment_method_id']==method,'observed_delivered':bool(order and order['status']=='delivered')}
  pq=p.get('payment_quote')or''
  if args['payment_method_id'] is None and contains(text,pq) and 'original' in pq.lower():args['payment_method_id']=w.cfg.get('original_payment',w.cfg['payment_method_id'])
  if w.business=='return':checks['legal_method']=args['payment_method_id'] in w.legal_methods();checks['permitted']=args['payment_method_id']==method
  checks['payment']=args['payment_method_id']==method and contains(text,pq)
  aq=p.get('amount_quote')or'';spoken=p.get('amount');magnitude_ok=amount is not None and isinstance(spoken,(int,float)) and (abs(money(spoken))==amount if w.business=='return' else money(spoken)==amount)
  checks['amount']=bool(magnitude_ok and contains(text,aq) and any(abs(money(v))==abs(amount) for v in re.findall(r'-?\d+\.\d+',aq.replace(',',''))))
  if all(checks.values()) and not w.withdrawn and not getattr(w,'oracle_withdrawn',False):
   detail={'arguments':args,'difference':float(amount)};rec=add_reply(w,ar,'Yes, I approve exactly that complete current '+w.business+' proposal, all listed items, stated exact amount and refund/payment method. Those are all the items I want processed.','confirm',detail,True);return {**rec,'extraction':p,'checks':checks}
  why=', '.join(k for k,v in checks.items() if not v)
  correction='I have NOT approved. Please correct '+why+'. '
  if w.business=='exchange':correction+=f'The maximum signed whole difference means <= {w.cap:.2f}; negative means minimum refund. Your proposed total is {amount}. Ask about an active compliant substitute, then show the complete current proposal for separate approval.'
  else:correction+='Return only my latest scope '+packed(scope)+' and refund to '+method+'. Explain any policy conflict before asking about a different permitted route; ask fresh complete approval.'
  return {**add_reply(w,ar,correction,'correction'),'extraction':p,'checks':checks}
 if kind in ('spec_permission','refund_permission') and asks:
  offers=p.get('active_offers',[]);rejected=set(p.get('rejected_offer_ids',[]));question_ids=set(re.findall(r'\b\d{10}\b',quote))
  for x in offers:
   oq=x.get('quote')or'';v=x.get('variant_id') if w.business=='exchange' else x.get('payment_method_id')
   if x.get('status')!='active' or not contains(text,oq) or not v or v not in text or v in rejected:continue
   if w.business=='exchange':
    belongs=[i for i in scope if w.variant(i,v)];i=belongs[0] if len(belongs)==1 else x.get('item_id')
    if question_ids and v not in question_ids:continue
    line=next((line for line in text.splitlines() if v in line),'').lower()
    if any(s in line for s in ('not allowed','does not work','rejected','not be allowed','does not meet')) and v not in question_ids:continue
    if i!=scope[0] or not w.feasible(v):continue
    w.oracle[i]=v
    if w.group=='official':w.targets[i]=v;w.core.requirements[i]=deepcopy(w.variant(i,v)['options'])
    detail={'object':i,'offered_variant_id':v};rec=add_reply(w,ar,f'Replace my CURRENT request for original item {i} with SKU {v}, if in stock and whole signed difference <= {w.cap:.2f}. This supersedes my previous specification for this item. Other items stay as agreed. This is specification permission only; show the full new proposal for separate approval.','clarify',detail)
   else:
    if v not in w.legal_methods():continue
    w.oracle_payment=v
    if w.group=='official':w.payment=v
    rec=add_reply(w,ar,'Use '+v+' as my permitted refund method. Keep exactly the latest return scope. This is method permission only; show the complete current return, amount and method for separate approval.','clarify',{'payment_method_id':v})
   return {**rec,'extraction':p,'accepted_offer':v}
  answer='I have not accepted another specification or refund method. Please offer a CURRENT active compliant option; do not use an example or an option you have just rejected.'
  if w.business=='exchange':answer+=f' My signed condition is total <= {w.cap:.2f}.'
  return {**add_reply(w,ar,answer,'correction'),'extraction':p}
 stopq=p.get('stop_quote')or''
 if kind=='stop' and contains(text,stopq) and re.search(r'stop|cancel|closed|(?:keep|remain|leave).*unchanged|not (?:process|submit|register|proceed)|won.t (?:process|submit|register|proceed)',stopq,re.I) and not re.search(r'until|unless|before.*approv|not.*yet',stopq,re.I):
  w.stopped=True;w.terminal_reason='withdrawal_acknowledged' if getattr(w,'oracle_withdrawn',False) else 'voluntary_stop';return {**add_reply(w,ar,'Understood. Keep the database unchanged.','stop'),'extraction':p}
 if w.withdrawn or getattr(w,'oracle_withdrawn',False):
  return {**add_reply(w,ar,'The request is withdrawn. Stop without any write.','information'),'extraction':p}
 return {**add_reply(w,ar,'Please resolve my latest request from observed facts. If a policy or amount condition is unclear, ask that question; otherwise ask for specific permission or complete current-plan approval.','information'),'extraction':p}

def respond(w,text,ar):
 order=visible_order(w);identities=[{'item_id':i['item_id'],'name':i['name'],'product_id':i['product_id']} for i in (order or{}).get('items',[])]
 p=w.t.json([{'role':'system','content':EXTRACT},{'role':'user','content':packed({'business':w.business,'actual_assistant':text,'public_order_id':w.cfg['order_id'],'public_item_identities':identities,'recent_actual_user_messages':[m['content'] for m in w.history if m['role']=='user'][-2:]})}],'simulator','actual_current_question_not_rejected_discussion',max_tokens=2100)
 return adjudicate(w,text,ar,p)

def return_choose(w,t):return t.json([{'role':'system','content':RETURN_DECISION+'\n'+a2.POLICY},{'role':'user','content':packed(w.model_state())}],'cognitive','return_next_work')
def return_dispatch(w,program_retry_allowed=True):
 if w.pending:return Dispatch('state_semantics','actual new user reply')
 if not program_retry_allowed:return Dispatch('decision_model','prior program work was rejected; model must read specific feedback')
 if w.withdrawn:return Dispatch('decision_model','withdrawal must be acknowledged and stopped')
 missing=[k for k in ('get_order_details','get_user_details') if k not in w.observed]
 if len(missing)==1:
  k=missing[0];return Dispatch('program','unique missing observation',{'work_type':'query','object':w.cfg['order_id'] if k=='get_order_details' else w.cfg['user_id'],'parameters':{'tool':k},'evidence_refs':[],'expected':'record formal native observation','reason':'known sole missing evidence'})
 if missing or not w.feasible():return Dispatch('decision_model','missing evidence or refund-policy conflict')
 if not w.current_plan():k='prepare'
 elif w.current_auth():k='submit'
 elif not any(a.get('kind')=='confirm' and a.get('arguments')==w.args() and a.get('epoch')==w.env_epoch for a in w.asks.values()):k='confirm'
 else:return Dispatch('decision_model','confirmation needs follow-up')
 return Dispatch('program','determinate current-plan contract',{'work_type':k,'object':w.cfg['order_id'],'parameters':{},'evidence_refs':[],'expected':'complete current contract','reason':'necessary current prerequisites program-verified'})

def return_execute(w,d,t,trace):
 before=w.export();allowed=False;reason=None;result=None;original=deepcopy(d)
 try:
  assert not w.pending,'Pending user message needs semantics';k=d['work_type'];p=d.get('parameters',{});obj=d['object'];assert d.get('reason') and d.get('expected'),'reason/expected required';assert all(isinstance(i,int) and 0<=i<len(w.history) for i in d.get('evidence_refs',[])),'invalid evidence source'
  if k=='query':
   tool=p['tool'];assert tool in ('get_order_details','get_user_details');args={'order_id':w.cfg['order_id']} if tool=='get_order_details' else {'user_id':w.cfg['user_id']};assert obj==next(iter(args.values()));result=dump(w.tools.use_tool(tool,**args));w.observe(tool,args,result)
  else:
   assert obj==w.cfg['order_id'],'whole-return object is exact order'
   if k=='analyze':
    assert w.legal_methods(),'need order/profile evidence for route comparison';facts={'current_method':w.payment,'current_method_legal':w.payment in w.legal_methods(),'legal_methods':w.legal_methods(),'original_method':w.cfg['original_payment'],'refund_total':str(w.amount()),'current_scope':w.scope,'public_user_request':w.history[w.sources['payment']]['content'],'no_approval_granted':True};result=t.json([{'role':'system','content':'Compare ONLY these program-verified return facts against the actual user request and preference. Return JSON {"analysis":"grounded local route comparison","recommended_method":"one observed legal ID","not_authorization":true}. Do not invent faster timing, fees, permission or a refund settlement. Empty current-feasible set is a valid conflict finding.'},{'role':'user','content':packed(facts)}],'semantic','return_policy_route_analysis');w.analysis_results.append({'facts':facts,'advice':result})
   elif k=='clarify':
    method=p['payment_method_id'];assert method in w.legal_methods() and method!=w.payment,'different observed legal route required';text='The current requested refund method '+w.payment+' is not the route being proposed. Official policy permits original payment '+w.cfg['original_payment']+' or an existing gift card. For the current return scope '+packed(w.scope)+', refund total '+str(w.amount())+', do you accept refund method '+method+'? This is method permission only; complete return approval will be requested separately.';ar=len(w.history);w.history.append({'role':'assistant','content':text});result=respond(w,text,ar);w.sim_records.append(result)
   elif k=='prepare':
    assert w.feasible(),'scope/method/order evidence infeasible';assert not p,'parameters must come from current state';w.plan={'arguments':w.args(),'refund_amount':str(w.amount()),'epoch':w.env_epoch,'fingerprint':hashed([w.args(),str(w.amount()),w.env_epoch])};result=deepcopy(w.plan)
   elif k=='confirm':
    assert w.current_plan() and not p,'current whole-return plan required';ar=len(w.history);text='Please independently approve this COMPLETE CURRENT return proposal: '+packed(w.plan)+'. Order will become return requested and an email will explain how to return; refund is not reported as settled. Do you approve the exact complete scope, amount and refund method?';w.history.append({'role':'assistant','content':text});result=respond(w,text,ar);w.sim_records.append(result)
   elif k=='submit':
    assert w.current_auth() and not p,'current complete authorization required';args=w.args();check=w.env_valid(args);result=dump(w.tools.return_delivered_order_items(**args));w.observe('return_delivered_order_items',args,result);w.writes.append({'arguments':args,'result':result,'independent_valid_authorization':check});w.stopped=True
   elif k=='stop':assert w.withdrawn,'solvable active request must not be abandoned';w.stopped=True;w.terminal_reason='withdrawal_acknowledged';result={'correct_stop':True,'written':False}
   else:raise ValueError('unknown return work')
  allowed=True;w.remaining_budget['operations']-=1
 except (AssertionError,KeyError,ValueError,TypeError) as ex:reason=str(ex)
 feedback={'selected_work':original,'allowed':allowed,'reason':reason,'result':deepcopy(result)};w.feedback.append(feedback);trace.append({'module':'task_execution_feedback','model_original_choice':original,'allowed':allowed,'rejection_reason':reason,'result':result,'before':before,'after':w.export(),'updated_model_state':deepcopy(w.model_state())});return feedback
