"""Reviewable examples from actual round23 requests, never relabel forced work."""
from run24 import *
from dynamic_constraint_agent_v2.evaluation import first_quality

def make():
 source=R/'experiments/preliminary/round23-framework-loop/LEARNING_CANDIDATES.json';x=read(source);accepted=[];review=[];seen=set()
 for c in x['demonstration_candidates']:
  trace_path=Path(c['source_trace']);trace=read(trace_path);ix=int(c['id'].split('/event')[1]);e=trace[ix];d=e['model_output'];k=d['work_type'];ex=trace[ix+1];state=e['state'];final=read(Path(str(trace_path).replace('_trace.json','_final.json')))
  checks={'autonomous':e['module']=='cognitive_decision' and c['not_forced_first_work'],'final_quality':all(c['final_checks'].values()),'native_outcome':outcome(final)['correct_registered'],'execution_allowed':ex['module']=='task_execution_feedback' and ex['allowed'],'raw_not_program_corrected':ex['model_original_choice']==ex['normalized_work'],'references_valid':all(0<=r<len(ex['before']['history']) for r in d.get('evidence_refs',[])),'appropriate':all(first_quality(d,state,ex['allowed']).values())}
  calls=[json.loads(s) for s in (trace_path.parent/'model_calls.jsonl').read_text('utf-8').splitlines()]
  branch=trace_path.name.removesuffix('_trace.json');actual=[]
  for call in calls:
   if call['branch']!=branch or call['role']!='cognitive' or call['status']!='success':continue
   try:
    raw=call['response']['choices'][0]['message']['content'].strip()
    if raw.startswith('```'):raw=raw.split('\n',1)[1].rsplit('```',1)[0]
    if json.loads(raw)==d:actual.append(call)
   except Exception:pass
  checks['actual_request_found']=bool(actual)
  key=(c['base_task'],k)
  selected=all(checks.values()) and key not in seen and len(accepted)<12
  if selected:
   call=actual[0];model_input=call['messages'];actual_state=json.loads(model_input[1]['content']);checks['exact_actual_visible_input']=True
   checks['trace_state_differs_due_to_mutable_alias']=actual_state!=state
   assert 'environment_only' not in packed(model_input)
   assert all(first_quality(d,actual_state,ex['allowed']).values())
   accepted.append({'id':c['id'],'base_task':c['base_task'],'source_trace':str(trace_path),'source_trace_sha256':sha(trace_path),'source_event':ix,'source_response_id':call['response']['id'],'work_category':'信息获取（用户许可）' if k=='clarify' else '操作执行','messages':deepcopy(model_input)+[{'role':'assistant','content':packed(d)}],'decision':d,'pass_reason':checks,'subsequent_effect':{'allowed':ex['allowed'],'result':ex['result'],'final_checks':c['final_checks']},'partition':'review_pool; group entire base_task before training/test assignment','not_forced':True});seen.add(key)
  review.append({'id':c['id'],'base_task':c['base_task'],'work_type':k,'checks':checks,'selected':selected,'disposition':'selected_reviewable_example' if selected else 'eligible_not_selected_for_small_batch' if all(checks.values()) else 'diagnostic_not_positive'})
 out=E/'results/B1';out.mkdir(parents=True,exist_ok=True)
 # Metadata/future evidence stay outside the actual training messages.
 with (out/'SFT_EXAMPLES.jsonl').open('w',encoding='utf-8') as f:
  for a in accepted:f.write(json.dumps(a,ensure_ascii=False)+'\n')
 save(out/'SCREENING.json',{'source':str(source),'source_sha256':sha(source),'screened':len(review),'selected':len(accepted),'records':review,'coverage_gap':{'inventory_query':'no such autonomous work in the 52-source pool','analysis':'no autonomous analyze in full strictly accepted source continuations; forced B analyze is excluded, A analyze is checkpoint-only'},'training_performed':False,'independent_blind_review':False})
 save(out/'PARTITIONS.json',{'rule':'group all states/branches/repeats of each base_task together; no row-level random split','assignments':{tid:'review_pool; not yet assigned train/test' for tid in sorted({c['base_task'] for c in accepted})},'model_not_selected':True})
 # Export forced analysis only for diagnostic review, NOT accepted SFT.
 forced=[]
 for p in (V/'results/new01').glob('B_*_analyze_trace.json'):
  e=read(p)[0];forced.append({'source':str(p),'forced':True,'event':e,'disposition':'diagnostic_only; no autonomous model first choice'})
 save(out/'FORCED_ANALYSIS_REVIEW.json',forced)
 print({'screened':len(review),'selected':len(accepted),'coverage_gap':True})

if __name__=='__main__':make()
