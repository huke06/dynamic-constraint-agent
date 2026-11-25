# Post-run reporting only. Not imported by the frozen Agent.
"""Post-run evidence export/reporting only; never imported by frozen execution."""
import sys,json,hashlib
from collections import Counter,defaultdict
from construct20 import R,read,save,sha
from score20 import linefile

def excerpts(folder):
 out=R/'results'/folder;rows=[];mapping={}
 for n in read(out/'results.json'):
  tr=read(out/(n+'_trajectory.json'));final=read(out/(n+'_final.json'));ref='R'+hashlib.sha256(n.encode()).hexdigest()[:8];mapping[ref]=n;claims=[]
  for ix,e in enumerate(tr):
   module=e.get('module');d=e.get('model_output',{})
   if d:
    st=e.get('visible_state')or e.get('before',{});goal=st.get('goal',{});claims.append({'entry':ix,'kind':module,'work':d.get('work_type'),'object':d.get('object'),'reason':d.get('reason'),'analysis':d.get('analysis'),'question':d.get('question'),'updates':d.get('updates'), 'inventory':[(i['item_id'],i['requested_variant'],i['condition_stock']) for i in goal.get('scope',[])],'current_authorization':st.get('current_authorization'),'current_order_status':st.get('current_order_status')})
   if module=='native_speech':claims.append({'entry':ix,'kind':module,'text':e['text'],'checks':e['user_result'].get('checks'),'extraction':e['user_result'].get('extraction'),'latest_products':e['before']['core']['products'],'order_status':e['before']['database']['orders'][final['cfg']['order_id']]['status']})
  rows.append({'blind_ref':ref,'claims':claims,'source_file':n+'_trajectory.json'})
 save(R/f'results/{folder}_review_mapping.json',mapping);save(R/f'results/{folder}_REVIEW_EVIDENCE.json',rows)
 # No group names in the compact reading copy. Unblinding mapping is separate.
 text=[]
 for row in rows:
  text.append(row['blind_ref'])
  for c in row['claims']:
   text.append(json.dumps({k:v for k,v in c.items() if k not in ('latest_products','source_file','extraction') and v is not None},ensure_ascii=False))
 (R/f'results/{folder}_REVIEW_READING.txt').write_text('\n'.join(text),encoding='utf-8')

def reports():
 s1=read(R/'results/stage1_scores.json');s2=read(R/'results/stage2_scores.json') if(R/'results/stage2_scores.json').exists()else[];allrows=s1+s2
 for stage,rows,groups in [('stage1',s1,('unified','ondemand')),('stage2',s2,('official','ondemand'))]:
  lines=['# '+stage+'逐次配对结果','', '质量=正确登记、当前授权、无不合法提交尝试、条件许可及未受影响依据正确、事实/理由复核通过。正确登记与质量分别列出。投入只在同质量且用量完整的配对解释；异常保留。','', '|层级/任务|版本|重复|两组正确登记|两组质量|两组变化后首个操作|两组Agent请求|两组输入/输出词元|两组耗时秒|可比较投入|','|---|---|---:|---|---|---|---|---|---|---|']
  keys=list(dict.fromkeys((r['tier'],r['task_id'],r['version'],r['id'].split('_r')[1].split('_')[0])for r in rows))
  for tier,tid,ver,rep in keys:
   aa=[next(r for r in rows if r['tier']==tier and r['task_id']==tid and r['version']==ver and r['group']==g and r['id'].split('_r')[1].split('_')[0]==rep) for g in groups];a,b=aa;comparable=all(x['quality']and x['agent_unknown_usage']==0 and not x['fact_review'].get('simulation_deviation') for x in aa)
   field=lambda k:' / '.join(str(x[k])for x in aa)
   work=lambda r:(r['post_change_first_work']or{}).get('work_type','—')+':'+str((r['post_change_first_work']or{}).get('object',(r['post_change_first_work']or{}).get('parameters','')))
   lines.append(f"|{tier}/{tid}|{ver}|{rep}|{field('final_correct')}|{field('quality')}|{work(a)} / {work(b)}|{field('agent_requests')}|{a['agent_input_tokens']}/{a['agent_output_tokens']} / {b['agent_input_tokens']}/{b['agent_output_tokens']}|{a['wall_seconds']:.2f} / {b['wall_seconds']:.2f}|{comparable}|")
  lines+=['','组顺序：'+' / '.join(groups)+'。post_change_first_work为首个执行工作，语义解析若更早发生另见完整轨迹。']
  if not rows:lines+=['','第二阶段未启动，详见GATE.json。预注册9题36条未启动，不作为失败或成功分母。']
  (R/f'results/{stage.upper()}_PAIRED_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
 save(R/'results/ACCOUNTING.json',[{'id':r['id'],'roles':r['roles'],'agent_requests':r['agent_requests'],'input_tokens':r['agent_input_tokens'],'output_tokens':r['agent_output_tokens'],'unknown_usage':r['agent_unknown_usage'],'operations':r['operations'],'queries':r['query_events'],'repeated_queries':r['repeated_queries'],'wall_seconds':r['wall_seconds']}for r in allrows])
 summary=[]
 for stage,rows in [('stage1',s1),('stage2',s2)]:
  for tier,tid in dict.fromkeys((r['tier'],r['task_id'])for r in rows):
   for g in dict.fromkeys(r['group']for r in rows):
    rr=[r for r in rows if r['tier']==tier and r['task_id']==tid and r['group']==g];summary.append({'stage':stage,'tier':tier,'task_id':tid,'group':g,'n':len(rr),'correct':sum(r['final_correct']for r in rr),'quality':sum(r['quality']for r in rr),'events':sum(r['event_received']for r in rr),'unsafe_attempts':sum(len(r['unsafe_attempts'])for r in rr),'agent_requests':sum(r['agent_requests']for r in rr),'input':sum(r['agent_input_tokens']for r in rr),'output':sum(r['agent_output_tokens']for r in rr)})
 save(R/'results/TASK_SUMMARY.json',summary)
 calls=[x for folder in ('stage1','stage2') if(R/'results'/folder/'model_calls.jsonl').exists() for x in linefile(R/'results'/folder/'model_calls.jsonl')];events=[x for folder in ('stage1','stage2') if(R/'results'/folder/'request_events.jsonl').exists() for x in linefile(R/'results'/folder/'request_events.jsonl')]
 save(R/'results/REQUEST_DIAGNOSTICS.json',{'returned_models':dict(Counter(x.get('response',{}).get('model','NO_RESPONSE')for x in calls)),'failed_requests':[{'branch':x['branch'],'role':x['role'],'attempt':x['attempt'],'diagnostic':x.get('diagnostic'),'usage':x['usage'],'seconds':x['seconds']}for x in calls if x['status']!='success'],'parse_errors':[x for x in events if x['event']=='response_parse_error'],'retry_attempts':sum(x['attempt']>1 for x in calls),'runtime_source_unchanged':all(sha(R/k)==v for k,v in read(R/'configs/freeze_stage1.json')['files'].items())})
 # Root independent analyst assigns fact_review after evidence inspection; no model judge token costs.
 save(R/'results/analysis_provenance.json',{'analysis_script_sha256':sha(__file_path()),'frozen_runtime_imports_analysis':False,'external_model_judge_requests':0,'note':'Post-run evidence display/report only; scoring definitions and progression gate were frozen before formal run.'})

def __file_path():
 from pathlib import Path
 return Path(__file__)

def trace(folder,tid,rep=1):
 groups=('unified','ondemand')if folder=='stage1'else('official','ondemand');lines=['# 完整动态多商品配对轨迹','',f'基础任务{tid}，重复{rep}。原始全部状态、请求和反馈见对应trajectory/model_calls文件；以下按真实时序列出每次调用触发、模型选择、用户原话和程序执行。']
 for group in groups:
  out=R/'results'/folder;n=next(n for n,r in read(out/'results.json').items()if r['task_id']==str(tid)and r['group']==group and r['version']=='changed'and f'_r{rep}_'in n);f=read(out/(n+'_final.json'));tr=read(out/(n+'_trajectory.json'));calls=[c for c in linefile(out/'model_calls.jsonl')if c['branch']==n];lines+=['',f'## {group}: {n}','','### 初始公开用户消息','',f['cfg']['initial_message'],'','### 逐轮记录','']
  for ix,e in enumerate(tr):
   lines.append(f"**{ix}. {e.get('module')}**")
   d=e.get('model_output')
   if d:lines+=['', '```json',json.dumps(d,ensure_ascii=False,indent=2),'```']
   if e.get('trigger_reason'):lines.append('触发原因：'+e['trigger_reason'])
   if e.get('module')=='program_execution':
    lines.append('执行：'+json.dumps(e['job'],ensure_ascii=False));lines.append('程序检查：'+json.dumps({'allowed':e['allowed'],'rejection_reason':e.get('rejection_reason'),'independent':e.get('independent_submit_check'),'result':e.get('result')},ensure_ascii=False))
    before=e['before'];after=e['after'];new=after['history'][len(before['history']):];lines.append('新增公开消息/工具：'+json.dumps(new,ensure_ascii=False));lines.append('当前目标：'+json.dumps(after['targets'])+'；授权记录状态：'+str(after['core']['records'].get('authorization',{}).get('status')))
   if e.get('module')=='public_change':
    q=e['snapshot'];before=q['before_records'];after=q['after_records'];changed=[k for k in set(before)|set(after)if before.get(k)!=after.get(k)];preserved=[k for k in before if k in after and before[k]==after[k]];lines.append('变化传播后的受影响记录：'+', '.join(changed));lines.append('原样保留记录：'+', '.join(preserved))
   if e.get('module')=='native_execution':lines.append(json.dumps({k:e.get(k)for k in ('native_tool','parameters','independent_submit_check','actual_executed','native_error','result')},ensure_ascii=False))
   if e.get('module')=='native_speech':lines+=['助手：'+str(e['text']),'用户及模拟核验：'+json.dumps(e['user_result'],ensure_ascii=False)]
   lines.append('')
  lines+=['### 实际调用账本','', '|序|角色|触发原因|输入|输出|缓存命中|用量未知|秒|','|---:|---|---|---:|---:|---:|---|---:|']
  for i,c in enumerate(calls):
   u=c['usage']or{};lines.append(f"|{i}|{c['role']}|{c['trigger_reason']}|{u.get('prompt_tokens','未知')}|{u.get('completion_tokens','未知')}|{u.get('prompt_cache_hit_tokens','未知')}|{c['usage']is None}|{c['seconds']:.2f}|")
  lines+=['','最终数据库：'+json.dumps(f['database']['orders'][f['cfg']['order_id']],ensure_ascii=False)]
 (R/f'results/DYNAMIC_PAIR_{folder}_t{tid}_r{rep}.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
 if sys.argv[1]=='excerpts':excerpts(sys.argv[2])
 elif sys.argv[1]=='reports':reports()
 elif sys.argv[1]=='trace':trace(sys.argv[2],sys.argv[3])
