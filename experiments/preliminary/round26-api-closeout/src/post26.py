"""POST-RUN ONLY. Independent native-state scoring and review packets."""
import json,hashlib
from pathlib import Path
from decimal import Decimal
from collections import Counter
E=Path(__file__).resolve().parents[1];R=E.parents[2]
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def packed(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def money(v):return Decimal(str(v)).quantize(Decimal('.01'))
def canon(a):return(a.get('order_id'),a.get('payment_method_id'),tuple(sorted(zip(a['item_ids'],a['new_item_ids']))) if 'new_item_ids' in a else tuple(sorted(a['item_ids'])))
def calls(out):return [json.loads(s) for s in (out/'model_calls.jsonl').read_text('utf-8').splitlines()]
def metrics(cs):
 z={'requests':len(cs),'input':0,'output':0,'cache_hit':0,'cache_miss':0,'usage_complete':True,'failed':0,'seconds':sum(c['seconds'] for c in cs),'roles':dict(Counter(c['role'] for c in cs))}
 for c in cs:
  z['failed']+=c['status']!='success';u=c.get('usage')
  if u is None:z['usage_complete']=False;continue
  z['input']+=u['prompt_tokens'];z['output']+=u['completion_tokens']
  for src,dest in [('prompt_cache_hit_tokens','cache_hit'),('prompt_cache_miss_tokens','cache_miss')]:
   if src not in u:z['usage_complete']=False
   else:z[dest]+=u[src]
 return z

def outcome(start,x):
 cfg=x['cfg'];env=x['environment_only'];ws=x['writes'];kind=cfg['business'];checks={}
 if cfg.get('expected')=='stop':
  checks={'event_observed':x.get('change') is not None,'no_write':not ws,'database_unchanged':x['database']==start['database'],'withdrawal_acknowledged':x.get('terminal_reason')=='withdrawal_acknowledged'};return {'correct':all(checks.values()),'checks':checks}
 checks={'one_write':len(ws)==1}
 if len(ws)!=1:return {'correct':False,'checks':checks}
 w=ws[0];a=w['arguments'];res=w['result'];oid=cfg['order_id'];items={i['item_id']:i for i in cfg['environment']['orders'][oid]['items']};checks.update(order=a['order_id']==oid,authorization=any(z['valid'] and z['epoch']==env['epoch'] and canon(z['arguments'])==canon(a) for z in env['approvals']),database_result=x['database']['orders'][oid]==res)
 if kind=='return':checks.update(scope=Counter(a['item_ids'])==Counter(env['scope']),refund_method=a['payment_method_id']==env['payment'] and res['return_payment_method_id']==env['payment'],native_items=Counter(res['return_items'])==Counter(env['scope']),status=res['status']=='return requested')
 else:
  mapping=dict(zip(a['item_ids'],a['new_item_ids']));stock=True;delta=Decimal('0')
  for i,v in mapping.items():
   row=x['database']['products'][items[i]['product_id']]['variants'].get(v);stock=stock and row is not None and row['available'] is True and v!=i
   if row:delta+=money(row['price'])-money(items[i]['price'])
  checks.update(scope=Counter(a['item_ids'])==Counter(cfg['scope']),current_targets=mapping==env['targets'],inventory_product=stock,amount=delta==money(res['exchange_price_difference']),cap=delta<=Decimal(x['hard_cap']),payment=a['payment_method_id']==cfg['payment_method_id'],status=res['status']=='exchange requested')
 return {'correct':all(checks.values()),'checks':checks}

def summarize(out,label):
 review=read(E/'results/FACT_REVIEW.json') if (E/'results/FACT_REVIEW.json').exists() else{};cs=calls(out);rows=[];packet=[]
 for r in read(out/'OUTCOMES.json'):
  n=r['id'];start=read(out/(n+'_start.json'));x=read(out/(n+'_final.json'));tr=read(out/(n+'_trace.json'));bad=[];rejected=[];steps=[];queries=[];clarifies=[];prepare=[];since_change=False;first_after=None
  branchcalls=[c for c in cs if c['branch']==n];cog=[c for c in branchcalls if c['role']=='cognitive'];cogidx=0
  for ix,e in enumerate(tr):
   m=e['module']
   if m=='public_change':since_change=True;continue
   if m=='work_selection':
    d=e['model_output'];s={'event':ix,'source':e['source'],'work_type':d['work_type'],'object':d['object'],'parameters':d.get('parameters',{}),'reason':d['reason']};steps.append(s)
    if since_change and first_after is None:first_after=s
    if e['source']=='decision_model':
     c=cog[cogidx];cogidx+=1;packet.append({'id':n,'phase':label,'event':ix,'kind':'decision','decision':d,'actual_input':json.loads(c['messages'][1]['content']),'response_id':c['response']['id']})
   elif m=='task_execution_feedback':
    d=e['model_original_choice'];k=d['work_type']
    if not e['allowed']:rejected.append({'event':ix,'work':d,'reason':e['rejection_reason']})
    if k=='query':queries.append(str(d['object']))
    if k=='clarify':clarifies.append(packed([d['object'],d.get('parameters')]))
    if k=='prepare':prepare.append(packed(e['after'].get('plan',{}).get('arguments')))
    if k=='analyze' and e['allowed']:
     result=e.get('result')or{};packet.append({'id':n,'phase':label,'event':ix,'kind':'analysis','result':result,'current_targets':e['before'].get('targets'),'scope':e['before'].get('scope'),'cap':e['before'].get('hard_cap'),'analysis_record':e['after'].get('analysis_results',[])[-1:]})
   elif m=='native_execution':
    s={'event':ix,'work_type':e['tool'],'object':e['arguments'],'reason':e['model_original'].get('content')};steps.append(s)
    if since_change and first_after is None:first_after=s
    if e.get('independent_authorization') is False:bad.append({'event':ix,'kind':'unauthorized_native_attempt','executed':e['executed']})
    if e.get('native_error'):bad.append({'event':ix,'kind':'native_error','error':e['native_error']})
    if e['tool'] in ('get_order_details','get_user_details','get_product_details'):queries.append(packed([e['tool'],e['arguments']]))
   elif m=='native_speech':
    rec=e['user_result'];s={'event':ix,'work_type':rec['kind'],'object':'actual speech','reason':e['text']};steps.append(s)
    if since_change and first_after is None:first_after=s
    packet.append({'id':n,'phase':label,'event':ix,'kind':'speech','text':e['text'],'user_result':rec,'observed_order':e['before'].get('observed',{}).get('get_order_details'),'visible_facts':e['before'].get('observed',e['before'].get('core',{}).get('products',{})),'recent_user_messages':[m['content'] for m in e['before']['history'] if m['role']=='user'][-3:]})
  verdict=review.get(label+'/'+n,{'status':'unreviewed','issues':[]});agent=metrics([c for c in branchcalls if c['role']!='simulator']);sim=metrics([c for c in branchcalls if c['role']=='simulator']);ind=outcome(start,x);eligible=ind['correct'] and not bad and not rejected and r['error'] is None and verdict['status']=='supported' and agent['usage_complete'] and sim['usage_complete'] and not agent['failed'] and not sim['failed']
  rows.append({**r,**ind,'phase':label,'source_dir':str(out),'strict_quality':eligible,'fact_review':verdict,'agent':agent,'simulator':sim,'steps':steps,'first_after_change':first_after,'bad_attempts':bad,'program_rejections':rejected,'repeated_queries':len(queries)-len(set(queries)),'repeated_clarifications':len(clarifies)-len(set(clarifies)),'repeated_prepare':len(prepare)-len(set(prepare)),'initial_prefix':{'messages':len(start['history']),'native_observations':sum(m['role']=='tool' for m in start['history'])},'terminal_reason':x.get('terminal_reason')})
 save(out/'SCORES.json',rows);save(out/'REVIEW_PACKET.json',packet);return rows

def tables(a,repair,b):
 # Raw full planned denominator retained; corrected overlay is separately identified.
 replacement={r['id']:r for r in repair};combined=[replacement.get(r['id'],r) for r in a];save(E/'results/A_EFFECTIVE_SCORES.json',combined);pairs=[]
 for biz in ('exchange','return'):
  lines=[f'# {biz} 官方同批配对','', '数值顺序：官方 / 框架。原始A01成绩不变；“末次定向复验”只是工程定位索引，并非统一修订版的新同批成绩。具体版本见results/A_PAIRS.json。成本结论仅使用RESULTS.md另列的同批、同质量配对。','', '|基础题/重复/情形|原始正确|末次定向复验正确|末次严格质量|末次Agent调用|输入/输出|命中/未命中|模拟调用|质量可比|','|---|---|---|---|---|---|---|---|---|']
  for r in a:
   if r['business']!=biz or r['group']!='official':continue
   n=r['id'];ns=[n,n.replace('_official','_framework')];orig=[next(z for z in a if z['id']==i) for i in ns];xs=[replacement.get(z['id'],z) for z in orig];ok=all(z['strict_quality'] for z in xs);f=lambda fun:' / '.join(str(fun(z)) for z in xs)
   lines.append('|'+n.removeprefix('A_').removesuffix('_official')+'/'+r['scenario']+'|'+' / '.join(str(z['correct']) for z in orig)+'|'+f(lambda z:z['correct'])+'|'+f(lambda z:z['strict_quality'])+'|'+f(lambda z:z['agent']['requests'])+'|'+f(lambda z:f"{z['agent']['input']}/{z['agent']['output']}")+'|'+f(lambda z:f"{z['agent']['cache_hit']}/{z['agent']['cache_miss']}")+'|'+f(lambda z:z['simulator']['requests'])+'|'+str(ok)+'|');pairs.append({'business':biz,'id':n,'task':r['task'],'scenario':r['scenario'],'ids':ns,'phases':[z['phase'] for z in xs],'comparable':ok})
  (E/f'OFFICIAL_{biz.upper()}_PAIRS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 save(E/'results/A_PAIRS.json',pairs)
 bp=[];lines=['# 同状态续行与偏好验收','','|检查点/重复|正确|严格质量|属性/退款偏好|调用 分析/澄清|方向|','|---|---|---|---|---|---|'];candidates=[]
 for s in read(E/'configs/DPO_CHECKPOINTS.json'):
  directions=[]
  for rep in (1,2):
   ids=[f'B_{s["id"]}_r{rep}_{k}' for k in ('analyze','clarify')];xs=[next(z for z in b if z['id']==n) for n in ids];prefs=[]
   for z in xs:
    x=read(Path(z['source_dir'])/(z['id']+'_final.json'));cfg=x['cfg']
    if not z['correct']:prefs.append([]);continue
    args=x['writes'][0]['arguments']
    if cfg['business']=='return':v=[int(args['payment_method_id']==cfg['preferred_payment'])]
    else:
     i=cfg['scope'][0];mapping=dict(zip(args['item_ids'],args['new_item_ids']));o=cfg['environment']['orders'][cfg['order_id']];pid=next(it['product_id'] for it in o['items'] if it['item_id']==i);options=x['database']['products'][pid]['variants'][mapping[i]]['options'];v=[int(options[k]==cfg['initial_options'][i][k]) for k in s['priorities']]
    prefs.append(v)
   ok=all(z['strict_quality'] for z in xs)
   if not ok:direction='pending'
   elif prefs[0]!=prefs[1]:direction='analyze' if prefs[0]>prefs[1] else 'clarify'
   else:
    costs=[(z['agent']['requests'],z['agent']['cache_miss'],z['agent']['output']) for z in xs]
    direction='analyze' if costs[0]!=costs[1] and all(a<=b for a,b in zip(*costs)) else 'clarify' if costs[0]!=costs[1] and all(a>=b for a,b in zip(*costs)) else 'tie'
   directions.append(direction);lines.append(f'|{s["id"]}/{rep}|'+' / '.join(str(z['correct']) for z in xs)+'|'+' / '.join(str(z['strict_quality']) for z in xs)+'|'+str(prefs)+'|'+' / '.join(str(z['agent']['requests']) for z in xs)+'|'+direction+'|');bp.append({'state':s['id'],'repeat':rep,'ids':ids,'direction':direction,'preference_vectors':prefs,'same_input':read(E/'results/B01'/(ids[0]+'_visible_start.json'))==read(E/'results/B01'/(ids[1]+'_visible_start.json'))})
  stable=directions[0]==directions[1] and directions[0] in ('analyze','clarify');candidates.append({'checkpoint':s['id'],'business':s['cfg']['business'],'base_task':s['cfg']['task_id'],'directions':directions,'stable':stable,'winner':directions[0] if stable else None,'status':'export_eligible' if stable else 'tie' if directions==['tie','tie'] else 'pending' if 'pending' in directions else 'reversal','specific_object_and_offer_matter':True})
 (E/'DPO_PATHS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');save(E/'results/DPO_PAIRS.json',bp);save(E/'results/DPO_SELECTION.json',candidates)

if __name__=='__main__':
 a=summarize(E/'results/A01','A01');b=summarize(E/'results/B01','B01');repair=[]
 for name in ['simfix1','simfix2','simfix3','simfix4','statefix1','statefix2','statefix3']:
  for p in sorted((E/'versions'/name/'results').glob('*')):
   if (p/'OUTCOMES.json').exists():repair+=summarize(p,name+'/'+p.name)
 tables(a,repair,b)
