import json
from copy import deepcopy
import experiment14 as parent
from exchange_core import packed
from engine import Case
def build(state):
 p=parent.read(parent.HERE/'scenarios/public/task52.json');fixture=deepcopy(p['fixture'])
 for m in fixture['shared_history']:
  if m['role']=='tool':
   v=json.loads(m['content'])
   if isinstance(v,dict) and v.get('product_id')=='8940227892':v['variants']['3892645120']['available']=None;m['content']=packed(v)
 c=Case(fixture,p['verified_interpretation']);ref=len(c.history);q=parent.base.QUOTE;c.history.append({'role':'user','content':q});c.core.evidence[str(ref)]=deepcopy(c.history[-1])
 c.apply_user({'change':{'present':False},'authorization':{'approved':False},'permission_update':{'kind':'grant','variant_id':'3892645120','source_ref':ref,'source_quote':q}},ref-1,ref)
 pending=deepcopy(c.conditional_permission);reference=parent.read(parent.ROOT/'configs/reference14.json');wrapper=json.loads(reference['state']['F']['dialogue'][13]['content'])
 if state=='unknown':wrapper['official_result']['variants']['3892645120']['available']=None
 c.core.observe('get_product_details',wrapper['arguments'],wrapper['official_result'],13);c.resolve_conditional(13);c.core.review([c.changed_item],13)
 if state=='unknown':
  key='match:'+c.changed_item;record=c.core.records[key];c.core.put(key,None,record['depends_on'],[13],status='unknown')
 c.history.append({'role':'observation','work':'inventory','content':packed(wrapper)});c.core.evidence['13']=deepcopy(c.history[-1]);c.permission_history=[pending,deepcopy(c.conditional_permission)]
 return c
OLD_CLARIFY=parent.interface14.clarification
def clarification(c):
 stock=c.core.products['8940227892']['variants']['3892645120']['available']
 if stock is not None:return OLD_CLARIFY(c)
 # Generate same fields/template, replacing only the stock statement without exposing the DB.
 proxy=deepcopy(c);proxy.core.products['8940227892']['variants']['3892645120']['available']=False
 text,fields=OLD_CLARIFY(proxy);text=text.replace('exists but is currently out of stock.','exists, but its stock is not yet verified. Your willingness to accept that 10x variant remains conditional and has not become effective.')
 fields['out_of_stock']['available']=None
 return text,fields
parent.interface14.clarification=clarification
