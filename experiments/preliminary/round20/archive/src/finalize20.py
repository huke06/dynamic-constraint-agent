"""Post-execution audit/aggregation. Not part of the frozen Agent runtime."""
import json,hashlib
from collections import Counter
from construct20 import R,read,save,sha
from score20 import linefile,summarize
from analysis20 import reports,trace

def main():
 summarize('stage2');reports();trace('stage1','0');trace('stage2','29',2);trace('stage2','23')
 metrics={};pair_checks={};operation_audit=[]
 quality_lines=['# 逐轨迹质量分项','','正确登记含一次性写入、目标范围、同产品规格、库存、支付、Decimal整单差额和最终DB状态。无写入不据此推断约束已违反，但不算本轮要求的办理完成。严格质量还核对中间话术与理由；模拟偏离另外归因，不改写正式事实。','', '|轨迹|正确登记/必要写入约束|当前完整授权|不合法提交尝试|B显式依据保留|话术事实|理由/整体复核|模拟偏离|实际终点|','|---|---|---|---:|---|---|---|---|---|']
 for folder,groups in [('stage1',('unified','ondemand')),('stage2',('official','ondemand'))]:
  rows=read(R/f'results/{folder}_scores.json');out=R/'results'/folder;eligible=[]
  for z in rows:
   fr=z['fact_review'];b=z['unaffected_B_evidence_preserved'];btext=str(b)if b is not None else'不适用/官方无显式依据模块';speech=fr.get('speech_fact_status',fr.get('speech_factual_status','supported'));quality_lines.append(f"|{z['id']}|{'通过'if z['final_correct']else'未写入/未完成'}|{z['current_authorization']}|{len(z['unsafe_attempts'])}|{btext}|{speech}|{fr['status']}|{bool(fr.get('simulation_deviation'))}|{z['error']or'正确登记'}|")
  for a in rows:
   if a['group']!=groups[0]:continue
   n=a['id'].rsplit('_',1)[0]+'_'+groups[1];b=next(z for z in rows if z['id']==n)
   pair_checks[a['id']]=read(out/(a['id']+'_start.json'))==read(out/(n+'_start.json'))
   valid=all(z['quality']and not z['agent_unknown_usage']and not z['fact_review'].get('simulation_deviation')for z in (a,b))
   if valid:eligible.extend([a,b])
  records=[]
  for tier in dict.fromkeys(z['tier']for z in rows):
   for group in groups:
    rr=[z for z in rows if z['tier']==tier and z['group']==group];ee=[z for z in eligible if z['tier']==tier and z['group']==group]
    record={'tier':tier,'group':group,'base_tasks':len(set(z['task_id']for z in rr)),'n':len(rr),'final_correct':sum(z['final_correct']for z in rr),'quality_supported':sum(z['quality']for z in rr),'pending':sum(z['fact_review']['status']=='pending'for z in rr),'events_received':sum(z['event_received']for z in rr),'errors':[{'id':z['id'],'error':z['error']}for z in rr if z['error']],'comparable_pairs':len(ee),'comparable_requests':sum(z['agent_requests']for z in ee),'comparable_input':sum(z['agent_input_tokens']for z in ee),'comparable_output':sum(z['agent_output_tokens']for z in ee),'comparable_seconds':sum(z['wall_seconds']for z in ee),'comparable_agent_inference_seconds':sum(sum(v['request_seconds']for k,v in z['roles'].items()if k!='simulator')for z in ee),'comparable_request_mean_input':sum(z['agent_input_tokens']for z in ee)/sum(z['agent_requests']for z in ee)if ee else None};records.append(record)
   for z in rows:
    if z['tier']!=tier:continue
    final=read(out/(z['id']+'_final.json'));start=read(out/(z['id']+'_start.json'));actual_tools=[tc['function']['name']for m in final['history']for tc in m.get('tool_calls',[])];prefix_tools=[tc['function']['name']for m in start['history']for tc in m.get('tool_calls',[])];operation_audit.append({'id':z['id'],'public_prefix_tool_counts':dict(Counter(prefix_tools)),'all_history_tool_counts':dict(Counter(actual_tools)),'remaining_budget':final['remaining_budget'],'all_messages_user_assistant_tool':dict(Counter(m['role']for m in final['history']))})
  metrics[folder]=records
 save(R/'results/COMPARABLE_COSTS.json',metrics);save(R/'results/TOOL_AND_BUDGET_AUDIT.json',operation_audit)
 (R/'results/QUALITY_COMPONENTS.md').write_text('\n'.join(quality_lines),encoding='utf-8')
 lines=['# 同质量且无模拟偏离的投入比较','','只纳入双方质量通过、用量完整、无已确认模拟偏离的配对。原始失败和其投入仍在逐条表及原始账本中；这里不拿它们计算收益。','','|阶段/层级|有效配对数|组别|实际Agent请求|输入词元|输出词元|平均每请求输入|续行耗时秒|Agent请求耗时秒|','|---|---:|---|---:|---:|---:|---:|---:|---:|']
 for stage,rr in metrics.items():
  for x in rr:lines.append(f"|{stage}/{x['tier']}|{x['comparable_pairs']}|{x['group']}|{x['comparable_requests']}|{x['comparable_input']}|{x['comparable_output']}|{x['comparable_request_mean_input']:.1f}|{x['comparable_seconds']:.2f}|{x['comparable_agent_inference_seconds']:.2f}|")
 lines+=['','续行耗时不含公共起点构造，包含交互、程序执行和模拟用户；Agent请求耗时排除模拟用户。两者均非并发吞吐量指标。原生工具、自然发言与helper粒度不同，不以操作数量直接推导效率。']
 (R/'results/COMPARABLE_COSTS.md').write_text('\n'.join(lines),encoding='utf-8')
 f=read(R/'configs/freeze_stage1.json');changed=[s for s,h in f['read_only_sources'].items()if not __import__('pathlib').Path(s).exists()or sha(__import__('pathlib').Path(s))!=h];stable_changes={}
 for tid in ('0','58','95','106'):
  for rep in (1,2):
   for g in ('unified','ondemand'):
    a=read(R/f'results/stage1/t{tid}_stable_r{rep}_{g}_start.json');b=read(R/f'results/stage1/t{tid}_changed_r{rep}_{g}_start.json');a.pop('version');b.pop('version');stable_changes[f'{tid}/{rep}/{g}']=a==b
 save(R/'results/AUDIT.json',{'old_source_files_checked':len(f['read_only_sources']),'old_source_changes':changed,'runtime_frozen_files':len(f['files']),'runtime_files_unchanged':all(sha(R/s)==h for s,h in f['files'].items()),'full_pair_starts_equal':pair_checks,'all_pair_starts_equal':all(pair_checks.values()),'stable_changed_before_event_equal_except_private_version':stable_changes,'post_run_analysis_only_files':{s:sha(R/s)for s in ('src/analysis20.py','src/finalize20.py')},'formal_trajectory_count':sum(len(read(R/f'results/{stage}/results.json'))for stage in ('stage1','stage2')),'online_external_judge_api_requests':0,'orchestration_chat_analysis_tokens':'not metered as experiment Agent usage; unknown separately','training_and_preference_labels':False})
 save(R/'results/analysis_provenance.json',{'post_run_files':{s:sha(R/s)for s in ('src/analysis20.py','src/finalize20.py')},'execution_imports_these_analysis_files':False,'frozen_scoring_file':'src/score20.py','fact_dispositions':'results/fact_review.json','note':'Reports and attributions are post-run evidence interpretation. Frozen execution and scorer not modified.'})
 print(json.dumps(metrics,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
