from copy import deepcopy
def check():
 import experiment12 as e
 import repairs12 as r
 c=e.load_start('70','unknown');w=next(w for w in c.candidates() if w['work_id']=='screen')
 try:c.validate_instruction(c.instruction(w));raise AssertionError('unknown stock accepted')
 except r.Rejected as ex:assert ex.feedback['unmet_preconditions'] and 'unknown' in ex.feedback['specific_gap']
 camera=e.load_start('52','known');ref=len(camera.history);quote='If item 3892645120 is in stock I accept it.'
 camera.history.append({'role':'user','content':quote})
 camera.remember_conditional({'grant':True,'variant_id':'3892645120','source_quote':quote},ref)
 assert r.permission_state(camera)=='false'
 assert any(w['work_id']=='clarify' and w['ready'] for w in camera.candidates())
 assert camera.conditional_permission['source_quote']==quote
 c=e.original_start();p=r.confirmation(c)
 assert p['rows'][0]['available'] is True and p['difference']==22.55 and p['payment_method']['last_four']=='7312'
 assert 'old_keyboard_match' not in c.compact()['C']
 c=e.authorized_start();before=c.state();ev=e.inject(c,None,'offline');after=c.state()
 assert not c.plan and not c.confirmations and c.core.records['authorization']['status']=='stale'
 for k in ('identity','order','catalog','catalog_sources','payment'):assert before['F'][k]==after['F'][k]
 assert c.core.products['7765186836']['variants']['1665571435']['available'] is None
 for tid in ('70','52'):
  for st in ('known','unknown'):assert e.load_start(tid,st).state()==e.load_start(tid,st).state()
 # A reply changing requirements while saying yes cannot authorize the prior plan.
 c=e.original_start();i=len(c.history);q='Yes, but change the color to black.';c.history.append({'role':'user','content':q})
 c.apply_user({'change':{'present':True,'ambiguous':False,'source_ref':i,'source_quote':q,'hard_options':{'color':'black'},'preferred_options':{}},'permission_update':{'kind':'none'},'authorization':{'approved':True,'source_ref':i,'source_quote':q}},i-1,i)
 assert not c.confirmations and c.plan is None
 return {'passed':True,'model_calls':0,'tests':['selected-work feedback identifies stock observation gap','false conditional permission preserved and clarification available','current confirmation uses true stock, Decimal quote, real payment','original authorization invalid after change while identity/order/catalog/payment retained','simultaneous yes and changed requirements does not authorize old plan','all paired start constructions equal','historical-match label replaced by recomputed compatibility']}
