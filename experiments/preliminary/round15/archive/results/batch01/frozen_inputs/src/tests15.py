import json
from copy import deepcopy
def check():
 import experiment15 as e
 from fact_verifier import replay
 a=e.load15('known');b=e.load15('unknown');p='8940227892';v='3892645120'
 assert a.history[:13]==b.history[:13]
 x=json.loads(a.history[13]['content']);y=json.loads(b.history[13]['content']);x['official_result']['variants'][v]['available']=None;assert x==y
 assert a.goal['hard_options']==b.goal['hard_options'] and a.goal['preferred_options']==b.goal['preferred_options']
 assert a.conditional_permission['sat']=='未满足' and b.conditional_permission['sat']=='未知'
 # Scan every serialized catalogue/rule/permission-event in unknown runtime, including history JSON strings.
 seen=[]
 def scan(x):
  if isinstance(x,str):
   try:scan(json.loads(x))
   except (ValueError,TypeError):pass
  elif isinstance(x,list):
   for z in x:scan(z)
  elif isinstance(x,dict):
   if x.get('item_id')==v and 'available'in x:assert x['available'] is None;seen.append(1)
   if x.get('variant_id')==v and 'stock'in x:assert x['stock'] is None
   if x.get('variant_id')==v and 'sat'in x:assert x['sat']=='未知'
   for z in x.values():scan(z)
 scan(e.base.runtime(b));assert seen
 assert replay(b.history,len(b.history))['products'][p]['variants'][v]['available'] is None
 assert 'not yet verified' in e.interface14.clarification(b)[0]
 db=e.read(e.HERE/'scenarios/initial_database.json');tools=e.b.RetailTools(e.b.RetailDB.model_validate(deepcopy(db)))
 w=next(w for w in b.candidates() if w['work_id']=='inventory');b.deterministic(b.instruction(w),tools);assert b.core.products[p]['variants'][v]['available'] is False and b.conditional_permission['sat']=='未满足'
 for c in (a,e.load15('unknown')):
  assert not next(w for w in c.candidates() if w['work_id']=='prepare')['ready'];assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
 return {'passed':True,'tests':['public history differs only observation13 specified available false/null','all other product observations and user words equal','all serialized unknown runtime catalogue/rules/permission events scanned for stock leak','permission state recomputed false vs unknown','neutral unknown clarification accurate','real tool reveals false and updates conditional permission','prepare/submit blocked without permission and current authorization'],'model_calls':0,'scan_occurrences':len(seen)}
