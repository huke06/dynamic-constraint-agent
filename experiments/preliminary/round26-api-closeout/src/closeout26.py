"""Post-run report material, immutable raw archive index and accounting."""
from post26 import *
import shutil

def slim(x):
 keys=['business','scope','payment','targets','hard_cap','plan','authorization','pending','parsed_history','withdrawn','stopped','change','terminal_reason','specification_permissions','current_full_authorization']
 z={k:x[k] for k in keys if k in x}
 if 'core' in x:z['core']={k:v for k,v in x['core'].items() if k not in ('products','db','history','cfg')}
 return z

def run():
 a=read(E/'results/A01/SCORES.json');b=read(E/'results/B01/SCORES.json');phases=[(E/'results/A01','A01'),(E/'results/B01','B01')]
 for name in ['simfix1','simfix2','simfix3','simfix4','statefix1','statefix2','statefix3']:
  for p in sorted((E/'versions'/name/'results').glob('*')):
   if (p/'SCORES.json').exists():phases.append((p,name+'/'+p.name))
 cohort={}
 for biz in ('exchange','return'):
  for g in ('official','framework'):
   xs=[r for r in a if r['business']==biz and r['group']==g];cohort[biz+'/'+g]={'n':len(xs),'correct':sum(r['correct'] for r in xs),'strict':sum(r['strict_quality'] for r in xs),'event_triggered':sum(r['event_triggered'] for r in xs),'bad_attempts':sum(len(r['bad_attempts']) for r in xs),'program_rejections':sum(len(r['program_rejections']) for r in xs)}
 pairs=[];lines=['# 原始A01：全部预选题配对','','数值顺序为官方/框架；20个基础订单，预定4题复验另列，不能将重复当独立题。定向修复不替换此表。','', '|业务/任务/重复|情形|正确终态|事实/理由审阅|事件实际触发|同质量可比|Agent请求|输入|输出|缓存命中/未命中|耗时秒（端到端）|','|---|---|---|---|---|---|---|---|---|---|---|']
 for off in [r for r in a if r['group']=='official']:
  fw=next(r for r in a if r['id']==off['id'].replace('_official','_framework'));xs=[off,fw];good=all(r['strict_quality'] for r in xs);f=lambda fun:' / '.join(str(fun(r)) for r in xs)
  pairs.append({'task':off['task'],'business':off['business'],'repeat':2 if '_r2_' in off['id'] else 1,'ids':[r['id'] for r in xs],'comparable':good,'agent':[r['agent'] for r in xs],'end_to_end_seconds':[r['seconds'] for r in xs]})
  lines.append('|'+off['business']+'/'+off['id'].removesuffix('_official')+'|'+off['scenario']+'|'+f(lambda r:r['correct'])+'|'+f(lambda r:r['fact_review']['status'])+'|'+f(lambda r:r['event_triggered'])+'|'+str(good)+'|'+f(lambda r:r['agent']['requests'])+'|'+f(lambda r:r['agent']['input'])+'|'+f(lambda r:r['agent']['output'])+'|'+f(lambda r:str(r['agent']['cache_hit'])+'/'+str(r['agent']['cache_miss']))+'|'+f(lambda r:round(r['seconds'],2))+'|')
 (E/'OFFICIAL_RAW_PAIRS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');save(E/'results/RAW_PAIRS.json',pairs)
 costs={k:[sum(p['agent'][j][k] for p in pairs if p['comparable']) for j in (0,1)] for k in ['requests','input','output','cache_hit','cache_miss','seconds']};costs['pairs']=sum(p['comparable'] for p in pairs);costs['bases']=len(set((p['business'],p['task']) for p in pairs if p['comparable']));costs['end_to_end_seconds']=[sum(p['end_to_end_seconds'][j] for p in pairs if p['comparable']) for j in (0,1)]
 save(E/'results/COHORT_SUMMARY.json',{'raw_A01':cohort,'raw_same_quality_costs':costs,'main_40':{g:sum(r['correct'] for r in a if r['group']==g and '_r1_' in r['id']) for g in ('official','framework')},'repeats_8':{g:sum(r['correct'] for r in a if r['group']==g and '_r2_' in r['id']) for g in ('official','framework')}})
 lines=['# 定向修复：逐批保留','','均为原失败涉及题目的独立重新采样；不与原A01合并成成功率。修复前后模型采样有波动，不能只挑成功版本替换原分数。','', '|冻结版本/批次|轨迹|正确|未办结|','|---|---|---|---|']
 for p,label in phases[2:]:
  xs=read(p/'SCORES.json');lines.append(f'|{label}|{len(xs)}|{sum(r["correct"] for r in xs)}|'+', '.join(r['id']+':'+str(r.get('error')or r['terminal_reason']) for r in xs if not r['correct'])+'|')
 (E/'TARGETED_RECHECKS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 # Every round26 request log, including development and aborted attempts, is counted once.
 ledger=[]
 for path in sorted(E.rglob('model_calls.jsonl')):
  cs=calls(path.parent);ev=path.parent/'request_events.jsonl';events=[json.loads(l) for l in ev.read_text('utf-8').splitlines()] if ev.exists() else[];starts=sum(e.get('event')=='request_started' for e in events);finishes=sum(e.get('event')=='request_finished' for e in events)
  ledger.append({'phase':str(path.parent.relative_to(E)),'logged_requests':len(cs),'request_started':starts,'request_finished':finishes,'unfinished_usage_unknown':max(0,starts-finishes),'status_counts':dict(Counter(c['status'] for c in cs)),'agent':metrics([c for c in cs if c['role']!='simulator']),'simulator':metrics([c for c in cs if c['role']=='simulator']),'actual_model_values':dict(Counter(c.get('response',{}).get('model','not_returned') for c in cs)),'diagnostics':[{'branch':c['branch'],'role':c['role'],'diagnostic':c.get('diagnostic'),'usage':c.get('usage'),'status':c['status'],'provider_request_id':c.get('provider_request_id')} for c in cs if c['status']!='success']})
 save(E/'results/REQUEST_LEDGER.json',ledger)
 ml=['# 请求与用量总账','','Agent与模拟用户分别记录。seconds为请求等待合计，端到端时间另见原始配对；未知usage不补0。外部评分无API调用；本助手编排消耗无法从这些日志计量，单列未知。','', '|批次|已记录/启动/结束|Agent请求/输入/输出|命中/未命中|模拟请求/输入/输出|未完成用量未知|','|---|---|---|---|---|---|']
 for z in ledger:
  ag=z['agent'];sm=z['simulator'];ml.append(f'|{z["phase"]}|{z["logged_requests"]}/{z["request_started"]}/{z["request_finished"]}|{ag["requests"]}/{ag["input"]}/{ag["output"]}|{ag["cache_hit"]}/{ag["cache_miss"]}|{sm["requests"]}/{sm["input"]}/{sm["output"]}|{z["unfinished_usage_unknown"]}|')
 (E/'REQUEST_ACCOUNTING.md').write_text('\n'.join(ml)+'\n',encoding='utf-8')
 # Lossless conversation + all ordered action records; bulky repeated states remain in raw JSON.
 def trace_doc(filename,title,selected):
  lines=['# '+title,'','以下逐条保留完整公开对话、工具记录、模型选择和执行反馈。每轮重复的全库快照另见对应原始trace；这里列出受影响状态。']
  for phase,n in selected:
   p=E/phase;tr=read(p/(n+'_trace.json'));fin=read(p/(n+'_final.json'));lines+=['','## '+phase+'/'+n,'','### 完整公开消息','', '```json',json.dumps(fin['history'],ensure_ascii=False,indent=2),'```','','### 三模块逐轮记录','']
   for ix,e in enumerate(tr):
    z={k:v for k,v in e.items() if k not in ('before','after','visible_state')}
    for k in ('before','after'):
     if k in e:z[k]=slim(e[k])
    if 'visible_state'in e:z['visible_state']=e['visible_state']
    lines += [f'事件 {ix}：{e["module"]}','```json',json.dumps(z,ensure_ascii=False,indent=2),'```']
   lines+=['','### 实际终态','```json',json.dumps({'writes':fin['writes'],'terminal_reason':fin.get('terminal_reason'),'order':fin['database']['orders'][fin['cfg']['order_id']],'source_trace_sha256':sha(p/(n+'_trace.json'))},ensure_ascii=False,indent=2),'```']
  (E/filename).write_text('\n'.join(lines)+'\n',encoding='utf-8')
 trace_doc('TRACE_EXCHANGE_CONFLICT.md','换货冲突：相同终态不掩盖中间cap判断错误',[('results/A01','A_E_EDB08_r1_official'),('results/A01','A_E_EDB08_r1_framework')])
 trace_doc('TRACE_RETURN_METHOD.md','退货方式变化：原始断点、修复成功及重复中的剩余失败',[('results/A01','A_R_RDB01_r1_official'),('results/A01','A_R_RDB01_r1_framework'),('versions/statefix3/results/recheck01','A_R_RDB01_r1_framework'),('versions/statefix3/results/recheck01','A_R_RDB01_r2_framework')])
 lines=['# 变化前后与三个模块','','状态=当前要求/事实/授权；决策=模型原始选择；执行/反馈=共同门禁、原生工具及后续状态。完整原话和SHA见两份代表轨迹。','']
 for row in a:
  if row['group']!='framework' or not row['event_triggered']:continue
  tr=read(E/'results/A01'/(row['id']+'_trace.json'));lines+=['## '+row['id'],'']
  for ix,e in enumerate(tr):
   if e['module'] in ('public_change','semantic_update'):
    lines+=['```json',json.dumps({'event':ix,'module':e['module'],'change':e.get('change',e.get('result')),'model_update':e.get('model_output'),'before':slim(e.get('before',{})),'after':slim(e.get('after',{}))},ensure_ascii=False,indent=2),'```']
  lines+=['首个后续工作：`'+packed(row['first_after_change'])+'`','']
 (E/'STATE_TRANSITIONS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('cohort',cohort,'cost',costs,'formal_extra',sum(len(read(p/'SCORES.json')) for p,_ in phases[2:]))

if __name__=='__main__':run()
