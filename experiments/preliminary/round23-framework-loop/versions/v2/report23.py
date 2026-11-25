"""Post-run evidence export and accounting; not imported by the frozen runner."""
import sys,json,hashlib
from pathlib import Path
import run23 as run
from dynamic_constraint_agent_v2.evaluation import outcome,first_quality
EXP=run.EXP;REPO=run.REPO
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def calls(folder):return[json.loads(s)for s in(folder/'model_calls.jsonl').read_text('utf-8').splitlines()]
def review_export(phase):
 p=EXP/'results'/phase;lines=[];evidence=[]
 for z in read(p/'OUTCOMES.json'):
  n=z['id'];tr=read(p/(n+'_trace.json'));lines.append(n);claims=[]
  for ix,e in enumerate(tr):
   if e['module']=='cognitive_decision':
    d=e['model_output'];lines.append(f"{ix} {d['work_type']} {d['object']} {d['reason']}");claims.append({'entry':ix,'type':'decision','raw':d,'visible_state':e['state']})
   elif e['module']=='task_execution_feedback':
    a=e.get('result')or{};advice=a.get('model_advice')if isinstance(a,dict)else None
    if advice:lines.append('ANALYSIS '+json.dumps(advice,ensure_ascii=False));claims.append({'entry':ix,'type':'analysis','raw':advice,'program_facts':a['facts'],'current_objects':e['updated_model_state']['objects']})
    if not e['allowed']:lines.append('REJECT '+str(e['rejection_reason']))
   elif e['module']=='semantic_question':lines.append('QUESTION '+json.dumps(e['model_output'],ensure_ascii=False));claims.append({'entry':ix,'type':'question','raw':e['model_output'],'evidence':e.get('visible_input')})
  evidence.append({'id':n,'claims':claims})
 (p/'REVIEW.txt').write_text('\n'.join(lines),encoding='utf-8');save(p/'REVIEW_EVIDENCE.json',evidence)

def score_phase(phase):
 p=EXP/'results'/phase;cs=calls(p);rev=read(EXP/'results/FACT_REVIEW.json')if(EXP/'results/FACT_REVIEW.json').exists()else{};rows=[]
 for z in read(p/'OUTCOMES.json'):
  n=z['id'];x=read(p/(n+'_final.json'));tr=read(p/(n+'_trace.json'));cc=[c for c in cs if c['branch']==n];fr=rev.get(n,{'status':'pending','issues':[]});first=next((e for e in tr if e['module']=='task_execution_feedback'),None);decision=next((e for e in tr if e['module']=='cognitive_decision'),None);usage={k:sum((c['usage']or{}).get(field,0)for c in cc if c['role']!='simulator')for k,field in [('input','prompt_tokens'),('output','completion_tokens'),('cache_hit','prompt_cache_hit_tokens'),('cache_miss','prompt_cache_miss_tokens')]};usage.update(requests=len([c for c in cc if c['role']!='simulator']),unknown=sum(c['usage']is None for c in cc),model_seconds=sum(c['seconds']for c in cc if c['role']!='simulator'))
  result=outcome(x);q=first_quality(decision['model_output'],decision['state'],first['allowed'])if z['checkpoint']and decision and first else None
  rejects=[{'entry':ix,'reason':e['rejection_reason'],'choice':e['model_original_choice']}for ix,e in enumerate(tr)if e['module']=='task_execution_feedback'and not e['allowed']];duplicates=[];seen=set()
  for ix,e in enumerate(tr):
   if e['module']=='task_execution_feedback':
    d=e['normalized_work'];key=(d['work_type'],d['object'],str(e['before']['targets']))
    if d['work_type']in('query','prepare')and key in seen:duplicates.append({'entry':ix,'work_type':d['work_type'],'object':d['object']})
    seen.add(key)
  processed_reuse=[ix for ix,e in enumerate(tr)if e['module']=='semantic_update'and not set(e['model_output'].get('processed_refs',[]))<=set(e['before']['pending'])]
  unsafe=[ix for ix,e in enumerate(tr)if e['module']=='task_execution_feedback'and e['model_original_choice']['work_type']=='submit'and not(e['actual_native']or{}).get('independent_submit_check',{}).get('independent_valid_authorization',False)]
  permission_checks=[]
  for e in tr:
   if e['module']=='task_execution_feedback'and e['model_original_choice']['work_type']=='clarify'and e['allowed']:
    i=e['normalized_work']['object'];v=e['normalized_work']['parameters']['variant_id'];permission_checks.append({'item':i,'variant':v,'env_matches_actual_offer':e['after']['environment_only']['targets'][i]==v,'new_actual_user_messages':[m for m in e['after']['history'][len(e['before']['history']):]if m['role']=='user']})
  strict=(all(q.values())if q else result['correct_registered'])and fr['status']=='supported'and not unsafe and not processed_reuse and not fr.get('simulation_deviation');r={**z,'outcome':result,'first_choice':q,'first_raw_decision':decision and decision['model_output'],'first_executed':first and first['allowed'],'strict_quality':bool(strict),'fact_review':fr,'usage':usage,'rejections':rejects,'repeated_work':duplicates,'processed_reference_reuse':processed_reuse,'unsafe_submit_attempts':unsafe,'actual_permission_checks':permission_checks};rows.append(r)
 save(p/'SCORES.json',rows);return rows

def report():
 old=score_phase('old01');new=score_phase('new01');a=[z for z in new if z['checkpoint']];b=[z for z in new if not z['checkpoint']];lines=['# 首步决策配对表','','首步先由模型提出，随后共同执行；两个组的公共状态一致，候选组仅多工作清单。以下组顺序直接/候选。','','|题/状态/重复|工作类型|对象|类型/对象适切|执行通过|严格质量|调用|输入/输出|','|---|---|---|---|---|---|---|---|']
 pair_a=[]
 for tid in('26','35'):
  for state in('conflict','feasible'):
   for rep in(1,2):
    aa=[next(z for z in a if z['id']==f'A_t{tid}_{state}_r{rep}_{g}')for g in('direct','candidate')];x,y=aa;pair_a.append({'task':tid,'state':state,'repeat':rep,'direct':x,'candidate':y});d=lambda z:z['first_raw_decision'];q=lambda z:str(z['first_choice']['type_appropriate'])+'/'+str(z['first_choice']['object_appropriate']);lines.append(f"|{tid}/{state}/{rep}|{d(x)['work_type']} / {d(y)['work_type']}|{d(x)['object']} / {d(y)['object']}|{q(x)} / {q(y)}|{x['first_executed']} / {y['first_executed']}|{x['strict_quality']} / {y['strict_quality']}|{x['usage']['requests']} / {y['usage']['requests']}|{x['usage']['input']}/{x['usage']['output']} / {y['usage']['input']}/{y['usage']['output']}|")
 (EXP/'FIRST_DECISION_PAIRS.md').write_text('\n'.join(lines),encoding='utf-8');save(EXP/'results/A_PAIRS.json',pair_a)
 pair_b=[];lines=['# 同状态续行对照表','','组顺序：先分析 / 先澄清。首步由试验指定，后续共同direct模型策略。只有严格质量双方通过且用量完整、无环境偏离，才比较投入。','','|题/重复|正确登记|严格质量|请求|输入/输出|命中/未命中|重复工作|耗时秒|可比|','|---|---|---|---|---|---|---|---|---|']
 for tid in('26','35'):
  for rep in(1,2):
   aa=[next(z for z in b if z['id']==f'B_t{tid}_conflict_r{rep}_{first}')for first in('analyze','clarify')];x,y=aa;valid=all(z['strict_quality']and not z['usage']['unknown']for z in aa);pair_b.append({'task':tid,'repeat':rep,'comparable':valid,'analyze':x,'clarify':y});lines.append(f"|{tid}/{rep}|{x['outcome']['correct_registered']} / {y['outcome']['correct_registered']}|{x['strict_quality']} / {y['strict_quality']}|{x['usage']['requests']} / {y['usage']['requests']}|{x['usage']['input']}/{x['usage']['output']} / {y['usage']['input']}/{y['usage']['output']}|{x['usage']['cache_hit']}/{x['usage']['cache_miss']} / {y['usage']['cache_hit']}/{y['usage']['cache_miss']}|{len(x['repeated_work'])} / {len(y['repeated_work'])}|{x['seconds']:.2f} / {y['seconds']:.2f}|{valid}|")
 (EXP/'CONTINUATION_PAIRS.md').write_text('\n'.join(lines),encoding='utf-8');save(EXP/'results/B_PAIRS.json',pair_b)
 save(EXP/'results/ACCOUNTING.json',[{'id':r['id'],'usage':r['usage'],'error':r['error']}for r in old+new]);save(EXP/'results/STATE_COMPARISONS.json',[{'id':r['id'],'transitions':[{'module':e['module'],'before_targets':e['before']['targets'],'after_targets':e['after']['targets'],'before_authorization':e['before']['core']['records'].get('authorization'),'after_authorization':e['after']['core']['records'].get('authorization'),'current_state':e.get('updated_model_state',e.get('current_model_input'))}for e in read(EXP/('results/old01'if r in old else'results/new01')/(r['id']+'_trace.json'))if e['module']in('task_execution_feedback','state_constraint_update')]}for r in old+b])
 print('old',sum(z['outcome']['correct_registered']for z in old),sum(z['strict_quality']for z in old));print('A',[(g,sum(z['strict_quality']for z in a if z['group']==g))for g in('direct','candidate')]);print('B',sum(z['outcome']['correct_registered']for z in b),sum(z['strict_quality']for z in b));print('pairs',[(z['task'],z['repeat'],z['comparable'],z['analyze']['usage']['requests'],z['clarify']['usage']['requests'])for z in pair_b])

def trace(phase,n):
 p=EXP/'results'/phase;tr=read(p/(n+'_trace.json'));start=read(p/(n+'_start.json'));end=read(p/(n+'_final.json'));lines=['# 三模块完整轨迹：'+n,'','## 决策起点（只含当时可见状态）','','```json',json.dumps(read(p/(n+'_visible_start.json')),ensure_ascii=False,indent=2),'```']
 for ix,e in enumerate(tr):
  lines+=['',f"## 事件{ix}：{e['module']}",'']
  obj={k:v for k,v in e.items()if k not in('before','after','state','updated_model_state','current_model_input')};lines+=['```json',json.dumps(obj,ensure_ascii=False,indent=2),'```']
  if 'before'in e and'after'in e:
   lines+=['实际新增公开消息：','```json',json.dumps(e['after']['history'][len(e['before']['history']):],ensure_ascii=False,indent=2),'```','状态更新：','```json',json.dumps({'current_targets':e['after']['targets'],'permission_sources':e['after']['permission_sources'],'authorization':e['after']['core']['records'].get('authorization'),'pending':e['after']['pending']},ensure_ascii=False,indent=2),'```']
 lines+=['','## 实际最终记录与独立核验','','```json',json.dumps({'order':end['database']['orders'][end['cfg']['order_id']],'outcome_checks':outcome(end)},ensure_ascii=False,indent=2),'```'];dest=EXP/f'TRACE_{n}.md';dest.write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
 if sys.argv[1]=='review':review_export(sys.argv[2])
 elif sys.argv[1]=='report':report()
 elif sys.argv[1]=='trace':trace(sys.argv[2],sys.argv[3])
