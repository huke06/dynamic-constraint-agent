"""Post-run integrity and provenance audit. Never calls a model or modifies frozen files."""
import ast,hashlib,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
BATCH=ROOT/'results/20261123T001740331845Z'
OLD=ROOT.parent/'09_固定起点续行复验'
OLDBATCH=OLD/'results/20261122T132951508463Z'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calls(p):return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
    frozen=BATCH/'frozen'; f=read(BATCH/'freeze.json'); checks={}
    checks['frozen_files_unchanged']=all(sha(frozen/p)==v for p,v in f['files'].items())
    checks['protected_files_unchanged']=all(sha(Path(p))==v for p,v in f['protected'].items())
    modules=['baseline_engine.py','baseline_runner.py','exchange_core.py','adjacent_reference.py',
             'legacy_engine.py','engine.py','normalization.py','contracts08.py','input_boundary.py','snapshots.py','checks.py']
    checks['business_modules_identical_09']={p:sha(frozen/p)==sha(OLD/p) for p in modules}
    def defs(path):
        t=ast.parse(path.read_text(encoding='utf-8'))
        return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    a,b=defs(frozen/'run.py'),defs(OLD/'run.py')
    checks['work_scores_rollout_identical_09']={k:a[k]==b[k] for k in ('work','scores','rollout')}
    checks['snapshots_identical_09']=all(sha(p)==sha(OLD/'snapshots'/p.relative_to(frozen/'snapshots')) for p in (frozen/'snapshots').rglob('*') if p.is_file())
    results=read(BATCH/'results.json'); rows=read(BATCH/'evaluation/rescored.json')['rows']
    checks['eight_results_and_writes']=len(results)==8 and len(rows)==8 and all(r['R_write'] for r in rows)
    checks['all_goal_constraints_and_authorization']=all(all(r['program_business_checks'].values()) and r['semantic_current_consent'] for r in rows)
    pairs=[]
    for tid in ('70','52'):
        for st,first in [('known','screen'),('unknown','inventory')]:
            names=[f't{tid}_r1_{st}_{x}' for x in (first,'clarify')]
            starts=[read(BATCH/(n+'_start.json')) for n in names]
            pairs.append({'task':tid,'state':st,'complete_start_equal':starts[0]==starts[1],
                          'historical_start_equal':all(sha(BATCH/(n+'_start.json'))==sha(OLDBATCH/(n+'_start.json')) for n in names)})
    checks['pairs']=pairs
    archive=ROOT/'offline_v2/original_09_scores'
    checks['original09_score_archive_exact']=all(sha(p)==sha(OLDBATCH/p.name) for p in archive.iterdir() if p.is_file())
    live=calls(BATCH/'model_calls.jsonl'); ev=calls(BATCH/'evaluation/model_calls.jsonl')
    oldids={r['response']['id'] for r in calls(OLDBATCH/'model_calls.jsonl')}
    offline=[r for sub in ('offline_v1','offline_v2') for r in calls(ROOT/sub/'model_calls.jsonl')]
    liveids=[r['response']['id'] for r in live+ev]
    checks['fresh_unique_live_ids']=len(set(liveids))==len(liveids) and not(set(liveids)&(oldids|{r['response']['id'] for r in offline}))
    checks['no_replayed_calls']=all('reused_from' not in r for r in live+ev)
    checks['no_online_initial_semantics']=all('initial' not in r['stage'] for r in live)
    checks['no_evaluation_feedback_to_agent']=all('10_v2' not in json.dumps(r['messages']) and 'semantic_review' not in json.dumps(r['messages']) for r in live if r['category']=='agent')
    checks['freeze_before_new_business_api']=f['utc']<read(BATCH/'started.json')['utc']
    auth=[]
    for name in results:
        final=read(BATCH/(name+'_final_state.json')); w=final['P']['writes'][0]
        auth.append({'id':name,'order_id':w['arguments']['order_id'],'new_item_ids':w['arguments']['new_item_ids'],
                     'payment_method_id':w['arguments']['payment_method_id'],'price_difference':w['result']['exchange_price_difference'],
                     'status':w['result']['status'],'confirmation_sources':w['gate']['confirmation_sources'],'allowed':w['gate']['allowed']})
    save(BATCH/'ACTUAL_WRITES.json',auth)
    # This is a provenance check, separate from frozen extractor's stock-value checks.
    name='t70_r1_unknown_inventory'; h=read(BATCH/(name+'_final_state.json'))['F']['dialogue']; env=json.loads(h[12]['content'])
    provenance={'id':name,'ref':12,'observation_role':h[12]['role'],'work':h[12]['work'],
        'official_tool':env.get('official_tool'),'arguments':env['arguments'],
        'official_result_available':env['official_result']['variants']['1665571435']['available'],
        'derived_summary_is_separate_field':'derived_available_options' in env,
        'judge_original':results[name]['external_evaluation'],
        'decision':'Official get_product_details result exists inside executor envelope; dismissing entire ref12 as self-generated is unsupported. Ref8 unknown does not supersede ref12 true.',
        'score_change':'No rewrite to frozen scoring or original judge. Ref16 stock assertion already supported by frozen replay; whole trajectory stays pending for unrelated absent-SKU stock wording.',
        'limitation':'Frozen judge extractor models available values only, not provenance assertions; this supplementary program audit is reported separately.'}
    save(BATCH/'JUDGE_PROVENANCE_AUDIT.json',provenance)
    checks['ref12_contains_official_result']=env.get('official_tool')=='get_product_details' and env['official_result']['variants']['1665571435']['available'] is True
    # Re-run deterministic scoring only, measuring CPU/elapsed after module import. No extraction redraw.
    sys.path.insert(0,str(frozen))
    import score_facts
    before=sha(BATCH/'evaluation/rescored.json'); wall=time.perf_counter(); cpu=time.process_time()
    score_facts.evaluate(BATCH,BATCH/'evaluation',None)
    save(BATCH/'program_timing.json',{'batch':'new10','cpu_seconds':time.process_time()-cpu,'elapsed_seconds':time.perf_counter()-wall,
        'model_calls':0,'scope':'deterministic replay, comparisons and JSON IO; excludes imports, network/model extraction and unmetered assistant semantic review'})
    checks['deterministic_rescore_identical']=before==sha(BATCH/'evaluation/rescored.json')
    def ok(x):
        if isinstance(x,bool):return x
        if isinstance(x,dict):return all(ok(v) for v in x.values())
        if isinstance(x,list):return all(ok(v) for v in x)
        return True
    passed=ok(checks)
    save(BATCH/'DELIVERY_AUDIT.json',{'passed':passed,'protected_count':len(f['protected']),'frozen_count':len(f['files']),'checks':checks})
    print(json.dumps({'passed':passed,'checks':checks},ensure_ascii=False,indent=2))
    assert passed
if __name__=='__main__':main()
