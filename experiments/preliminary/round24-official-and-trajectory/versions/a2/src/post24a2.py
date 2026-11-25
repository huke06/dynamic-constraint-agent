"""POST-RUN ONLY: summaries/review packets. Not loaded by frozen execution."""
from run24a2 import *
from collections import Counter

def calls_for(out,n):return [json.loads(l) for l in (out/'model_calls.jsonl').read_text('utf-8').splitlines() if json.loads(l)['branch']==n]
def outcome24(x):
 # Native exchange arrays are zipped mappings. Their order is not a scope rule.
 z=outcome(x);cfg=x['cfg']
 if len(x['writes'])==1:
  a=x['writes'][0]['arguments'];mapping=dict(zip(a['item_ids'],a['new_item_ids']))
  z['checks']['scope_unchanged']=len(a['item_ids'])==len(cfg['scope']) and len(mapping)==len(cfg['scope']) and set(mapping)==set(cfg['scope'])
  z['checks']['current_user_goal']=mapping==x['environment_only']['targets']
 z['correct_registered']=all(z['checks'].values());return z
def account(calls):
 z={'calls':len(calls),'input':0,'output':0,'cache_hit':0,'cache_miss':0,'usage_complete':True,'seconds':sum(c['seconds'] for c in calls),'roles':dict(Counter(c['role'] for c in calls)),'failed_requests':sum(c['status']!='success' for c in calls)}
 for c in calls:
  u=c.get('usage')
  if not u:z['usage_complete']=False;continue
  z['input']+=u['prompt_tokens'];z['output']+=u['completion_tokens']
  for k,out in [('prompt_cache_hit_tokens','cache_hit'),('prompt_cache_miss_tokens','cache_miss')]:
   if k not in u:z['usage_complete']=False
   else:z[out]+=u[k]
 return z

def summarize(phase):
 out=E/'results'/phase;rows=read(out/'OUTCOMES.json');review=read(E/'results/FACT_REVIEW.json') if (E/'results/FACT_REVIEW.json').exists() else {};scores=[];packet=[]
 for r in rows:
  n=r['id'];x=read(out/(n+'_final.json'));start=read(out/(n+'_start.json'));tr=read(out/(n+'_trace.json'));calls=calls_for(out,n);agent=[c for c in calls if c['role']!='simulator'];sim=[c for c in calls if c['role']=='simulator'];warnings=[];steps=[];queries=[];clars=[];rejections=[];unsafe=[];preps=[];confirms=[];redundant_visible_queries=0
  for j,e in enumerate(tr):
   mod=e['module']
   if mod=='cognitive_decision':
    d=e['model_output'];steps.append({'event':j,'work':d['work_type'],'object':d['object'],'reason':d['reason'],'parameters':d.get('parameters')});packet.append({'id':n,'event':j,'module':mod,'reason':d['reason'],'current_difference':e['state']['current_difference'],'cap':e['state']['hard_constraint'],'stocks':[o['CURRENT_EFFECTIVE_SPECIFICATION']['stock'] for o in e['state']['objects']]})
   if mod=='task_execution_feedback':
    d=e['model_original_choice']
    if not e['allowed']:rejections.append({'event':j,'choice':d,'reason':e['rejection_reason']})
    if d['work_type']=='query':
     queries.append(d['object']);redundant_visible_queries+=int(d['object'] in e['before']['core']['products'])
    if e['allowed'] and d['work_type']=='prepare':preps.append(e['result'].get('fingerprint'))
    if e['allowed'] and d['work_type']=='confirm':confirms.append(e['before']['plan'].get('fingerprint'))
    if d['work_type']=='clarify':clars.append(packed([d['object'],d.get('parameters')]))
    if d['work_type']=='analyze':packet.append({'id':n,'event':j,'module':'analysis','advice':e.get('result',{}).get('model_advice'),'program_facts':e.get('result',{}).get('facts'),'before_targets':e['before']['targets']})
   if mod=='native_execution':
    steps.append({'event':j,'work':e['native_tool'],'object':e['parameters'],'reason':e['model_original'].get('content')})
    if e['native_tool']=='get_product_details':
     queries.append(e['parameters']['product_id']);redundant_visible_queries+=int(e['parameters']['product_id'] in e['before']['core']['products'])
    if e.get('independent_submit_check') and not e['independent_submit_check']['independent_valid_authorization']:unsafe.append(j)
   if mod=='native_speech':
    steps.append({'event':j,'work':'speech','object':e['user_result']['kind'],'reason':e['text']});packet.append({'id':n,'event':j,'module':mod,'text':e['text'],'user_result':e['user_result'],'visible_evidence_history':e['before']['history']})
  change_index=next((i for i,e in enumerate(tr) if e['module']=='public_change'),None)
  after_first=next((s for s in steps if change_index is not None and s['event']>change_index),None)
  simrecords=read(out/(n+'_simulator.json'));sim_ok=True
  # Catalogue object repair is expected adjudication, not silent Agent correction.
  for s in simrecords:
   if s.get('accepted_offer'):
    i=s.get('program_resolved_original_item');v=s['accepted_offer']
    if not i or i not in s['reply'] or v not in s['reply']:sim_ok=False
  verdict=review.get(n,{'status':'unreviewed','issues':[]})
  independent=outcome24(x)
  quality=independent['correct_registered'] and not unsafe and verdict['status']=='supported' and sim_ok and r['error'] is None
  pvec=None;options=None
  if phase=='B01' and r['correct_registered']:
   state=next(s for s in read(E/'configs/B/states.json') if '_'+s['id']+'_' in n);i=x['cfg']['scope'][0];v=x['writes'][0]['arguments']['new_item_ids'][0];prod=x['database']['products'][next(z['product_id'] for z in x['cfg']['environment']['orders'][x['cfg']['order_id']]['items'] if z['item_id']==i)];options=prod['variants'][v]['options'];original=x['cfg']['initial_options'][i];pvec=[int(options.get(k)==original.get(k)) for k in state['priorities']]
  s={**r,**independent,'legacy_order_sensitive_outcome':{'correct_registered':r['correct_registered'],'checks':r['checks']},'strict_quality':quality,'environment_comparable':not verdict.get('environment_issue'),'fact_review':verdict,'agent':account(agent),'simulator':account(sim),'steps':steps,'first_after_change':after_first,'rejections':rejections,'unsafe_attempts':unsafe,'repeated_query_count':len(queries)-len(set(queries)),'query_already_observed_count':redundant_visible_queries,'repeated_clarification_count':len(clars)-len(set(clars)),'repeated_prepare_count':len(preps)-len(set(preps)),'repeated_confirm_count':len(confirms)-len(set(confirms)),'simulator_consistent':sim_ok and 'simulator_contaminated' not in verdict['status'],'preference_vector':pvec,'final_options':options,'final_arguments':x['writes'][0]['arguments'] if x['writes'] else None,'public_prefix':{'history_messages':len(start['history']),'native_tool_observations':len([h for h in start['history'] if h['role']=='tool']),'online_steps':len(steps)}};scores.append(s)
 save(out/'SCORES.json',scores);save(out/'REVIEW_PACKET.json',packet)
 return scores

def tables(a,b):
 lines=['# A 官方与冻结v2配对','', '顺序：官方 / 框架。严格质量包含独立写入核验、事实审阅、无未授权尝试及模拟一致性。','', '|题/重复|正确登记|严格质量|Agent请求|输入/输出|缓存命中/未命中|模拟请求|重复查询|可比较|','|---|---|---|---|---|---|---|---|---|']
 pairs=[]
 for tid in ('80','23','29','43'):
  for rep in (1,2):
   xs=[next(s for s in a if s['id']==f'A_t{tid}_r{rep}_{g}') for g in ('official','framework')];p=all(x['strict_quality'] and x['agent']['usage_complete'] and x['environment_comparable'] for x in xs)
   fmt=lambda fun:' / '.join(str(fun(x)) for x in xs)
   lines.append('|'+f'{tid}/{rep}|'+fmt(lambda x:x['correct_registered'])+'|'+fmt(lambda x:x['strict_quality'])+'|'+fmt(lambda x:x['agent']['calls'])+'|'+fmt(lambda x:f"{x['agent']['input']}/{x['agent']['output']}")+'|'+fmt(lambda x:f"{x['agent']['cache_hit']}/{x['agent']['cache_miss']}")+'|'+fmt(lambda x:x['simulator']['calls'])+'|'+fmt(lambda x:x['repeated_query_count'])+'|'+str(p)+'|');pairs.append({'task':tid,'repeat':rep,'comparable':p,'ids':[x['id'] for x in xs],'after_change':[x['first_after_change'] for x in xs]})
 (E/'OFFICIAL_PAIRS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');save(E/'results/A_PAIRS.json',pairs)
 return
 lines=['# B 同状态续行与偏好候选','', '顺序：先分析 / 先澄清；向量依用户当时可见的优先级逐项记是否保留。硬约束和正确办结在偏好前，投入在偏好后。','', '|状态/重复|正确登记|严格质量|偏好保持向量|请求|输入/输出|方向及依据|','|---|---|---|---|---|---|---|'];candidates=[];bpairs=[]
 for state in read(E/'configs/B/states.json'):
  directions=[]
  for rep in (1,2):
   xs=[next(s for s in b if s['id']==f'B_{state["id"]}_r{rep}_{k}') for k in ('analyze','clarify')];eligible=all(x['strict_quality'] and x['agent']['usage_complete'] for x in xs);direction='pending_quality';why='事实/完整用量待核实'
   if eligible:
    u,v=[x['preference_vector'] for x in xs]
    if u!=v:direction='analyze' if u>v else 'clarify';why='公开软优先级字典序保持度'
    else:
     costs=[(x['agent']['calls'],x['agent']['cache_miss'],x['agent']['output']) for x in xs]
     if all(a<=b for a,b in zip(costs[0],costs[1])) and costs[0]!=costs[1]:direction='analyze';why='同偏好下成本各维不劣'
     elif all(a>=b for a,b in zip(costs[0],costs[1])) and costs[0]!=costs[1]:direction='clarify';why='同偏好下成本各维不劣'
     else:direction='tie';why='同偏好；成本持平或各有取舍'
   directions.append(direction);f=lambda fun:' / '.join(str(fun(x)) for x in xs)
   lines.append('|'+f'{state["id"]}/{rep}|'+f(lambda x:x['correct_registered'])+'|'+f(lambda x:x['strict_quality'])+'|'+f(lambda x:x['preference_vector'])+'|'+f(lambda x:x['agent']['calls'])+'|'+f(lambda x:f"{x['agent']['input']}/{x['agent']['output']}")+'|'+direction+': '+why+'|');bpairs.append({'state':state['id'],'repeat':rep,'priorities':state['priorities'],'ids':[x['id'] for x in xs],'direction':direction,'reason':why,'preference_vectors':[x['preference_vector'] for x in xs]})
  status='stable_candidate' if directions[0]==directions[1] and directions[0] in ('analyze','clarify') else 'tie' if directions==['tie','tie'] else 'pending_quality' if 'pending_quality' in directions else 'unstable'
  candidates.append({'state':state['id'],'base_task':state['task'],'priorities':state['priorities'],'repeat_directions':directions,'status':status,'direction':directions[0] if status=='stable_candidate' else None,'not_training_label':True,'independent_review_required':True,'forced_first_work':True})
 (E/'CONTINUATION_PREFERENCES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');save(E/'results/B2_PAIRS.json',bpairs);save(E/'results/DPO_CANDIDATES.json',candidates)

def audit():
 all_calls=[];phases={};equal={}
 for phase in ('pilot01','pilot02','pilot03','A01','B01'):
  out=E/'results'/phase
  if not (out/'model_calls.jsonl').exists():continue
  calls=[json.loads(l) for l in (out/'model_calls.jsonl').read_text('utf-8').splitlines()];all_calls+=calls;phases[phase]={'agent':account([c for c in calls if c['role']!='simulator']),'simulator':account([c for c in calls if c['role']=='simulator'])}
 for r in read(E/'results/A01/OUTCOMES.json'):
  if r['group']!='official':continue
  a=read(E/'results/A01'/(r['id']+'_start.json'));b0=read(E/'results/A01'/(r['id'].replace('official','framework')+'_start.json'));equal[r['id']]=a==b0
 for r in read(E/'results/B01/OUTCOMES.json'):
  if r['first']!='analyze':continue
  a=read(E/'results/B01'/(r['id']+'_start.json'));b0=read(E/'results/B01'/(r['id'].replace('_analyze','_clarify')+'_start.json'));equal[r['id']]=a==b0
 verify();save(E/'results/ACCOUNTING.json',{'phases':phases,'all_requests':len(all_calls),'models':dict(Counter(c.get('response',{}).get('model','no response') for c in all_calls)),'unknown_usage_requests':sum(c.get('usage') is None for c in all_calls),'external_judge_calls':0,'orchestration_chat_cost':'unknown, excluded','equal_full_paired_starts':equal,'freezes_verified':True})

def trace_md(phase,n):
 out=E/'results'/phase;tr=read(out/(n+'_trace.json'));calls=calls_for(out,n);lines=['# 完整代表轨迹 '+n,'','公开起点与初始工具依据：','```json',packed(read(out/(n+'_start.json'))['history']),'```']
 for j,e in enumerate(tr):
  lines+=['',f'## {j} · '+e['module'],'```json']
  if e['module']=='cognitive_decision':show=e
  elif e['module']=='task_execution_feedback':show={k:e.get(k) for k in ('model_original_choice','normalized_work','allowed','rejection_reason','actual_native','result','updated_model_state')}
  elif e['module']=='semantic_update':show={k:e.get(k) for k in ('model_output','trigger_reason')};show['before_pending']=e['before']['pending'];show['after_targets']=e['after']['targets'];show['after_authorization']=e['after']['core'].get('records',{}).get('authorization');show['actual_user_messages']=[e['before']['history'][r] for r in e['before']['pending']]
  elif e['module']=='native_execution':show={k:v for k,v in e.items() if k not in ('before','after')}
  elif e['module']=='native_speech':show={k:v for k,v in e.items() if k not in ('before','after')}
  elif e['module']=='public_change':show={'kind':e['event']['state']['change'],'after_targets':e['event']['state']['targets'],'before_records':e['event']['before_records'],'after_records':e['event']['after_records']}
  else:show=e
  lines.extend([json.dumps(show,ensure_ascii=False,indent=2),'```'])
 lines+=['','## 每次实际调用','']
 for c in calls:lines.append(packed({'role':c['role'],'trigger':c['trigger_reason'],'model':c.get('response',{}).get('model'),'id':c.get('response',{}).get('id'),'usage':c['usage'],'seconds':c['seconds'],'status':c['status']}))
 lines+=['','## 实际最终登记','```json',json.dumps(read(out/(n+'_final.json'))['writes'],ensure_ascii=False,indent=2),'```']
 (E/(n+'_FULL_TRACE.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':
 a=summarize('A01');tables(a,[])
 for n in ['A_t23_r1_official','A_t23_r1_framework','A_t43_r1_official','A_t43_r1_framework']:trace_md('A01',n)
