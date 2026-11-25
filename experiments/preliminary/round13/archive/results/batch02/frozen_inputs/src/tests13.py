from copy import deepcopy
def check():
 import experiment13 as e
 import recovery13 as r
 from fact_verifier import replay
 c,db,ev=e.construct();original=deepcopy(c.conditional_permission)
 assert original['sat']=='未满足' and original['source_quote']==e.QUOTE and c.goal['alternative_permission']=='unknown'
 observed=replay(c.history,len(c.history));v=observed['products']['8940227892']['variants']
 assert v['3892645120']['available'] is False and v['6384525445']['available'] is True and v['7255224608']['available'] is True
 assert any(w['work_id']=='clarify' and w['ready'] for w in c.candidates())
 assert any(w['work_id']=='screen' and w['ready'] for w in c.candidates())
 # Reproduces old completion defect, then verifies new turn-local contract does not accept it.
 assert r.PRE_COMPLETED(c,'permission_rule_acquired') is True
 r.begin(c);assert not c.completed('current_reply_clarification_resolved')
 def answer(c,kind,text,grant=None):
  ar=len(c.history);c.history.append({'role':'assistant','content':'Which available alternative would you accept?'});ur=len(c.history);c.history.append({'role':'user','content':text})
  c.apply_user({'change':{'present':False},'permission_update':{'kind':'grant','variant_id':grant,'source_ref':ur,'source_quote':text} if grant else {'kind':'none'},'authorization':{'approved':False},'clarification_resolution':{'kind':kind,'source_ref':ur,'source_quote':text}},ar,ur)
 # Unclear answer leaves old permission intact but does not complete this work.
 answer(c,'information_unclear','I am not sure yet.');assert c.conditional_permission==original and not c.completed('current_reply_clarification_resolved')
 assert any(w['work_id']=='clarify' for w in c.candidates())
 # Explicit rejection resolves the question but cannot authorize an exchange.
 c2=e.construct()[0];r.begin(c2);answer(c2,'explicit_rejection','I do not want to exchange for any of these alternatives.');assert c2.completed('current_reply_clarification_resolved') and not c2.confirmations and not c2.writes
 # A new, source-bound alternative grant is independent from transaction authorization.
 c3=e.construct()[0];r.begin(c3);answer(c3,'new_permission','I accept item 6384525445 if it is in stock.','6384525445')
 assert c3.completed('current_reply_clarification_resolved') and c3.last_clarification_outcome['new_permission_effective']
 assert any(x['source_quote']==e.QUOTE for x in c3.permission_history)
 w=next(w for w in c3.candidates() if w['work_id']=='prepare');tools=e.b.RetailTools(e.b.RetailDB.model_validate(deepcopy(db)))
 args={'order_id':c3.core.order_id,'item_ids':[c3.changed_item],'new_item_ids':['6384525445'],'payment_method_id':c3.core.payment}
 c3.deterministic(c3.instruction(w,{'arguments':args}),tools)
 submit=next(w for w in c3.candidates() if w['work_id']=='submit');assert not submit['ready']
 try:c3.validate_instruction(c3.instruction(submit));raise AssertionError('unauthorized submit accepted')
 except e.shared.repairs12.Rejected as ex:assert 'authorization_current' in ex.feedback['unmet_preconditions']
 assert e.runtime(e.construct()[0])==e.runtime(e.construct()[0])
 return {'passed':True,'model_calls':0,'old_completion_defect_reproduced':True,'tests':['old permission and source preserved, stock false and effective permission unknown','real tool confirms existing preferred SKU unavailable; alternatives available','clarify ready despite old false rule','old rule cannot complete current clarify before or after unclear reply','new grant / explicit rejection / unclear outcomes distinguished by current reply','new effective alternative permission does not imply complete-plan authorization','submit blocked without current authorization','identical runtime reconstruction across branches']}
