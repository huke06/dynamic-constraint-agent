"""Post-run reporting. Not imported by the frozen experiment."""
from collections import Counter
from construct20 import R,read,save,sha
from score22 import score

def report():
 out=R/'results/batch01';scores=score();calls=[__import__('json').loads(s)for s in(out/'model_calls.jsonl').read_text('utf-8').splitlines()];details=[];review=[];a=['# A：同状态首步配对','','每格保留原始选择与执行核验，质量含对象、推进和理由；不按动作相同评分。','','|题/状态/重复|直接选择→执行|候选选择→执行|严格首步质量|','|---|---|---|---|'];bt=['# B：同状态合理首步续行','','同一题93的两个状态，独立基础任务数为1。强制首步后共同续行，不比较首步模型调用（首步工作由试验指定）。','','|状态/重复|先分析 登记/严格质量|先澄清 登记/严格质量|调用|输入/输出|耗时秒|可比较|','|---|---|---|---|---|---|---|'];bpairs=[]
 for r in scores:
  n=r['id'];cc=[c for c in calls if c['branch']==n];agent=[c for c in cc if c['role']!='simulator'];r['usage']={'agent_requests':len(agent),'input':sum((c['usage']or{}).get('prompt_tokens',0)for c in agent),'output':sum((c['usage']or{}).get('completion_tokens',0)for c in agent),'hit':sum((c['usage']or{}).get('prompt_cache_hit_tokens',0)for c in agent),'miss':sum((c['usage']or{}).get('prompt_cache_miss_tokens',0)for c in agent),'unknown':sum(c['usage']is None for c in agent)};details.append({'id':n,'usage':r['usage'],'calls':[{'role':c['role'],'trigger':c['trigger_reason'],'usage':c['usage'],'seconds':c['seconds'],'diagnostic':c.get('diagnostic')}for c in cc]});tr=read(out/(n+'_trace.json'));review.append({'id':n,'decision':r.get('decision'),'executed':[{k:e.get(k)for k in('module','job','allowed','rejection_reason','model_output','result')}for e in tr]})
 for tid in('91','102','93','98'):
  for state in read(R/f'configs/tasks/{tid}/case.json')['states']:
   for rep in(1,2):
    aa=[next(r for r in scores if r['part']=='A'and r['task']==tid and r['state']==state and r['rep']==rep and r['group']==g)for g in('direct','candidate')];cell=lambda r:str((r.get('decision')or{}).get('work_type'))+':'+str((r.get('decision')or{}).get('object'))+' → '+str(r['allowed']);a.append(f"|{tid}/{state}/{rep}|{cell(aa[0])}|{cell(aa[1])}|{aa[0]['strict_decision_quality']} / {aa[1]['strict_decision_quality']}|")
 for s in('conflict','feasible'):
  for rep in(1,2):
   aa=[next(r for r in scores if r['part']=='B'and r['state']==s and r['rep']==rep and r['first']==first)for first in('analyze','clarify')];x,y=aa;valid=all(r['strict_completion']and not r['usage']['unknown']for r in aa);bpairs.append({'state':s,'repeat':rep,'comparable':valid,'analyze':x,'clarify':y});bt.append(f"|{s}/{rep}|{x['correct_registered']} / {x['strict_completion']}|{y['correct_registered']} / {y['strict_completion']}|{x['usage']['agent_requests']} / {y['usage']['agent_requests']}|{x['usage']['input']}/{x['usage']['output']} / {y['usage']['input']}/{y['usage']['output']}|{x['seconds']:.2f} / {y['seconds']:.2f}|{valid}|")
 (R/'results/FIRST_DECISION_PAIRS.md').write_text('\n'.join(a),encoding='utf-8');(R/'results/CONTINUATION_PAIRS.md').write_text('\n'.join(bt),encoding='utf-8');save(out/'SCORES.json',scores);save(out/'B_PAIRS.json',bpairs);save(out/'ACCOUNTING.json',details);save(out/'REVIEW_EVIDENCE.json',review)
 f=read(R/'configs/FREEZE.json');h=read(R/'configs/HISTORY_AUDIT.json');save(R/'results/AUDIT.json',{'runtime_unchanged':all(sha(R/k)==v for k,v in f['files'].items()),'old21_unchanged':all(sha(__import__('pathlib').Path(k))==v for k,v in h['old21_frozen_sources'].items()),'returned_models':dict(Counter(c.get('response',{}).get('model','NO_RESPONSE')for c in calls)),'failed_requests':[{'id':c['branch'],'diagnostic':c.get('diagnostic'),'usage':c['usage']}for c in calls if c['status']!='success'],'analysis_script':sha(__import__('pathlib').Path(__file__))})
 print('A',[(g,sum(r['strict_decision_quality']for r in scores if r['part']=='A'and r['group']==g))for g in('direct','candidate')]);print('B',[(p['state'],p['repeat'],p['analyze']['usage'],p['clarify']['usage'],p['comparable'])for p in bpairs])

def trace(n):
 out=R/'results/batch01';x=read(out/(n+'_final.json'));tr=read(out/(n+'_trace.json'));lines=['# 完整代表性续行轨迹：'+n,'','原始请求/响应与每轮完整状态在batch01；以下逐事件列出全部工作、反馈及实际公开消息。','',x['cfg']['initial_message']]
 for ix,e in enumerate(tr):
  lines+=['',f"## {ix}. {e.get('module')}",'','```json',__import__('json').dumps({k:v for k,v in e.items()if k not in('before','after','visible_state')},ensure_ascii=False,indent=2),'```']
  if 'after'in e:
   old=len(e['before']['history']);lines+=['新增消息：','```json',__import__('json').dumps(e['after']['history'][old:],ensure_ascii=False,indent=2),'```','授权状态：'+str(e['after']['core']['records'].get('authorization',{}).get('status'))]
 lines+=['','## 最终记录','',__import__('json').dumps(x['database']['orders'][x['cfg']['order_id']],ensure_ascii=False,indent=2)];(R/f'results/TRACE_{n}.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':report()
