from copy import deepcopy
def check():
 import experiment17 as e
 import helmet17 as h
 a=e.load('unknown_out');b=e.load('unknown_in');assert a.state()==b.state() and a.compact()==b.compact()
 assert 'historical_plan_compatible' not in a.compact()['C'] and a.compact()['user_intent_and_permission']['alternative_status']=='not_yet_accepted'
 expected={False:-0.44,True:22.55}
 for state,stock in [('unknown_out',False),('unknown_in',True)]:
  c=e.load(state);db=e.environment(state);tools=e.b.RetailTools(e.b.RetailDB.model_validate(deepcopy(db)));w=next(w for w in c.candidates() if w['work_id']=='inventory');c.deterministic(c.instruction(w),tools)
  assert c.core.products[h.PID]['variants'][h.TARGET]['available'] is stock
  assert (c.goal['alternative_permission']==h.TARGET) is stock
  if stock:
   prep=next(w for w in c.candidates() if w['work_id']=='prepare');args={'order_id':c.core.order_id,'item_ids':[h.ITEM],'new_item_ids':[h.TARGET],'payment_method_id':c.core.payment};c.deterministic(c.instruction(prep,{'arguments':args}),tools);assert c.plan['quote']['difference']==22.55;assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
  else:assert any(w['work_id']=='clarify' and w['ready'] for w in c.candidates())
 k=e.load('known_out');prod=k.core.products[h.PID];assert prod['variants'][h.TARGET]['available'] is False and prod['variants'][h.ALT]['available'] is True
 assert round(prod['variants'][h.ALT]['price']-k.core.item(h.ITEM)['price'],2)==-0.44
 assert k.core.users[k.core.authenticated]['payment_methods'][k.core.payment]['last_four']=='7312'
 return {'passed':True,'model_calls':0,'tests':['unknown public states/candidate menus equal','only target DB stock differs','queries activate original permission only when true','true quote22.55 needs fresh authorization','false has observed fallback196.89 and refund0.44','original Visa ending7312 observed','historical compatibility moved out of current C','not-yet-accepted is explicitly distinct from rejection'],'adapted_user_quote':h.QUOTE}
