import json,hashlib
from pathlib import Path
from copy import deepcopy
import baseline_runner as b
R=Path(__file__).resolve().parent.parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S1=[('0','#W2378156',['1151293680','4983901480'],['7706410293','7747408585'],'resource'),('58','#W5838674',['7441167885','3478699712'],['3815173328','6017636844'],'resource'),('95','#W2905754',['3478699712','4329558751'],['9844888101',None],'requirement'),('106','#W3388163',['9354168549','9025753381'],['2060066974',None],'requirement')]
S2=[('70','basic','#W3947049',['3358616356'],['9013366374'],'none'),('77','basic','#W1671835',['5081446110'],['3399869890'],'none'),('80','basic','#W7209932',['5047954489'],['9354168549'],'none'),('18','multistep','#W2890441',['8069050545'],[None],'none'),('45','multistep','#W9502127',['6259501109'],[None],'none'),('49','multistep','#W3470184',['2757705742'],[None],'none'),('23','dynamic','#W6876713',['6301799585','7082455361'],['8926329222',None],'resource'),('29','dynamic','#W7181492',['5753502325','8118291112'],['5206946487','8277474082'],'requirement'),('107','dynamic','#W8353027',['6245746168','6130713659'],['3112842858',None],'resource')]
def make():
 db=read(b.DATA/'db.json');ts=read(b.DATA/'tasks.json');manifest=[]
 for stage,specs in [('stage1',S1),('stage2',S2)]:
  for spec in specs:
   if stage=='stage1':tid,oid,scope,wanted,change=spec;tier='paired_multi'
   else:tid,tier,oid,scope,wanted,change=spec
   order=deepcopy(db['orders'][oid]);assert order['status']=='delivered';user=deepcopy(db['users'][order['user_id']]);products={};targets={};initial_options={}
   for iid,want in zip(scope,wanted):
    item=next(i for i in order['items'] if i['item_id']==iid);pid=item['product_id'];prod=deepcopy(db['products'][pid]);products[pid]=prod
    available=[v['item_id'] for v in prod['variants'].values() if v['available']is True and v['item_id']!=iid];unavailable=[v['item_id'] for v in prod['variants'].values() if v['available']is False and v['item_id']!=iid]
    assert available
    target=(unavailable[0] if tier=='multistep' and unavailable else want if want in available else available[0]);targets[iid]=target;initial_options[iid]=prod['variants'][target]['options']
   a=scope[0];pid=next(i['product_id'] for i in order['items'] if i['item_id']==a);alts=[v['item_id'] for v in products[pid]['variants'].values() if v['available']is True and v['item_id']not in (a,targets[a])];assert alts
   changed_target=alts[0];pay=order['payment_history'][0]['payment_method_id'];items=[{'item_id':i,'name':next(x['name'] for x in order['items'] if x['item_id']==i),'requested_variant':targets[i],'options':initial_options[i]} for i in scope]
   msg=f"I am {order['user_id']}; email {user['email']}. In delivered order {oid}, exchange ONLY these items in one complete request: {json.dumps(items)}. Keep every other item and order unchanged. Use original payment {pay}. I accept each named specification only if it is in stock; if unavailable ask before using a different specification. This is specification permission, not transaction approval. Show the complete combined proposal, net difference and payment, then ask for my approval."
   name=items[0]['name'];event=f"Before submission, change the {name} (original item {a}) to item {changed_target} with options {json.dumps(products[pid]['variants'][changed_target]['options'])}, if in stock. Keep the other exchange items and original payment unchanged. My old approval does not authorize the new complete proposal; ask for new final approval."
   cfg={'task_id':tid,'tier':tier,'stage':stage,'order_id':oid,'user_id':order['user_id'],'scope':scope,'targets':targets,'initial_options':initial_options,'payment_method_id':pay,'change_type':change,'changed_item':a,'changed_target':changed_target,'change_message':event,'initial_message':msg,'initial_catalogues':tier!='multistep','environment':{'orders':{oid:order},'users':{order['user_id']:user},'products':products},'adaptation':'Controlled continuation of this public retail base task. Scope/variants/payment explicit in public user message; only one delivered order, distinct original IDs/products. Stage1 selects two items from same order (including archived original two-item tasks 0/58); other scopes adapted. Stage2 held-out task IDs never used in stage1 pilot. No private reference actions enter Agent.'}
   save(R/f'configs/{stage}/{tid}/original_task.json',next(t for t in ts if t['id']==tid));save(R/f'configs/{stage}/{tid}/case.json',cfg);manifest.append({'stage':stage,'task_id':tid,'tier':tier,'order_id':oid,'change':change,'scope':scope})
 save(R/'configs/tasks.json',manifest)
if __name__=='__main__':make()
