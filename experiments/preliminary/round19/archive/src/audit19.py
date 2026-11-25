"""Post-run integrity audit; independent of scores and never calls a model."""
from pathlib import Path
from construct18 import R,read,save,sha
from score19 import linefile
def audit():
 f=read(R/'configs/freeze.json');checks={'frozen_unchanged':all(sha(R/k)==v for k,v in f['files'].items()),'old01_18_proposal_benchmark_unchanged':all(sha(Path(k))==v for k,v in f['read_only_sources'].items()),'offline_passed':read(R/'configs/offline.json')['passed'],'freeze_before_main':f['utc']<read(R/'results/main/started.json')['utc'],'32_formal_saved':len(read(R/'results/main/results.json'))==32,'4_context_saved':len(read(R/'results/context/results.json'))==4}
 calls=linefile(R/'results/main/model_calls.jsonl');checks['official_no_project_tools']=all(not({'prepare','confirm','submit','evidence','prepare_exchange_proposal'} & {t['function']['name'] for t in a['tools']}) for a in calls if a['category']=='agent' and a['branch'].endswith('_official'));checks['official_native_standard_message_roles']=all(all(m['role']in ('system','user','assistant','tool') for m in a['messages']) for a in calls if a['category']=='agent' and a['branch'].endswith('_official'));checks['framework_has_compact_fields']=all('current_goal'in __import__('json').loads(a['messages'][1]['content']) and 'interaction_history'not in __import__('json').loads(a['messages'][1]['content']) for a in calls if a['category']=='agent' and a['branch'].endswith('_framework'))
 checks['shared_native_schemas']=len({__import__('json').dumps(a['tools'],sort_keys=True) for a in calls if a['category']=='agent'})==1
 for folder in ('main','context'):
  cc=linefile(R/f'results/{folder}/model_calls.jsonl');ee=linefile(R/f'results/{folder}/request_events.jsonl');checks[folder+'_request_pairs']=sum(e['event']=='request_started' for e in ee)==len(cc)==sum(e['event']=='request_finished' for e in ee)
 for tid in ('27','75'):
  a=read(R/f'results/context/cost_t{tid}_original_start.json');b=read(R/f'results/context/cost_t{tid}_compact_start.json');checks[tid+'_context_starts_identical']=a==b
 for tid in ('6','27','75','77'):
  for rep in (1,2):
   starts=[read(R/f'results/main/t{tid}_{ver}_r{rep}_{g}_start.json')['history'] for ver in ('stable','changed') for g in ('official','framework')];checks[tid+'_'+str(rep)+'_public_starts_identical']=all(s==starts[0] for s in starts)
 save(R/'results/AUDIT.json',{'passed':all(checks.values()),'checks':checks,'protected_files':len(f['read_only_sources'])});assert all(checks.values()),checks;print(checks)
if __name__=='__main__':audit()
