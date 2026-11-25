"""Post-run audits, candidate manifest and external raw-evidence copy. No API calls."""
import json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'experiments/preliminary/round23-framework-loop';V=E/'versions/v2'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 archives=[];bad=[]
 for m in(ROOT/'experiments/preliminary').glob('round*/ARCHIVE.json'):
  a=read(m)
  for f in a['copied_files']:
   if sha(Path(f['original']))!=f['sha256']or sha(ROOT/f['copy'])!=f['sha256']:bad.append(f['original'])
  archives.append({'round':a['round'],'files':len(a['copied_files'])})
 assert not bad,bad
 frozen={str(p.relative_to(ROOT)):all(sha(ROOT/k)==v for k,v in read(p)['files'].items())for p in(E/'configs/FREEZE.json',V/'configs/FREEZE.json')};assert all(frozen.values())
 pairs={};raw_accounts=[];apirows=[]
 for base,version in((E,'v1'),(V,'v2')):
  for phase in('pilot01','pilot02','pilot03','old01','new01'):
   folder=base/'results'/phase
   if not(folder/'OUTCOMES.json').exists():continue
   rows=read(folder/'OUTCOMES.json');cc=[json.loads(s)for s in(folder/'model_calls.jsonl').read_text('utf-8').splitlines()];apirows.extend(cc);raw_accounts.append({'version':version,'phase':phase,'trajectories':len(rows),'requests':len(cc),'input':sum((c['usage']or{}).get('prompt_tokens',0)for c in cc),'output':sum((c['usage']or{}).get('completion_tokens',0)for c in cc),'cache_hit':sum((c['usage']or{}).get('prompt_cache_hit_tokens',0)for c in cc),'cache_miss':sum((c['usage']or{}).get('prompt_cache_miss_tokens',0)for c in cc),'unknown_usage':sum(c['usage']is None for c in cc),'failed_requests':sum(c['status']!='success'for c in cc),'terminal_errors':[{'id':r['id'],'error':r['error']}for r in rows if r['error']]})
   if phase=='new01':
    for z in rows:
     n=z['id']
     if z['checkpoint']and z['group']=='direct':
      mate=n.replace('_direct','_candidate');a=next(c for c in cc if c['branch']==n and c['role']=='cognitive');b=next(c for c in cc if c['branch']==mate and c['role']=='cognitive');x=json.loads(a['messages'][-1]['content']);y=json.loads(b['messages'][-1]['content']);y.pop('candidate_work');pairs[version+'/'+n]={'identical_full_start':read(folder/(n+'_start.json'))==read(folder/(mate+'_start.json')),'actual_input_equal_except_candidate':x==y}
     if not z['checkpoint']and z['first']=='analyze':
      mate=n.replace('_analyze','_clarify');pairs[version+'/'+n]={'identical_full_start':read(folder/(n+'_start.json'))==read(folder/(mate+'_start.json'))}
 assert all(all(z.values())for z in pairs.values())
 save(E/'results/ALL_PHASE_ACCOUNTING.json',raw_accounts)
 save(E/'results/INTEGRITY_AUDIT.json',{'historical_rounds':archives,'historical_copied_files_total':sum(x['files']for x in archives),'original_or_copy_hash_mismatches':bad,'frozen_versions':frozen,'paired_starts_and_actual_inputs':pairs,'actual_api_requests_all_phases':len(apirows),'api_errors':sum(x['status']!='success'for x in apirows),'returned_models':dict(__import__('collections').Counter(x.get('response',{}).get('model','NO_RESPONSE')for x in apirows)),'simulator_model_calls':0,'external_judge_api_calls':0,'orchestration_chat_cost':'unknown, excluded from experiment Agent accounting'})
 # Candidate references only; no ready-to-train SFT/DPO chosen/rejected examples.
 candidates=[]
 for phase in('old01','new01'):
  folder=V/'results'/phase
  for z in read(folder/'SCORES.json'):
   if z['checkpoint']or not z['strict_quality']:continue
   tr=read(folder/(z['id']+'_trace.json'))
   for ix,event in enumerate(tr):
    if event['module']=='cognitive_decision':candidates.append({'id':z['id']+f'/event{ix}','base_task':z['task'],'source_phase':phase,'source_trace':str(folder/(z['id']+'_trace.json')),'state_field':'state (available before decision, no future outcomes)','decision_field':'model_output','final_checks':z['outcome']['checks'],'status':'demonstration_candidate_requires_independent_review_and_base_task_split','not_forced_first_work':True})
 b=read(V/'results/B_PAIRS.json');cost_candidate=[]
 for tid in('26','35'):
  pp=[x for x in b if x['task']==tid]
  if all(x['comparable']for x in pp):
   cost_candidate.append({'base_task':tid,'state':'conflict','pair_refs':[x['analyze']['id']+' vs '+x['clarify']['id']for x in pp],'calls_analyze':[x['analyze']['usage']['requests']for x in pp],'calls_clarify':[x['clarify']['usage']['requests']for x in pp],'status':'conditional_comparison_or_preference_candidate_NOT_READY_FOR_DPO','preferred_first_work':None,'cost_only_direction':'clarify uses fewer requests under this controlled acceptance script','unresolved':['Final SKUs differ: analyze branch preserves more initially requested option fields; soft preference utility not scored.','All cap/stock-feasible offers are accepted by controlled user; not general human behavior.','Single assistant semantic audit, no independent blind review.','Do not choose preference direction until business utility/cost tradeoff is defined.']})
 save(E/'LEARNING_CANDIDATES.json',{'model_training_performed':False,'ready_training_labels_generated':False,'demonstration_candidates':candidates,'comparison_candidates':cost_candidate,'pending':[{'base_task':'35','reason':'First analysis continuation has ambiguous amount comparator; only second repeat strictly comparable, no repeated preference candidate.'}],'task_partition_rule':'All states/branches/repeats of one base task must remain in one future partition; old repair cases are not unseen evaluation tasks.'})
 # Preserve source locations and add an external copy, without moving originals.
 external=Path('D:/experimentn/research-raw-archives/round23-framework-loop');manifest=[]
 for base,version in((E,'v1'),(V,'v2')):
  for phase in('pilot01','pilot02','pilot03','old01','new01'):
   folder=base/'results'/phase
   if not folder.exists():continue
   for p in folder.iterdir():
    if p.is_file()and(p.suffix=='.jsonl'or any(p.name.endswith(t)for t in('_start.json','_final.json','_trace.json','_visible_start.json'))):
     target=external/version/phase/p.name;target.parent.mkdir(parents=True,exist_ok=True)
     if target.exists():assert sha(target)==sha(p)
     else:shutil.copy2(p,target)
     manifest.append({'original':str(p),'external_copy':str(target),'sha256':sha(p),'bytes':p.stat().st_size})
 save(E/'RAW_ARCHIVES.json',{'original_locations_preserved':True,'external_root':str(external),'raw_files':manifest,'total_bytes':sum(x['bytes']for x in manifest),'restore_note':'Restore raw files to original results directories before rerunning reports. Source/configs/summary and representative Markdown traces are versioned in Git.'})
 print('historical source hashes',sum(x['files']for x in archives),'intact; candidates',len(candidates),'raw files',len(manifest))
if __name__=='__main__':main()
