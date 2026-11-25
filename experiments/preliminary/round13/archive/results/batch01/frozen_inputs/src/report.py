"""Summaries of post-run frozen scoring. No API calls and no original score mutation."""
import json,sys,hashlib
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def calls(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()] if p.exists() else []
def cost(rows):
    return {'calls':len(rows),'missing_usage':sum('usage' not in r.get('response',{}) for r in rows),
        **{k:sum(r.get('response',{}).get('usage',{}).get(k,0) for r in rows) for k in ('prompt_tokens','completion_tokens','total_tokens')},
        'seconds':sum(r.get('seconds',0) for r in rows)}
def pairs(rows):
    output=[]
    for tid in ('70','52'):
        for state in ('known','unknown'):
            selected=[r for r in rows if r['task']==tid and r['state']==state]
            repeats=sorted(set(r['repeat'] for r in selected))
            for rep in repeats:
                group=[r for r in selected if r['repeat']==rep]
                a=next(r for r in group if r['first']!='clarify'); c=next(r for r in group if r['first']=='clarify')
                comparable=a['quality_pass'] and c['quality_pass']
                output.append({'task':tid,'state':state,'repeat':rep,'same_start':a['start_sha256']==c['start_sha256'],
                    'quality_comparable':comparable,
                    'work_evidence_minus_clarify':a['work_steps']-c['work_steps'] if comparable else None,
                    'review_evidence_minus_clarify':a['reviews']-c['reviews'] if comparable else None,
                    'tools_evidence_minus_clarify':sum(a['tools'].values())-sum(c['tools'].values()) if comparable else None,
                    'Agent_calls_evidence_minus_clarify':a['Agent']['calls']-c['Agent']['calls'] if comparable else None,
                    'Agent_tokens_evidence_minus_clarify':a['Agent']['total_tokens']-c['Agent']['total_tokens'] if comparable else None})
    return output
def make_rows(batch,scored,modelrows):
    output=[]
    for s in scored:
        name=s['id']; task,rep,state,first=name.split('_'); r=read(batch/(name+'_result.json'))
        traj=read(batch/(name+'_trajectory.json')); completed=[e for e in traj if 'after' in e]
        start=read(batch/(name+'_start.json'))
        final=read(batch/(name+'_final_state.json'))
        reviews=len(final['P']['review_audit'])-len(start['state']['P']['review_audit'])
        progress=s.get('work_progress',[])
        output.append({'id':name,'task':task[1:],'repeat':int(rep[1:]),'state':state,'first':first,
            'R_write':s['R_write'],'R_goal':s['R_goal'],'necessary_constraints':s['necessary_constraints'],
            'semantic_consent':s['semantic_current_consent'],'factual_status':s['factual_status'],'quality_pass':s['quality_pass'],
            'old_strict':s['old_strict_pass'],'work_steps':len(completed),'work_sequence':[e['u']['z']['work_id'] for e in completed],
            'reviews':reviews,'tools':{'inventory_queries':sum(e['u']['z']['work_id']=='inventory' for e in completed),'exchange_writes':len(final['P']['writes'])},
            'Agent':cost([c for c in modelrows if c['branch']==name and c['category']=='agent']),
            'work_contracts_completed':all(e['completion_satisfied'] for e in completed),
            'cache_only_preparation_steps':sum(p['new_artifacts']==['cached_candidates_organized'] for p in progress),
            'steps_with_direct_business_artifact':sum(any(a!='cached_candidates_organized' for a in p['new_artifacts']) for p in progress),
            'new_artifact_counts':dict(Counter(a for p in progress for a in p['new_artifacts'])),
            'start_sha256':r.get('start_sha256'),'abort_stage':r.get('abort_stage'),'error':r.get('error'),
            'arbitration':s['arbitration'],'claim_counts':s['counts']})
    return output
def main(batch):
    business=calls(batch/'model_calls.jsonl'); evaluation=calls(batch/'evaluation/model_calls.jsonl')
    live_scored=read(batch/'evaluation/rescored.json')['rows']; old_scored=read(HERE/'offline_v2/rescored.json')['rows']
    oldbatch=HERE.parent/'09_固定起点续行复验/results/20261122T132951508463Z'
    rows=make_rows(batch,live_scored,business); oldrows=make_rows(oldbatch,old_scored,calls(oldbatch/'model_calls.jsonl'))
    livepairs=pairs(rows); oldpairs=pairs(oldrows)
    readiness=[]
    for tid in ('70','52'):
        for state in ('known','unknown'):
            available=[p for p in oldpairs+livepairs if p['task']==tid and p['state']==state and p['quality_comparable']]
            ds=[p['Agent_tokens_evidence_minus_clarify'] for p in available]
            consistent=bool(ds) and (all(d>0 for d in ds) or all(d<0 for d in ds) or all(d==0 for d in ds))
            readiness.append({'task':tid,'state':state,'first_works':['screen','clarify'] if state=='known' else ['inventory','clarify'],
                'diagnostic_3_2_candidate_ready':True,'old09_quality_pairs':sum(p['task']==tid and p['state']==state and p['quality_comparable'] for p in oldpairs),
                'new10_quality_pairs':sum(p['task']==tid and p['state']==state and p['quality_comparable'] for p in livepairs),
                'at_least_two_quality_pairs_same_token_direction':len(available)>=2 and consistent,
                'note':'Scenario eligibility is not proof of autonomous policy benefit; old and new batches/version information remain separate.'})
    accounts={
        'live_Agent':cost([r for r in business if r['category']=='agent']),
        'live_simulated_user':cost([r for r in business if r['category']=='environment_user']),
        'live_legacy_judge':cost([r for r in business if r['category']=='external_evaluation']),
        'live_fact_extraction':cost([r for r in evaluation if r['category']=='external_fact_extraction']),
        'live_judge_evidence_extraction':cost([r for r in evaluation if r['category']=='external_evidence_extraction']),
        'offline_v1_development':cost(calls(HERE/'offline_v1/model_calls.jsonl')),
        'offline_v2_validation':cost(calls(HERE/'offline_v2/model_calls.jsonl'))}
    versionlist=[{'source':source,'branch':r['branch'],'category':r['category'],
        **{k:r.get('response',{}).get(k) for k in ('model','system_fingerprint','id','created')}}
        for source,data in [('live_business',business),('live_scoring',evaluation),('offline_v1',calls(HERE/'offline_v1/model_calls.jsonl')),('offline_v2',calls(HERE/'offline_v2/model_calls.jsonl'))] for r in data]
    save(batch/'returned_models_all.json',versionlist)
    summary={'rows':rows,'pairs':livepairs,'old09_rescored_pairs':oldpairs,'readiness_3_2':readiness,'accounts':accounts,
        'old09_counts':dict(Counter(r['factual_status'] for r in old_scored)),
        'new10_counts':dict(Counter(r['factual_status'] for r in live_scored)),
        'returned_models':dict(Counter(str(r['model'])+' / '+str(r['system_fingerprint']) for r in versionlist)),
        'fixed_start_prefix_model_calls':0,'no_preference_labels':True}
    save(batch/'summary.json',summary)
    lines=['# 第10轮逐任务配对表','', '质量不等或待核实的配对不比较投入；—不代表零差。差值均为库存依据先行减去澄清先行。','']
    for tid in ('70','52'):
        lines+=['## 任务'+tid,'','|状态|写入两侧|事实两侧|质量可比|工作差|review差|工具差|Agent调用差|Agent词元差|',
            '|---|---|---|---|---:|---:|---:|---:|---:|']
        for p in [x for x in livepairs if x['task']==tid]:
            g=[r for r in rows if r['task']==tid and r['state']==p['state']]
            values=[p['state'],' / '.join(str(r['R_write']) for r in g),' / '.join(r['factual_status'] for r in g),p['quality_comparable']]+[
                p[k] for k in ('work_evidence_minus_clarify','review_evidence_minus_clarify','tools_evidence_minus_clarify','Agent_calls_evidence_minus_clarify','Agent_tokens_evidence_minus_clarify')]
            lines.append('|'+ '|'.join('—' if v is None else str(v) for v in values)+'|')
        lines.append('')
    (batch/'PAIRED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'rows':[{k:r[k] for k in ('id','R_write','factual_status','quality_pass','work_steps','reviews','Agent','arbitration')} for r in rows],
        'pairs':livepairs,'old_pairs':oldpairs,'readiness':readiness,'accounts':accounts,'models':summary['returned_models']},ensure_ascii=False,indent=2))
if __name__=='__main__': main(Path(sys.argv[1]))
