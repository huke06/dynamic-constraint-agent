"""POST-RUN: actual-request SFT and same-input DPO, with sidecar provenance."""
from post26 import *

def decode(s):
 s=s.strip()
 if s.startswith('```'):s=s.split('\n',1)[1].rsplit('```',1)[0]
 return json.loads(s)
def write_jsonl(path,rows):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
def run():
 out=E/'samples';out.mkdir(exist_ok=True);split=read(E/'configs/PARTITIONS.json')['by_base_task'];datasets={k:[] for k in ('train','validation','test')};manifest=[];screen=[];automatic=[];seen=set()
 def add(sample_id,base,messages,source,checks):
  partition=split.get(base,'test');sig=hashed_messages(messages)
  if sig in seen:return
  seen.add(sig);datasets[partition].append({'messages':messages});manifest.append({'sample_id':sample_id,'base_task':base,'partition':partition,'line':len(datasets[partition]),'file':f'sft_{partition}.jsonl','messages_sha256':sig,'source':source,'checks':checks})
 # Existing reviewed round24 examples retain their exact model input and grouped split.
 old=R/'experiments/preliminary/round24-official-and-trajectory/results/B1/SFT_EXAMPLES.jsonl'
 for line in old.read_text('utf-8').splitlines():
  s=json.loads(line);base='exchange:'+s['base_task'];trace=Path(s['source_trace']);branch=trace.name.removesuffix('_trace.json');cs=calls(trace.parent);ix=next(i for i,c in enumerate(cs) if c.get('response',{}).get('id')==s['source_response_id']);assert cs[ix]['messages']==s['messages'][:-1]
  add('round24/'+s['id'],base,s['messages'],{'phase':'round24','request_file':str(trace.parent/'model_calls.jsonl'),'request_row':ix,'request_sha256':sha(trace.parent/'model_calls.jsonl'),'response_id':s['source_response_id'],'trace_file':str(trace),'trace_event':s['source_event'],'generation':'model_autonomous'},s['pass_reason'])
 sources=[(E/'results/A01','A01'),(E/'results/B01','B01')]
 for p in sorted((E/'versions').glob('*/results/*')):
  if (p/'SCORES.json').exists():sources.append((p,p.relative_to(E/'versions').parts[0]))
 for phase,label in sources:
  if not (phase/'SCORES.json').exists():continue
  scores={x['id']:x for x in read(phase/'SCORES.json')};allcalls=calls(phase)
  for n,score in scores.items():
   if score['group']!='framework':continue
   tr=read(phase/(n+'_trace.json'));final=read(phase/(n+'_final.json'));cfg=final['cfg'];base=cfg['business']+':'+cfg['task_id'];cog=[(j,c) for j,c in enumerate(allcalls) if c['branch']==n and c['role']=='cognitive'];ordinal=0
   if tr and tr[0]['module']=='task_execution_feedback':automatic.append({'phase':label,'id':n,'event':0,'kind':'experiment_forced_first','work':tr[0]['model_original_choice']})
   for ix,e in enumerate(tr):
    if e['module']=='program_historical_approval_archive':automatic.append({'phase':label,'id':n,'event':ix,'kind':'program_history_archive'});continue
    if e['module']!='work_selection':continue
    if e['source']!='decision_model':automatic.append({'phase':label,'id':n,'event':ix,'kind':'program_routine','work':e['model_output']});continue
    j,call=cog[ordinal];ordinal+=1;d=e['model_output'];fb=tr[ix+1];checks={'correct_end':score['correct'],'clean_trajectory':score['strict_quality'],'actual_output':decode(call['response']['choices'][0]['message']['content'])==d,'execution_allowed':fb['module']=='task_execution_feedback' and fb['allowed'],'no_program_replacement':fb.get('normalized_work',d)==d,'exact_before_input':json.loads(call['messages'][1]['content'])==e['visible_state'],'references_in_past':all(isinstance(ref,int) and 0<=ref<len(fb['before']['history']) for ref in d.get('evidence_refs',[])),'required_fields':all(k in d for k in ('work_type','object','parameters','evidence_refs','expected','reason'))}
    k=d['work_type'];progress=checks['execution_allowed']
    if k=='query':
     if cfg['business']=='return':progress=progress and d['parameters']['tool'] not in fb['before'].get('observed',{})
     else:progress=progress and d['object'] not in fb['before']['core']['products']
    elif k=='analyze':
     previous=[a for a in fb['before'].get('analysis_results',[]) if a.get('active',True)];progress=progress and not previous and bool(fb['after'].get('analysis_results'))
    checks['advances_current_work']=progress;selected=all(checks.values());sid=f'{label}/{n}/event{ix}';screen.append({'sample_id':sid,'base_task':base,'work_type':k,'selected':selected,'checks':checks,'reason_if_rejected':[k for k,v in checks.items() if not v]})
    if selected:
     messages=deepcopy_json(call['messages'])+[{'role':'assistant','content':packed(d)}]
     add(sid,base,messages,{'phase':label,'request_file':str(phase/'model_calls.jsonl'),'request_row':j,'request_sha256':sha(phase/'model_calls.jsonl'),'response_id':call['response']['id'],'trace_file':str(phase/(n+'_trace.json')),'trace_event':ix,'generation':'model_autonomous'},checks)
 for partition,rows in datasets.items():write_jsonl(out/f'sft_{partition}.jsonl',rows)
 save(out/'SFT_MANIFEST.json',manifest);save(out/'SFT_SCREENING.json',screen);save(out/'AUTOMATIC_AND_FORCED.json',automatic)
 # Predeclared branch decisions are honest candidate responses, not model choices.
 import sys
 sys.path.insert(0,str(R/'src'));sys.path.insert(0,str(R/'src/dynamic_constraint_agent_v2/compat'));from dynamic_constraint_agent_v2.decision import PROMPT
 policy=(R/'experiments/preliminary/round23-framework-loop/versions/v2/configs/official_policy.md').read_text('utf-8')
 from core26 import RETURN_DECISION
 candidates=read(E/'results/DPO_SELECTION.json');pair_scores=read(E/'results/DPO_PAIRS.json');dpo=[];dm=[]
 for s in read(E/'configs/DPO_CHECKPOINTS.json'):
  selection=next(x for x in candidates if x['checkpoint']==s['id'])
  if not selection['stable']:continue
  winner=selection['winner'];loser='clarify' if winner=='analyze' else 'analyze';n=f'B_{s["id"]}_r1_';phase=E/'results/B01';va=read(phase/(n+'analyze_visible_start.json'));vb=read(phase/(n+'clarify_visible_start.json'));assert va==vb
  da=read(phase/(n+winner+'_trace.json'))[0]['model_original_choice'];db=read(phase/(n+loser+'_trace.json'))[0]['model_original_choice'];assert da!=db
  prompt=[{'role':'system','content':(PROMPT if s['cfg']['business']=='exchange' else RETURN_DECISION)+'\n'+policy},{'role':'user','content':packed(va)}];sample={'prompt':prompt,'chosen':[{'role':'assistant','content':packed(da)}],'rejected':[{'role':'assistant','content':packed(db)}]};dpo.append(sample);base=s['cfg']['business']+':'+s['cfg']['task_id'];dm.append({'id':s['id'],'base_task':base,'partition':split.get(base,'test'),'line':len(dpo),'file':'dpo_all.jsonl','prompt_sha256':hashed_messages(prompt),'visible_snapshot':str(phase/(n+'analyze_visible_start.json')),'snapshot_sha256':sha(phase/(n+'analyze_visible_start.json')),'chosen_source':str(phase/(n+winner+'_trace.json')),'rejected_source':str(phase/(n+loser+'_trace.json')),'candidate_generation':'predeclared_executable_first_work_not_autonomous_model_response','supporting_repeats':[p for p in pair_scores if p['state']==s['id']],'comparison_rule':'hard correctness, end result, public preference, then cost','not_trained':True})
 write_jsonl(out/'dpo_all.jsonl',dpo);save(out/'DPO_MANIFEST.json',dm)
 for partition in datasets:write_jsonl(out/f'dpo_{partition}.jsonl',[s for s,m in zip(dpo,dm) if m['partition']==partition])
 save(out/'EXPORT_SUMMARY.json',{'SFT':{k:len(v) for k,v in datasets.items()},'SFT_work_types':dict(Counter(decode(read_jsonl(out/m['file'])[m['line']-1]['messages'][-1]['content'])['work_type'] for m in manifest)),'DPO':len(dpo),'automatic_or_forced_not_SFT':len(automatic),'actual_training':False})
 print(read(out/'EXPORT_SUMMARY.json'))
def deepcopy_json(x):return json.loads(json.dumps(x,ensure_ascii=False))
def hashed_messages(x):return hashlib.sha256(packed(x).encode()).hexdigest()
def read_jsonl(p):return [json.loads(l) for l in p.read_text('utf-8').splitlines() if l.strip()]
if __name__=='__main__':run()
