"""Frozen deterministic outcome checks, distinct from semantic evidence review."""
from decimal import Decimal
from copy import deepcopy
def canonical(a):return(a['order_id'],a['payment_method_id'],tuple(sorted(zip(a['item_ids'],a['new_item_ids']))))
def outcome(x):
 cfg=x['cfg'];writes=x['writes'];env=x['environment_only'];checks={'one_write':len(writes)==1,'current_authorization':False,'current_user_goal':False,'exact_amount':False,'hard_cap':False,'native_status':False,'scope_unchanged':False,'inventory_and_product':False,'payment':False}
 if len(writes)==1:
  w=writes[0];a=w['arguments'];order=cfg['environment']['orders'][cfg['order_id']];items={i['item_id']:i for i in order['items']};delta=Decimal('0');stock=True
  for i,v in zip(a['item_ids'],a['new_item_ids']):
   p=x['database']['products'][items[i]['product_id']];row=p['variants'].get(v);stock=stock and row is not None and row['available']is True and v!=i
   if row:delta+=Decimal(str(row['price']))-Decimal(str(items[i]['price']))
  checks.update(current_authorization=any(z['valid']and z['epoch']==env['epoch']and canonical(z['arguments'])==canonical(a)for z in env['approvals']),current_user_goal=a['new_item_ids']==[env['targets'][i]for i in cfg['scope']],exact_amount=delta==Decimal(str(w['result']['exchange_price_difference'])),hard_cap=delta<=Decimal(x['hard_cap']),native_status=w['result']['status']=='exchange requested'and x['database']['orders'][cfg['order_id']]==w['result'],scope_unchanged=a['item_ids']==cfg['scope'],inventory_and_product=stock,payment=a['payment_method_id']==cfg['payment_method_id'])
 return {'correct_registered':all(checks.values()),'checks':checks}
def first_quality(d,state,allowed):
 if not d:return {'type_appropriate':False,'object_appropriate':False,'allowed':False}
 i=state['objects'][0]['original_item_id'];oid=state['order_id'];p=state['objects'][0]['product_id'];k=d.get('work_type');obj=d.get('object');obj=oid if obj==oid.lstrip('#')else obj;expected=p if k=='query'else i if k in('analyze','clarify')else oid
 if state['current_full_authorization']:accepted={'submit','analyze'}
 elif state['current_plan_valid']:accepted={'confirm','analyze'}
 elif state['constraint_judgments']['status']=='evidence_insufficient':accepted={'query'}
 elif state['constraint_judgments']['status']=='no_exact_match':accepted={'analyze','clarify'}
 else:accepted={'prepare','analyze','clarify'}
 return {'type_appropriate':k in accepted,'object_appropriate':obj==expected,'allowed':allowed}
