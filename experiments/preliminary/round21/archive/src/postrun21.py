"""Post-run reporting only; never imported by recheck21 or frozen execution."""
import json,sys
from collections import Counter
from construct20 import R,read,save,sha
from score20 import evaluate,linefile

def review_export(batch):
 out=R/'results'/batch;lines=[]
 for n in read(out/'results.json'):
  lines.append(n)
  for i,e in enumerate(read(out/(n+'_trajectory.json'))):
   if 'model_output'in e:lines.append(str(i)+' '+json.dumps(e['model_output'],ensure_ascii=False))
   if e.get('module')=='native_speech':lines.append(str(i)+' SPEECH '+e['text']+'\nUSER '+json.dumps(e['user_result'],ensure_ascii=False))
 (out/'REVIEW.txt').write_text('\n'.join(lines),encoding='utf-8')

def report(batch):
 out=R/'results'/batch;calls=linefile(out/'model_calls.jsonl');rows=[evaluate(n,out,calls)for n in read(out/'results.json')];save(out/'SCORES.json',rows);save(R/'results'/f'{batch}_scores.json',rows)
 lines=['# 第21轮逐次配对','','组顺序为官方 / 按需。仅严格质量通过、用量完整且无模拟偏离才比较投入。输入命中/未命中保留服务实际字段；没有返回则为未知。','','|题/重复|正确登记|严格质量|Agent调用|输入|输出|缓存命中/未命中|续行秒|可比|','|---|---|---|---|---|---|---|---|---|'];pairs=[];checks={};detail=[]
 for tid in ('80','49','23','107','29'):
  for rep in (1,2):
   aa=[next(z for z in rows if z['task_id']==tid and z['group']==g and f'_r{rep}_'in z['id'])for g in ('official','ondemand')];a,b=aa;valid=all(z['quality']and not z['agent_unknown_usage']and not z['fact_review'].get('simulation_deviation')for z in aa);f=lambda key:' / '.join(str(z[key])for z in aa);extra=[]
   for z in aa:
    cc=[c for c in calls if c['branch']==z['id']and c['role']!='simulator'];hit=sum((c['usage']or{}).get('prompt_cache_hit_tokens',0)for c in cc);miss=sum((c['usage']or{}).get('prompt_cache_miss_tokens',0)for c in cc);extra.append((hit,miss));detail.append({'id':z['id'],'roles':z['roles'],'agent_cache_hit':hit,'agent_cache_miss':miss,'calls':[{'role':c['role'],'trigger':c['trigger_reason'],'usage':c['usage'],'seconds':c['seconds'],'status':c['status']}for c in calls if c['branch']==z['id']]})
   checks[a['id']]=read(out/(a['id']+'_start.json'))==read(out/(b['id']+'_start.json'));pairs.append({'task_id':tid,'repeat':rep,'eligible':valid,'sides':aa,'cache':extra});lines.append(f"|{tid}/{rep}|{f('final_correct')}|{f('quality')}|{f('agent_requests')}|{f('agent_input_tokens')}|{f('agent_output_tokens')}|{extra[0]} / {extra[1]}|{a['wall_seconds']:.2f} / {b['wall_seconds']:.2f}|{valid}|")
 save(out/'PAIRS.json',pairs);save(out/'ACCOUNTING.json',detail);(out/'PAIRED_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8');(R/'results/PAIRED_RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
 freeze=read(R/'configs/recheck21_freeze.json');save(out/'AUDIT.json',{'frozen_unchanged':all(sha(R/k)==v for k,v in freeze['files'].items()),'pair_full_start_equal':checks,'offline_checks':len(read(R/'results/offline_regression.json')['checks']),'returned_models':dict(Counter(c.get('response',{}).get('model','NO_RESPONSE')for c in calls)),'failed_requests':[{'branch':c['branch'],'diagnostic':c.get('diagnostic'),'usage':c['usage']}for c in calls if c['status']!='success'],'parse_errors':[e for e in linefile(out/'request_events.jsonl')if e['event']=='response_parse_error'],'postrun_files':{p.name:sha(p)for p in(R/'src').glob('postrun21*.py')}})
 print([(z['id'],z['final_correct'],z['quality'],z['agent_requests'])for z in rows])

if __name__=='__main__':
 review_export(sys.argv[2])if sys.argv[1]=='review'else report(sys.argv[2])
