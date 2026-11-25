"""Prepared tasks, create-only online batches, independent native outcome audit."""
from core26 import *

def task_prepare():
 db=read(a2.b.DATA/'db.json');tasks=read(a2.b.DATA/'tasks.json');prior=read(E/'configs/PRIOR_USAGE.json');used=set(prior['orders']);used_tasks=set(prior['task_ids']);manifest=[]
 def clean(o):return o['status']=='delivered' and len({i['item_id'] for i in o['items']})==len(o['items'])
 # Two real existing gift-card routes, reserved before exchange fallback selection.
 specials=[]
 for oid,o in sorted(db['orders'].items()):
  if oid in used or not clean(o):continue
  orig=o['payment_history'][0]['payment_method_id'];g=[k for k,v in db['users'][o['user_id']]['payment_methods'].items() if v['source']=='gift_card' and k!=orig]
  if g:specials.append((oid,g[0]))
  if len(specials)==2:break
 reserved={oid for oid,_ in specials};assert len(reserved)==2
 # Official return task/order matches, one order per base task; never reuse a debug task.
 returns=[]
 for t in sorted(tasks,key=lambda t:int(t['id'])):
  if t['id'] in used_tasks:continue
  for act in (t.get('evaluation_criteria')or{}).get('actions',[]):
   if act['name']!='return_delivered_order_items':continue
   oid=act['arguments']['order_id'];o=db['orders'][oid]
   if oid in used or oid in reserved or any(z[1]==oid for z in returns) or not clean(o):continue
   returns.append((t['id'],oid));break
 # Need 10 source tasks plus two DB-derived refund changes. Structural eligibility is offline.
 assert len(returns)>=10
 selected=[]
 for kind,predicate in [('stable',lambda o:True),('stable',lambda o:True),('evidence',lambda o:True),('evidence',lambda o:True),('scope',lambda o:len(o['items'])>=2),('scope',lambda o:len(o['items'])>=2),('conflict',lambda o:True),('conflict',lambda o:True),('withdraw',lambda o:True),('withdraw',lambda o:True)]:
  pair=next(z for z in returns if z not in [(x[0],x[1]) for x in selected] and predicate(db['orders'][z[1]]));selected.append((*pair,kind));reserved.add(pair[1])
 selected += [('RDB01',specials[0][0],'payment'),('RDB02',specials[1][0],'payment')]
 for tid,oid,kind in selected:
  o=deepcopy(db['orders'][oid]);u=db['users'][o['user_id']];ids=[i['item_id'] for i in o['items']];scope=ids[:min(2,len(ids))];orig=o['payment_history'][0]['payment_method_id'];method='credit_card_0000000' if kind=='conflict' else orig;event={'kind':'none'}
  if kind=='scope':event={'kind':'scope','item_ids':ids[1:min(3,len(ids))]}
  elif kind=='withdraw':event={'kind':'withdraw'}
  elif kind=='payment':event={'kind':'payment','payment_method_id':next(g for oo,g in specials if oo==oid)}
  msg=f"I am {o['user_id']}, email {u['email']}. In order {oid}, I want to return EXACTLY original items {packed(scope)} and keep every other item unchanged. Requested refund method is {method}. This is my return request, not final transaction authorization. Verify the native order and refund rules, show the complete current scope, exact refund total and method, then ask independent approval before registering anything."
  if kind=='conflict':msg+=' If that refund route is prohibited, please first compare the legal routes and explain the policy conflict, then ask which concrete permitted route I accept; do not silently substitute.'
  cfg={'task_id':tid,'business':'return','scenario':kind,'order_id':oid,'user_id':o['user_id'],'scope':scope,'payment_method_id':method,'original_payment':orig,'preferred_payment':orig,'initial_message':msg,'initial_missing':kind=='evidence','event':event,'expected':'stop' if kind=='withdraw' else 'write','environment':{'orders':{oid:o},'users':{o['user_id']:u},'products':{}},'source':'official task controlled single-order return subtask' if not tid.startswith('RDB') else 'new controlled return from untouched public database order'}
  save(E/f'configs/tasks/R_{tid}/case.json',cfg);save(E/f'configs/tasks/R_{tid}/original.json',next(t for t in tasks if t['id']==tid) if not tid.startswith('RDB') else {'public_db_order':o,'user_id':o['user_id']});manifest.append({'id':'R_'+tid,'business':'return','task_id':tid,'order_id':oid,'scenario':kind})
 # All 8 exchange orders are new controlled public DB instances: most official
 # exchange task IDs/orders have already been used in earlier debugging.
 exchange=[]
 for oid,o in sorted(db['orders'].items()):
  if oid in used or oid in reserved or not clean(o) or len(o['items'])<2:continue
  if len({i['product_id'] for i in o['items'][:2]})!=2:continue
  if not all(sum(v['available'] and v['item_id']!=i['item_id'] for v in db['products'][i['product_id']]['variants'].values())>=2 for i in o['items'][:2]):continue
  pm=db['users'][o['user_id']]['payment_methods'][o['payment_history'][0]['payment_method_id']]
  if pm['source']=='gift_card':
   first,second=o['items'][:2];pa=db['products'][first['product_id']];pb=db['products'][second['product_id']];worst=max(money(v['price']) for v in pa['variants'].values() if v['available'] and v['item_id']!=first['item_id'])+min(money(v['price']) for v in pb['variants'].values() if v['available'] and v['item_id']!=second['item_id'])-money(first['price'])-money(second['price'])
   if worst>money(pm['balance']):continue
  exchange.append(oid)
  if len(exchange)==8:break
 for idx,(oid,kind) in enumerate(zip(exchange,['stable','stable','evidence','evidence','resource','resource','requirement','conflict'])):
  tid='EDB'+str(idx+1).zfill(2);o=db['orders'][oid];scope=[i['item_id'] for i in o['items'][:2]];cfg=a2.build_case(tid,oid,scope);cfg.update(business='exchange',scenario=kind,source='controlled exchange from untouched public database order; not an official benchmark task score',cap='10000.00')
  cfg['initial_catalogues']=kind!='evidence';i=scope[0];pid=o['items'][0]['product_id'];vs=[v for v in cfg['environment']['products'][pid]['variants'].values() if v['available'] and v['item_id']not in(i,cfg['targets'][i])];cfg['changed_item']=i;cfg['changed_target']=sorted(vs,key=lambda v:v['item_id'])[0]['item_id'];cfg['change_type']='resource' if kind=='resource' else 'requirement' if kind=='requirement' else 'none';cfg['change_message']=f"Before submission, change ONLY original item {i} to SKU {cfg['changed_target']}, if in stock. Other item and original payment stay unchanged. My previous approval does not authorize this new complete plan; ask fresh approval."
  if kind=='conflict':
   w=a2.BusinessState(cfg,'stable',None);w.initialize_constraints(10000);cap=money((min(Decimal(v['whole_difference']) for v in w.comparison()['negotiable'])+w.difference())/2);assert cap<w.difference();cfg['cap']=str(cap);cfg['initial_message']+=' If the current request conflicts with my cap, compare the feasible specification tradeoffs before asking my new permission.'
  cfg['initial_message']+=f" Maximum signed WHOLE new-minus-original difference <= {cfg['cap']}; a negative limit means MINIMUM refund, not maximum refund."
  save(E/f'configs/tasks/E_{tid}/case.json',cfg);save(E/f'configs/tasks/E_{tid}/original.json',{'public_db_order':o,'selected_scope':scope,'source_db_sha256':sha(a2.b.DATA/'db.json')});manifest.append({'id':'E_'+tid,'business':'exchange','task_id':tid,'order_id':oid,'scenario':kind})
 assert len(manifest)==20 and len({m['order_id'] for m in manifest})==20 and not {m['order_id'] for m in manifest}&used
 # Repeats selected BEFORE any formal calls: resource, conflict, scope and refund method.
 repeat=[next(m['id'] for m in manifest if m['business']==biz and m['scenario']==sc) for biz,sc in [('exchange','resource'),('exchange','conflict'),('return','scope'),('return','payment')]]
 save(E/'configs/TASKS.json',manifest);save(E/'configs/REPEATS.json',repeat)
 # DPO checkpoints use two old exchange preference states and one NEW return order.
 states=[]
 for label,priorities in [('capacity',['capacity','color','material']),('appearance',['color','material','capacity'])]:
  cfg=read(a2.V/'configs/tasks/26/case.json');cfg.update(business='exchange',scenario='preference_conflict',change_type='none',cap=str(money(cfg['caps']['conflict'])));cfg['initial_message']+=' SOFT preference priority highest first: '+packed(priorities)+'. These priorities remain for evaluating an explicitly accepted tradeoff; stock/cap/authorization are hard.';states.append({'id':'E26_'+label,'cfg':cfg,'first_works':['analyze','clarify'],'clarify_parameters':{'variant_id':'1240311797'},'priorities':priorities})
 cfg=read(E/'configs/tasks/R_RDB01/case.json');cfg.update(event={'kind':'none'},expected='write',payment_method_id='credit_card_0000000',preferred_payment=specials[0][1]);cfg['initial_message']=f"I am {cfg['user_id']}, email {cfg['environment']['users'][cfg['user_id']]['email']}. Return exactly {packed(cfg['scope'])} in {cfg['order_id']}. I initially request credit_card_0000000; if not permitted, compare legal routes. My SOFT preference is refund to existing gift card {specials[0][1]} over original {cfg['original_payment']}. I may explicitly accept a legal tradeoff but retain that priority for evaluating the route. Ask new method permission and separate complete return approval."
 states.append({'id':'R_refund_preference','cfg':cfg,'first_works':['analyze','clarify'],'clarify_parameters':{'payment_method_id':cfg['original_payment']},'priorities':[cfg['preferred_payment'],cfg['original_payment']]});save(E/'configs/DPO_CHECKPOINTS.json',states)
 # Separate old-order pilot cases; never included in formal 20-task denominator.
 pilotR=read(E/'configs/tasks/R_RDB01/case.json');old=read(a2.b.DATA/'db.json')['orders']['#W5565470'];user=db['users'][old['user_id']];orig=old['payment_history'][0]['payment_method_id'];pilotR.update(task_id='pilot_return26',order_id=old['order_id'],user_id=old['user_id'],scope=[old['items'][0]['item_id']],payment_method_id=orig,original_payment=orig,preferred_payment=orig,event={'kind':'scope','item_ids':[old['items'][1]['item_id']]},initial_missing=False,environment={'orders':{old['order_id']:old},'users':{old['user_id']:user},'products':{}});pilotR['initial_message']=f"I am {old['user_id']}, email {user['email']}. Return only {pilotR['scope'][0]} from delivered order {old['order_id']} to original payment {orig}. Show complete exact refund amount and method, then ask independent approval.";save(E/'configs/PILOT_RETURN.json',pilotR)
 save(E/'configs/MODEL_BUDGET.json',{'model':'deepseek-flash','temperature':0,'thinking':False,'agent_request_attempts':40,'known_agent_tokens':180000,'operations':24,'turns':35,'max_agent_output':1700,'max_simulator_output':2100,'timeout_seconds':60,'transport_attempts':2,'SDK_retries':0,'stop':'first actual business write or explicit withdrawal acknowledgement; no post-write receipt generation','old_v2_sha256':sha(a2.V/'configs/FREEZE.json')})

def evaluate(w):
 x=w.export();cfg=w.cfg;writes=w.writes
 if cfg.get('expected')=='stop':
  baseline=a2.b.RetailDB.model_validate(deepcopy(cfg['environment'])).model_dump(mode='json');unchanged=w.tools.db.model_dump(mode='json')==baseline;ok=bool(w.change and not writes and unchanged and getattr(w,'terminal_reason',None)=='withdrawal_acknowledged');return {'correct':ok,'checks':{'expected_withdrawal_observed':bool(w.change),'no_write':not writes,'database_unchanged':unchanged,'acknowledged':getattr(w,'terminal_reason',None)=='withdrawal_acknowledged'}}
 checks={'one_write':len(writes)==1}
 if len(writes)!=1:return {'correct':False,'checks':checks}
 wr=writes[0];args=wr['arguments'];order=cfg['environment']['orders'][cfg['order_id']];items={i['item_id']:i for i in order['items']};result=wr['result'];current=w.tools.db.model_dump(mode='json')['orders'][cfg['order_id']]
 checks.update(current_authorization=w.env_valid(args),database_result=current==result,payment=args['payment_method_id']==(w.oracle_payment if w.business=='return' else cfg['payment_method_id']))
 if w.business=='exchange':
  mapping=dict(zip(args['item_ids'],args['new_item_ids']));stock=True;delta=Decimal('0')
  for i,v in mapping.items():
   row=w.tools.db.products[items[i]['product_id']].variants.get(v);stock=stock and row is not None and row.available and i!=v
   if row:delta+=money(row.price)-money(items[i]['price'])
  checks.update(scope=Counter(args['item_ids'])==Counter(cfg['scope']),current_targets=mapping==w.oracle,inventory_product=bool(stock),amount=delta==money(result['exchange_price_difference']),cap=delta<=w.cap,status=result['status']=='exchange requested')
 else:checks.update(scope=Counter(args['item_ids'])==Counter(w.oracle_scope),method=args['payment_method_id']==w.oracle_payment,status=result['status']=='return requested',native_return_items=Counter(result['return_items'])==Counter(w.oracle_scope),native_refund_method=result['return_payment_method_id']==w.oracle_payment)
 return {'correct':all(checks.values()),'checks':checks}

def forced(w,kind,params):
 refs=[0]+(list(w.core.product_refs.values())+[w.cap_ref] if w.business=='exchange' else list(w.refs.values()))
 reason='The current requested route conflicts with observed constraints. Compare the feasible alternatives against the public user preference before choosing what new permission to seek.' if kind=='analyze' else 'Ask permission for this concrete observed compliant alternative, disclosing its tradeoff. Existing initial permission does not authorize this changed option or the whole transaction.'
 return {'work_type':kind,'object':w.cfg['scope'][0] if w.business=='exchange' and kind in('analyze','clarify') else w.cfg['order_id'],'parameters':deepcopy(params) if kind=='clarify' else{},'evidence_refs':sorted(set(refs)),'expected':'return a grounded comparison and negotiable alternatives, without granting authority' if kind=='analyze' else 'obtain concrete new permission or refusal, not transaction approval','reason':reason}

def rollout(out,n,cfg,t,group='framework',first=None,first_params=None):
 w=snapshot(cfg,t,group);t.world=w;t.branch=n;trace=[];error=None;beg=time.perf_counter();save(out/(n+'_start.json'),w.export());save(out/(n+'_visible_start.json'),w.model_state(True) if group=='framework' else w.history);repeated=Counter();retry_program=True
 if group=='official':
  agent=LLMAgent(list(w.tools.get_tools().values()),a2.POLICY,llm=a2.b.MODEL,llm_args={'temperature':0,'max_tokens':1700,'num_retries':0});h=[a2.typed(m) for m in w.history];state=agent.get_init_state(h[:-1]);incoming=h[-1]
 try:
  if first:
   d=forced(w,first,first_params or{});(exchange_execute if w.business=='exchange' else return_execute)(w,d,t,trace)
  for tick in range(35):
   if w.writes or w.stopped:break
   if min(w.remaining_budget.values())<=0:error='budget_exhausted';break
   if group=='framework':
    dis=choose_dispatch(w,program_retry_allowed=retry_program) if w.business=='exchange' else return_dispatch(w,retry_program)
    if dis.route=='state_semantics':
     if w.business=='exchange':semantic(w,t,trace)
     else:w.interpret(t,trace)
     continue
    if dis.route=='finished':break
    visible=deepcopy(w.model_state(True));d=dis.work if dis.route=='program' else choose(w,t,'candidate') if w.business=='exchange' else return_choose(w,t)
    trace.append({'module':'work_selection','source':dis.route,'dispatch_reason':dis.reason,'model_output':deepcopy(d),'visible_state':visible});fb=(exchange_execute if w.business=='exchange' else return_execute)(w,d,t,trace)
    retry_program=fb['allowed']
    if not fb['allowed']:
     k=packed([d['work_type'],d['object'],fb['reason']]);repeated[k]+=1
     if repeated[k]>=3:error='repeated_rejection';break
   else:
    before=w.export();msg,state=agent.generate_next_message(incoming,state);ar=len(w.history);raw={'role':'assistant','content':msg.content}
    if msg.tool_calls:raw['tool_calls']=[{'id':tc.id,'type':'function','function':{'name':tc.name,'arguments':packed(tc.arguments)}} for tc in msg.tool_calls]
    w.history.append(raw)
    if msg.tool_calls:
     outs=[]
     for tc in msg.tool_calls:
      submit=tc.name in ('exchange_delivered_order_items','return_delivered_order_items');auth=w.env_valid(tc.arguments) if submit else None;err=None
      try:
       result=dump(w.tools.use_tool(tc.name,**tc.arguments));w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)})
       if w.business=='exchange':w.core.observe(tc.name,tc.arguments,result,len(w.history)-1)
       else:w.observed[tc.name]=deepcopy(result);w.refs[tc.name]=len(w.history)-1
       if submit:w.writes.append({'arguments':tc.arguments,'result':result,'independent_valid_authorization':auth})
       if tc.name=='transfer_to_human_agents':w.stopped=True;w.terminal_reason='handoff'
      except Exception as ex:err=str(ex);result={'error':err};w.history.append({'role':'tool','tool_call_id':tc.id,'content':packed(result)})
      w.remaining_budget['operations']-=1;trace.append({'module':'native_execution','model_original':msg.model_dump(mode='json'),'tool':tc.name,'arguments':tc.arguments,'independent_authorization':auth,'executed':err is None,'native_error':err,'result':result,'before':before,'after':w.export()});outs.append(ToolMessage(role='tool',id=tc.id,content=packed(result),error=err is not None))
     incoming=MultiToolMessage(role='tool',tool_messages=outs)
    else:
     rec=respond(w,msg.content or'',ar);w.sim_records.append(rec);w.remaining_budget['operations']-=1;trace.append({'module':'native_speech','text':msg.content,'user_result':rec,'before':before,'after':w.export()})
     if w.event_export:
      state.messages.append(UserMessage(role='user',content=rec['reply']));public=[a2.typed(m) for m in w.history[rec['user_ref']+1:]];assert public;state.messages.extend(public[:-1]);incoming=public[-1]
     else:incoming=UserMessage(role='user',content=rec['reply'])
   if w.event_export:trace.append({'module':'public_change','event':w.event_export});w.event_export=None
   save(out/(n+'_trace.json'),trace)
  if not(w.writes or w.stopped):error=error or'loop_limit'
 except Exception as ex:
  from logging16 import sanitize
  error=type(ex).__name__+': '+sanitize(ex,getattr(t.sdk,'secret',None));trace.append({'module':'failure','error':error})
 save(out/(n+'_trace.json'),trace);save(out/(n+'_final.json'),w.export());save(out/(n+'_simulator.json'),w.sim_records);z=evaluate(w);row={'id':n,'task':cfg['task_id'],'business':cfg['business'],'scenario':cfg['scenario'],'group':group,'forced_first':first,'event_triggered':w.change is not None,'error':error,'seconds':time.perf_counter()-beg,**z};print(row,flush=True);return row

def freeze():
 assert read(E/'results/OFFLINE.json')['passed'];assert read(E/'results/GATE25.json')['passed'];p=E/'configs/FREEZE.json';assert not p.exists();files={str(f.relative_to(R)):sha(f) for folder in (E/'src',E/'configs') for f in folder.rglob('*') if f.is_file() and '__pycache__'not in f.parts};save(p,{'files':files,'model_budget':read(E/'configs/MODEL_BUDGET.json'),'round25':read(R/'experiments/preliminary/round25-on-demand-v2/configs/FREEZE.json')})
def verify():
 f=read(E/'configs/FREEZE.json');assert all(sha(R/k)==v for k,v in f['files'].items());a2.verify()
def run(which):
 if not which.startswith('pilot'):verify()
 out=E/'results'/which;out.mkdir(parents=True,exist_ok=False);t=Transport(out);t.install();rows=[]
 if which.startswith('pilot'):
  for f in (E/'src').glob('*.py'):save(out/'development_source'/f.name,{'sha256':sha(f),'source':f.read_text('utf-8')})
  cfg=read(E/'configs/PILOT_RETURN.json');conf=deepcopy(cfg);conf.update(task_id='pilot_return_conflict',event={'kind':'none'},payment_method_id='credit_card_0000000');conf['initial_message']=f"Return EXACTLY {packed(conf['scope'])} from delivered order {conf['order_id']}, my user ID is {conf['user_id']}. I request refund to credit_card_0000000; if prohibited, compare legal routes, ask my permission for a specific legal route, then show exact total and complete scope for separate approval."
  withdraw=deepcopy(cfg);withdraw.update(task_id='pilot_withdraw',scenario='withdraw',expected='stop',event={'kind':'withdraw'})
  excfg=read(a2.E/'configs/A/23/case.json');excfg.update(business='exchange',scenario='resource',cap='10000.00')
  cases=[('withdraw',withdraw)] if which=='pilot03' else [('return_scope',cfg),('return_conflict',conf),('withdraw',withdraw),('exchange_resource',excfg)]
  for label,case in cases:
   for g in ('official','framework'):
    rows.append(rollout(out,'pilot_'+label+'_'+g,case,t,g));save(out/'OUTCOMES.json',rows)
 elif which=='A01':
  tasks=read(E/'configs/TASKS.json');repeats=read(E/'configs/REPEATS.json')
  for ix,m in enumerate(tasks):
   for rep in ((1,2) if m['id'] in repeats else (1,)):
    for g in (('official','framework') if (ix+rep)%2 else ('framework','official')):
     cfg=read(E/f'configs/tasks/{m["id"]}/case.json');n=f'A_{m["id"]}_r{rep}_{g}';rows.append(rollout(out,n,cfg,t,g));save(out/'OUTCOMES.json',rows)
 elif which=='B01':
  for s in read(E/'configs/DPO_CHECKPOINTS.json'):
   for rep in (1,2):
    for first in (s['first_works'] if rep==1 else s['first_works'][::-1]):
     n=f'B_{s["id"]}_r{rep}_{first}';rows.append(rollout(out,n,s['cfg'],t,first=first,first_params=s['clarify_parameters']));save(out/'OUTCOMES.json',rows)
 t.close()
if __name__=='__main__':
 if sys.argv[1]=='prepare':task_prepare()
 elif sys.argv[1]=='freeze':freeze()
 else:run(sys.argv[1])
