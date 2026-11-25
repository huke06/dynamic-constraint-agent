import sys,json,time,re
from copy import deepcopy
from datetime import datetime,timezone
from decimal import Decimal
from construct20 import R,read,save,sha
from world20 import World,dump
from transport20 import Transport
from prompts20 import NATIVE_USER_EXTRACT
from runner20 import rollout,POLICY
from exchange_core import packed
from tau2.agent.llm_agent import LLMAgent
from tau2.data_model.message import AssistantMessage,UserMessage,ToolMessage,ToolCall,MultiToolMessage
def typed(m):
 if m['role']=='user':return UserMessage(role='user',content=m['content'])
 if m['role']=='tool':return ToolMessage(role='tool',id=m['tool_call_id'],content=m['content'])
 return AssistantMessage(role='assistant',content=m.get('content'),tool_calls=[ToolCall(id=a['id'],name=a['function']['name'],arguments=json.loads(a['function']['arguments'])) for a in m.get('tool_calls',[])]or None)
def user(w,t,text,ar):
 payload={'actual_assistant':text,'public_scope':w.cfg['scope'],'observed_order':w.core.orders[w.cfg['order_id']],'observed_catalogues':w.core.products,'original_payment':w.cfg['payment_method_id'],'recent_user_messages':[m['content'] for m in w.history if m['role']=='user'][-3:]};p=t.json([{'role':'system','content':NATIVE_USER_EXTRACT},{'role':'user','content':packed(payload)}],'simulator','actual_native_speech_needs_interpretation',max_tokens=2100);literal=lambda key:bool(p.get(key)) and isinstance(p[key],str) and p[key]in text
 if w.writes:
  ref=len(w.history);w.history.append({'role':'user','content':'Thank you.'});w.stopped=True;return {'reply':'Thank you.','extraction':p,'terminal':True,'approved':False,'user_ref':ref}
 if p.get('kind')=='proposal' and p.get('asks') and literal('question_quote'):
  pairs=p.get('pairs',[]);mapping={x.get('item_id'):x.get('new_item_id') for x in pairs};checks={'all_scope':len(pairs)==len(w.cfg['scope']) and set(mapping)==set(w.cfg['scope']),'amount_quoted':literal('amount_quote'),'payment_quoted':literal('payment_quote'),'pair_quotes':all(x.get('quote') and x['quote']in text for x in pairs)};args={'order_id':w.cfg['order_id'],'item_ids':list(w.cfg['scope']),'new_item_ids':[mapping.get(i) for i in w.cfg['scope']],'payment_method_id':p.get('payment_method_id')or(w.cfg['payment_method_id'] if literal('payment_quote') and any(s in p['payment_quote'].lower() for s in ('original','same','paypal','card')) else None)};delta=Decimal('0');rows=[];possible=True;new_oracle=deepcopy(w.oracle)
  for i,v in zip(args['item_ids'],args['new_item_ids']):
   prod=w.product(i);variant=(prod or{}).get('variants',{}).get(v)
   if not variant or variant['available']is not True or v==i:possible=False;continue
   if v!=w.oracle[i]:
    old=w.tools.db.products[w.item(i)['product_id']].variants[w.oracle[i]]
    if old.available:possible=False
    else:new_oracle[i]=v
   d=Decimal(str(variant['price']))-Decimal(str(w.item(i)['price']));delta+=d;rows.append({'item_id':i,'new_item_id':v,'old_price':w.item(i)['price'],'new_price':variant['price'],'difference':float(d),'options':variant['options']})
  checks['observed_stock_and_permitted_change']=possible;checks['payment']=args['payment_method_id']==w.cfg['payment_method_id'];checks['difference']=isinstance(p.get('difference'),(int,float)) and Decimal(str(p['difference']))==delta;checks['literal_amount']=any(abs(Decimal(s))==abs(delta) for s in re.findall(r'-?\d+\.\d{1,2}',p.get('amount_quote','')))
  if all(checks.values()):
   w.oracle=new_oracle;proposal={'arguments':args,'difference':float(delta),'rows':rows};ref=w.reply('confirm',ar,proposal);return {'reply':w.history[ref]['content'],'user_ref':ref,'extraction':p,'checks':checks,'approved':True}
  reply='I have not approved. Please correct '+', '.join(k for k,v in checks.items() if not v)+' and present ALL exchange items with the correct combined net difference and original payment.'
 elif p.get('kind')=='clarification' and literal('question_quote'):
  i=p.get('clarify_item_id');bad=[i for i in w.cfg['scope'] if w.product(i) and w.product(i)['variants'][w.oracle[i]]['available']is False]
  if i not in w.cfg['scope']:i=bad[0] if len(bad)==1 else None
  if i:
   offered=p.get('offered_variant_id');available=[v['item_id'] for v in w.product(i)['variants'].values() if v['available']is True and v['item_id']not in (i,w.oracle[i])];mentioned=[v for v in available if v in text];v=offered if offered in available and offered in text else mentioned[0] if mentioned else available[0] if available else None
   if v:
    detail={'object':i,'offered_variant_id':v,'text':text};ref=w.reply('clarify',ar,detail)
    if not mentioned and offered!=v:
     w.history[ref]['content']=f"I would accept item {v} if in stock. Keep the other items and original payment unchanged; that is not final authorization. Show the entire combined proposal again."
    return {'reply':w.history[ref]['content'],'user_ref':ref,'extraction':p,'approved':False}
  reply='Please keep all unchanged specifications and resolve only the unavailable item; ask me about an actual available alternative.'
 else:reply='Please follow my current request, verify missing facts, and ask for approval of the entire correct combined proposal before writing anything.'
 ref=len(w.history);w.history.append({'role':'user','content':reply});return {'reply':reply,'user_ref':ref,'extraction':p,'approved':False,'checks':locals().get('checks')}
def native_roll(cfg,version,n,t,out):
 w=World(cfg,version,t);t.world=w;t.branch=n;trace=[];start=time.perf_counter();error=None;save(out/(n+'_start.json'),w.export());agent=LLMAgent(list(w.tools.get_tools().values()),POLICY,llm='deepseek-flash',llm_args={'temperature':0,'max_tokens':1700,'num_retries':0});h=[typed(m) for m in w.history];state=agent.get_init_state(h[:-1]);incoming=h[-1]
 try:
  for turn in range(24):
   if w.stopped:break
   if min(w.remaining_budget.values())<=0:error='budget_exhausted';break
   before=w.export();msg,state=agent.generate_next_message(incoming,state);ar=len(w.history);raw={'role':'assistant','content':msg.content}
   # Native tool calls remain standard official ToolCall objects; no project gate.
   if msg.tool_calls:raw['tool_calls']=[{'id':a.id,'type':'function','function':{'name':a.name,'arguments':packed(a.arguments)}} for a in msg.tool_calls]
   w.history.append(raw)
   if msg.tool_calls:
    outputs=[]
    for tc in msg.tool_calls:
     policy={'independent_valid_authorization':w.env_valid(tc.arguments)} if tc.name=='exchange_delivered_order_items' else None;err=None
     try:
      result=dump(w.tools.use_tool(tc.name,**tc.arguments));w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)});w.core.observe(tc.name,tc.arguments,result,len(w.history)-1)
      if tc.name=='exchange_delivered_order_items':w.writes.append({'arguments':tc.arguments,'result':result,'independent':policy})
     except Exception as ex:err=str(ex);result={'error':err};w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)})
     w.remaining_budget['operations']-=1;trace.append({'module':'native_execution','native_tool':tc.name,'parameters':tc.arguments,'assistant_message':msg.model_dump(mode='json'),'before':before,'independent_submit_check':policy,'actual_executed':err is None,'native_error':err,'result':result,'after':w.export()});outputs.append(ToolMessage(role='tool',id=tc.id,content=packed(result),error=err is not None))
    incoming=MultiToolMessage(role='tool',tool_messages=outputs)
   else:
    rec=user(w,t,msg.content or '',ar);w.remaining_budget['operations']-=1;trace.append({'module':'native_speech','assistant_ref':ar,'text':msg.content,'user_result':rec,'before':before,'after':w.export()})
    if w.event_export:
     trace.append({'module':'public_change','snapshot':w.event_export});w.event_export=None;state.messages.append(UserMessage(role='user',content=rec['reply']));incoming=UserMessage(role='user',content='Public inventory/user update: '+w.change['public_text'])
    else:incoming=UserMessage(role='user',content=rec['reply'])
   save(out/(n+'_trajectory.json'),trace)
  if not w.stopped:error=error or 'loop_limit_without_terminal'
 except Exception as ex:
  from logging16 import sanitize
  error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'module':'failure','error':error,'state':w.export()})
 save(out/(n+'_trajectory.json'),trace);save(out/(n+'_final.json'),w.export());result={'id':n,'task_id':cfg['task_id'],'group':'official','version':version,'tier':cfg['tier'],'error':error,'writes':len(w.writes),'event_triggered':w.change is not None,'wall_seconds':time.perf_counter()-start};print(result,flush=True);return result
def pilot():
 out=R/'results/official_pilot';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);t.install();n='official_pilot_t0_changed';r=native_roll(read(R/'configs/stage1/0/case.json'),'changed',n,t,out);save(out/'results.json',{n:r});t.close()
def stage2():
 gate=read(R/'results/GATE.json');assert gate['passed'];f=read(R/'configs/freeze_stage1.json');assert all(sha(R/k)==v for k,v in f['files'].items());save(R/'configs/freeze_stage2.json',{'utc':datetime.now(timezone.utc).isoformat(),'stage1_freeze_sha256':sha(R/'configs/freeze_stage1.json'),'same_files':f['files'],'gate_sha256':sha(R/'results/GATE.json')});out=R/'results/stage2';out.mkdir(exist_ok=True);assert not(out/'started.json').exists();save(out/'started.json',{'utc':datetime.now(timezone.utc).isoformat()});t=Transport(out);t.install();results={}
 for row in read(R/'configs/tasks.json'):
  if row['stage']!='stage2':continue
  tid,tier=row['task_id'],row['tier'];cfg=read(R/f'configs/stage2/{tid}/case.json');ver='changed' if tier=='dynamic' else 'stable'
  for rep in (1,2):
   for group in (('official','ondemand') if rep==1 else ('ondemand','official')):
    n=f'{tier}_t{tid}_r{rep}_{group}';results[n]=native_roll(cfg,ver,n,t,out) if group=='official' else rollout(cfg,ver,group,n,t,out);save(out/'results.json',results)
 t.close()
if __name__=='__main__':{'pilot':pilot,'stage2':stage2}[sys.argv[1]]()
