"""Source-bound return state repair: canceling approval is not canceling business."""
import sys,importlib.util
from pathlib import Path
V=Path(__file__).resolve().parent;E=V.parents[1]
spec=importlib.util.spec_from_file_location('common_simfix',E/'versions/simfix2/repair.py');sim=importlib.util.module_from_spec(spec);spec.loader.exec_module(sim)
c=sim.c;r=sim.r;read=c.read;save=c.save;sha=c.sha
PROMPT=c.RETURN_SEMANTIC+''' Critical distinction: withdrawal means cancel the ENTIRE return BUSINESS. A message that changes refund method/scope and says OLD APPROVAL is withdrawn is NOT business withdrawal. Emit refund_permission/scope update for the new explicit requirement, and optionally authorization_withdrawal to invalidate only approval. Preserve the active return request. Quote the exact object of withdrawal. Never turn 'ask for new complete approval' into 'stop the business'.'''
def interpret(self,t,trace):
 before=self.export();backup={k:c.deepcopy(getattr(self,k)) for k in ('scope','payment','sources','authorization','withdrawn','pending','parsed_history','analysis_results')};payload={'pending':self.model_state()['pending_user_messages'],'observed_order':self.observed.get('get_order_details'),'legal_methods':self.legal_methods(),'validation_feedback':self.feedback[-1:]};result=t.json([{'role':'system','content':PROMPT},{'role':'user','content':c.packed(payload)}],'semantic','return_reply_authorization_scope_distinction');accepted=[]
 try:
  for u in result.get('updates',[]):
   ref=u['source_ref'];q=u['quote'];assert ref in self.pending and q and q in self.history[ref]['content'],'pending exact user quote required';ask=self.asks.get(str(ref));kind=u['kind'];binding=None
   if kind=='approval':
    if ask and ask['kind']=='confirm' and ask.get('approved') and ask['epoch']==self.env_epoch and c.key(ask['arguments'])==c.key(self.args()) and self.current_plan():self.authorization={'arguments':c.deepcopy(self.args()),'epoch':self.env_epoch,'source_ref':ref,'quote':q};binding='current'
    else:binding='historical_not_current'
   elif kind=='scope':
    ids=u.get('item_ids',[]);same=bool(c.re.search(r'same items|unchanged|as agreed',q,c.re.I))
    if not ids and same:ids=list(self.scope)
    assert self.amount(ids) is not None and (all(i in q for i in ids) or (same and c.Counter(ids)==c.Counter(self.scope))), 'Scope must cite literal IDs or an unchanged same-items reference to the current public scope.'
    self.scope=list(ids);self.sources['scope']=ref;self.authorization=None
   elif kind=='refund_permission':
    method=u['payment_method_id'];assert method in q and method in self.legal_methods();self.payment=method;self.sources['payment']=ref;self.authorization=None
   elif kind=='authorization_withdrawal':self.authorization=None;binding='authorization_only_business_active'
   elif kind=='withdrawal':
    source=self.history[ref]['content'].lower();assert 'entire return request' in source or ('cancel' in source and 'return' in source and 'approval' not in source),'Quote withdraws OLD APPROVAL, not the entire return request; keep business active and update the new refund/scope.';self.withdrawn=True;self.authorization=None
   elif kind not in ('unclear','none'):raise AssertionError('Unknown update kind')
   if kind in ('scope','refund_permission','withdrawal'):
    for a in self.analysis_results:a['active']=False;a['invalidated_by_user_ref']=ref
   self.parsed_history.append({'source_ref':ref,'kind':kind,'quote':q,'binding':binding});accepted.append(kind)
  refs=result.get('processed_refs',[]);assert all(ref in self.pending for ref in refs);self.pending=[ref for ref in self.pending if ref not in refs]
 except (AssertionError,KeyError,ValueError) as ex:
  for k,v in backup.items():setattr(self,k,v)
  self.feedback.append({'kind':'semantic_rejection','reason':str(ex),'output':result})
 trace.append({'module':'semantic_update','model_output':result,'accepted_update_kinds':accepted,'before':before,'after':self.export(),'version':'statefix2'})
c.ReturnState.interpret=interpret
def offline():
 cfg=read(E/'configs/tasks/R_RDB01/case.json');w=r.snapshot(cfg,None,'framework');ev=cfg['event'];ref=len(w.history);text='Before submission, change the refund method to '+ev['payment_method_id']+'. Return the same items. Old approval is withdrawn for this new proposal; ask for new complete approval.';w.history.append({'role':'user','content':text});w.pending=[ref]
 class Fixture:
  def json(self,*args,**kwargs):return {'updates':[{'kind':'refund_permission','source_ref':ref,'quote':text,'payment_method_id':ev['payment_method_id']},{'kind':'scope','source_ref':ref,'quote':'Return the same items','item_ids':list(w.scope)},{'kind':'authorization_withdrawal','source_ref':ref,'quote':text}],'processed_refs':[ref]}
 interpret(w,Fixture(),[]);assert not w.withdrawn and w.payment==ev['payment_method_id'] and not w.pending and not w.current_auth()
 class Bad:
  def json(self,*args,**kwargs):return {'updates':[{'kind':'withdrawal','source_ref':ref,'quote':'Old approval is withdrawn'}],'processed_refs':[ref]}
 w.pending=[ref];interpret(w,Bad(),[]);assert not w.withdrawn and w.pending==[ref] and w.feedback[-1]['kind']=='semantic_rejection'
 save(V/'OFFLINE.json',{'passed':True,'checks':['new method + approval-only withdrawal keeps business active','quote of old approval cannot cancel business','rejection is fed back and pending message retained']})
def freeze():
 assert read(V/'OFFLINE.json')['passed'];r.verify();files=[Path(__file__),E/'versions/simfix1/src/repair.py',E/'versions/simfix2/repair.py'];save(V/'FREEZE.json',{'files':{str(p.relative_to(c.R)):sha(p) for p in files},'affected_tasks':['R_RDB01'],'repeats':{'R_RDB01':[1]},'scope':'return same-items reference binding and specific rejection feedback; retains source-bound withdrawal guard; old snapshots/model/budgets/native tools unchanged'})
def run():
 r.verify();assert all(sha(c.R/k)==v for k,v in read(V/'FREEZE.json')['files'].items());out=V/'results/recheck01';out.mkdir(parents=True,exist_ok=False);t=c.Transport(out);t.install();rows=[]
 for mid,reps in [('R_RDB01',[1])]:
  for rep in reps:
   for g in ('official','framework'):
    n=f'A_{mid}_r{rep}_{g}';rows.append(r.rollout(out,n,read(E/f'configs/tasks/{mid}/case.json'),t,g));save(out/'OUTCOMES.json',rows)
 t.close()
if __name__=='__main__':{'offline':offline,'freeze':freeze,'run':run}[sys.argv[1]]()
