"""Post-run packaging and audits; never part of the frozen decision implementation."""
import json,random,hashlib,sys
from pathlib import Path
from collections import Counter,defaultdict
from construct18 import R,read,save,sha
from score18 import evaluate
def rows(path):return [json.loads(x) for x in path.read_text('utf-8').splitlines()]
def packet():
 items=[]
 for folder in ('main','exploratory'):
  out=R/'results'/folder
  if not(out/'results.json').exists():continue
  for n,meta in read(out/'results.json').items():
   if not(out/(n+'_trajectory.json')).exists():continue
   for i,e in enumerate(read(out/(n+'_trajectory.json'))):
    if 'decision'not in e:continue
    b=e['before'];pid=b['cfg']['product_id'];items.append(({'reason':e['decision']['reason'],'comparison':e['decision'].get('comparison'),'action':e['decision']['action'],'claims':e['decision']['claims'],'latest_visible_catalog':b['ledger']['products'][pid],'current_user_quote':b['history'][b['permission_source']]['content'],'current_permitted_variant':None if b['withdrawn'] else b['desired'],'current_authorization_status':b['ledger']['records'].get('authorization'),'proposal':b['plan'],'history':b['history'],'actual_selected_contract_feedback':e['check']},{'folder':folder,'id':n,'entry':i}))
 random.Random(1801).shuffle(items);pack=[];mapping={}
 for i,(p,m) in enumerate(items,1):code=f'J{i:03d}';pack.append({'code':code,**p});mapping[code]=m
 save(R/'results/REVIEW_PACKET.json',{'limits':'IDs/group/version labels removed and shuffled, but comparison style and task text can reveal them. Same assistant review, not independent blinded gold.','items':pack});save(R/'results/REVIEW_MAPPING.json',mapping);print({'review_items':len(pack)})
def deliver():
 s=read(R/'results/SUMMARY.json');out=R/'results/main';api=rows(out/'model_calls.jsonl');f=read(R/'configs/freeze.json');checks={'frozen_inputs_unchanged':all(sha(R/p)==v for p,v in f['files'].items()),'old_directories_proposal_sources_unchanged':all(sha(Path(p))==v for p,v in f['read_only_sources'].items()),'all32_saved':len(s['rows'])==32,'offline_passed':read(R/'configs/offline.json')['passed'] and read(R/'configs/additional_offline.json')['passed'],'freeze_before_online':f['utc']<read(out/'started.json')['utc']}
 from run18 import messages
 from world18 import World
 checks['first_messages_same_stable_changed']=all(messages(World(read(R/f'configs/tasks/{tid}/adapted.json'),'stable'),g)==messages(World(read(R/f'configs/tasks/{tid}/adapted.json'),'changed'),g) for tid in read(R/'configs/tasks.json') for g in ('free','framework'))
 checks['free_receives_no_state_or_candidates']=all(set(json.loads(a['messages'][1]['content']))=={'interaction_history','remaining_budget'} for a in api if a['branch'].endswith('_free'))
 checks['framework_receives_state_and_candidates']=all({'framework_state','candidate_work'}<=set(json.loads(a['messages'][1]['content'])) for a in api if a['branch'].endswith('_framework'))
 checks['actual_first_messages_equal_stable_changed']=all(next(a['messages'] for a in api if a['branch']==f't{tid}_stable_r{rep}_{g}')==next(a['messages'] for a in api if a['branch']==f't{tid}_changed_r{rep}_{g}') for tid in read(R/'configs/tasks.json') for rep in (1,2) for g in ('free','framework'))
 public_events=[];event_checks=[]
 for tid in read(R/'configs/tasks.json'):
  for rep in (1,2):
   ss=[read(out/f't{tid}_changed_r{rep}_{g}_event_snapshot.json') for g in ('free','framework') if (out/f't{tid}_changed_r{rep}_{g}_event_snapshot.json').exists()]
   event_checks.append(len(ss)==2)
   if len(ss)==2:public_events.append(ss[0]['history'][-1]['content']==ss[1]['history'][-1]['content'])
   for x in ss:
    event_checks.append(not x['writes'] and len(x['ledger']['old_confirmations'])==1)
 checks['same_public_change_content_both_groups']=bool(public_events) and all(public_events)
 checks['all_events_after_real_confirmation_before_write']=all(event_checks)
 ev=rows(out/'request_events.jsonl');checks['requests_balanced']=sum(x['event']=='request_started' for x in ev)==len(api)==sum(x['event']=='request_finished' for x in ev)
 save(R/'results/AUDIT.json',{'passed':all(checks.values()),'checks':checks});assert all(checks.values()),checks
 dims=[]
 for tid in read(R/'configs/tasks.json'):
  for ver in ('stable','changed'):
   for group in ('free','framework'):
    rs=[r for r in s['rows'] if r['task_id']==tid and r['version']==ver and r['group']==group];dims.append({'task_id':tid,'change_type':rs[0]['change_type'],'version':ver,'group':group,'n':len(rs),'correct':sum(r['final_correct'] for r in rs),'quality':sum(r['quality'] for r in rs),'event_reached':sum(r['event_triggered'] for r in rs),'unsafe_attempts':sum(len(r['old_plan_attempts']) for r in rs),'steps':[r['steps'] for r in rs],'first_after_change':[r['first_after_change']['action'] if r['first_after_change'] else None for r in rs]})
 bytype=[]
 for typ in ('resource','requirement','withdrawal'):
  for ver in ('stable','changed'):
   for group in ('free','framework'):
    rs=[r for r in s['rows'] if r['change_type']==typ and r['version']==ver and r['group']==group];bytype.append({'type':typ,'version':ver,'group':group,'independent_tasks':len({r['task_id'] for r in rs}),'trajectories':len(rs),'final_correct':sum(r['final_correct'] for r in rs),'full_quality':sum(r['quality'] for r in rs),'unsafe_attempts':sum(len(r['old_plan_attempts']) for r in rs)})
 save(R/'results/BY_TASK.json',dims);save(R/'results/BY_CHANGE_TYPE.json',bytype)
 tab=['# 按基础任务与变化类型汇总','','独立基础任务4；每格两次重复。F自由，K完整框架。','', '|任务/类型|版本|F/K正确结果|F/K完整质量|F/K不当尝试|F两次步骤|K两次步骤|','|---|---|---|---|---|---|---|']
 for tid in read(R/'configs/tasks.json'):
  for ver in ('stable','changed'):
   a,b=[next(x for x in dims if x['task_id']==tid and x['version']==ver and x['group']==g) for g in ('free','framework')];tab.append('|'+ '|'.join(map(str,[tid+'/'+a['change_type'],ver,str(a['correct'])+'/'+str(b['correct']),str(a['quality'])+'/'+str(b['quality']),str(a['unsafe_attempts'])+'/'+str(b['unsafe_attempts']),a['steps'],b['steps']]))+'|')
 tab+=['','类型汇总见BY_CHANGE_TYPE.json；资源变化有2道独立题，规格修改与撤回各1道，不能据轨迹数夸大独立样本。']
 (R/'results/BY_TASK.md').write_text('\n'.join(tab)+'\n',encoding='utf-8')
 # Reporting-only rendering adds rejection counts and concrete selected objects;
 # scores and resource eligibility remain those of frozen score18.py.
 table=['# 主实验配对结果（F自由/K完整框架）','','正确结果含应办者登记及应停者保持原状；无错误写入不等于无错误尝试。步骤/请求为原始记录，仅质量可比者计算投入差。','', '|基础题|版本/重复|F/K最终正确|F/K变化后首个工作及对象|F/K程序拒绝|F/K不当提交|F/K完整质量|F/K步骤|F/K请求|可比词元F−K|','|---|---|---|---|---|---|---|---|---|---:|']
 for pair in s['pairs']:
  tid,ver,rep=pair['task_id'],pair['version'],pair['repeat'];a,b=[next(x for x in s['rows'] if x['task_id']==tid and x['version']==ver and x['repeat']==rep and x['group']==g) for g in ('free','framework')]
  def selected(x):
   d=x['first_after_change']
   if not d:return '—'
   p=d.get('parameters',{});return d['action']+':'+str(p.get('variant_id') or p.get('arguments',{}).get('new_item_ids','—'))
  table.append('|'+ '|'.join(map(str,[tid,ver+'/'+str(rep),str(a['final_correct'])+'/'+str(b['final_correct']),selected(a)+' / '+selected(b),str(a['program_rejections'])+'/'+str(b['program_rejections']),str(len(a['old_plan_attempts']))+'/'+str(len(b['old_plan_attempts'])),str(a['quality'])+'/'+str(b['quality']),str(a['steps'])+'/'+str(b['steps']),str(a['calls'])+'/'+str(b['calls']),pair['tokens_F_minus_K'] if pair['quality_comparable'] else '—']))+'|')
 (R/'results/PAIRED_RESULTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
 account=[]
 for r in s['rows']:
  aa=[a for a in api if a['branch']==r['id']];t=read(out/(r['id']+'_trajectory.json'));account.append({k:r[k] for k in ('id','calls','prompt_tokens','completion_tokens','returned_tokens','missing_usage','steps','program_rejections')}|{'provider_cache_tokens':sum((a.get('usage')or{}).get('prompt_cache_hit_tokens',0) for a in aa),'environment_user_model_tokens':0,'external_review_model_tokens':0,'executor_wall_seconds_including_io':sum(e.get('wall_seconds',0) for e in t),'executor_process_cpu_seconds':sum(e.get('local_cpu_seconds',0) for e in t),'actual_tool_calls':r['executed_tools']})
 save(R/'results/ACCOUNTING.json',{'primary':account,'common_prefix':'Included in Agent prompt_tokens. Exact separate prefix tokens unknown; provider cache count overlaps and is not a substitute.','simulator_and_review':'Local controlled user and assistant review have no experimental model API calls. Exploratory calls recorded separately.','overhead_limits':'executor CPU/wall measured; pure framework-only overhead not isolated.'})
 save(R/'results/MODEL_VERSIONS.json',[{'id':a['branch'],'status':a['status'],'diagnostic':a.get('diagnostic'),'provider_request_id':a.get('provider_request_id'),**{k:a.get('response',{}).get(k) for k in ('model','system_fingerprint','id','created','usage')}} for a in api])
 # Full paired chronological traces, including attempted and actually executed work.
 for tid in ('6','27','75'):
  text=[f'# 任务{tid}变化版：两组第1次完整轨迹','']
  for group in ('free','framework'):
   n=f't{tid}_changed_r1_{group}';text+=['## '+group,'']
   for j,e in enumerate(read(out/(n+'_trajectory.json'))):
    if 'decision'not in e:text+=['请求/格式异常：'+json.dumps(e,ensure_ascii=False)];continue
    text+=['### 决策'+str(j+1),'模型原始输出：'+json.dumps(e['decision'],ensure_ascii=False),'当时许可原话：'+e['before']['history'][e['before']['permission_source']]['content'],'程序检查/实际工具：'+json.dumps(e['check'],ensure_ascii=False),'执行反馈：'+json.dumps(e['result'],ensure_ascii=False)]
    for ref in (e.get('assistant_ref'),e.get('user_ref')):
     if ref is not None:text+=[e['after']['history'][ref]['role']+'：'+e['after']['history'][ref]['content']]
    if not e['before']['event'] and e['after']['event']:text+=['变化事件：'+json.dumps(e['after']['event'],ensure_ascii=False)]
    text+=['执行后当前许可/授权：'+json.dumps({'variant':e['after']['desired'],'source':e['after']['permission_source'],'authorization_record':e['after']['ledger']['records'].get('authorization')},ensure_ascii=False)]
  (R/f'results/TRACE_TASK{tid}.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
 exp=R/'results/exploratory';exprows=[]
 if(exp/'results.json').exists():
  ep=rows(exp/'model_calls.jsonl')
  for n in read(exp/'results.json'):
   if(exp/(n+'_trajectory.json')).exists():
    row=evaluate(n,exp,ep);row['group']=read(exp/'results.json')[n]['group'];row['prefix_steps']=read(exp/(n+'_start.json'))['steps'];row['continuation_steps']=row['steps']-row['prefix_steps'];exprows.append(row)
  save(R/'results/EXPLORATORY.json',{'primary':False,'rows':exprows,'snapshot_policy':'Two exact event snapshots, each independently restored for state_direct/framework. No preference labels.'})
 print({'checks':checks,'main_final':sum(r['final_correct'] for r in s['rows']),'main_quality':sum(r['quality'] for r in s['rows']),'exploratory':len(exprows)})
if __name__=='__main__':{'packet':packet,'deliver':deliver}[sys.argv[1]]()
