"""Round 06 coordinator. Reused algorithms are in byte-identical Round 05 modules."""
import sys
sys.dont_write_bytecode = True
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import traceback
import harness as h
from engine import Case

HERE = Path(__file__).resolve().parent
b = h.base
h.KNOWN = HERE / 'scenarios'
FILES = ['run06.py', 'harness.py', 'engine.py', 'baseline_engine.py', 'baseline_runner.py',
         'exchange_core.py', 'scoring.json', 'PROTOCOL.md', 'scenarios', 'sources']

def save(path, value):
    b.save(path, value)

def inputs():
    return (b.read(HERE/'scenarios/config.json'), b.read(HERE/'scenarios/known_fixture.json'),
            b.read(HERE/'scenarios/initial_database.json'))

def protected():
    root = next(p for p in HERE.parents if (p/'tau2-official').exists())
    exp = root/'Codex工作区/实验'
    paths = [p for folder in exp.iterdir() if folder.is_dir() and folder.name[:2] in ('01','02','03','04','05')
             for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [Path(b.read(HERE/'sources/proposal_source.json')['source']), root/'exp2layer/llm.py']
    paths += [p for p in (root/'tau2-official/src/tau2/domains/retail').rglob('*.py')]
    paths += [b.DATA/'policy.md', b.DATA/'db.json']
    return {str(p.resolve()): b.sha(p) for p in paths if p.exists()}

def differences(a, c, path=''):
    if isinstance(a, dict) and isinstance(c, dict):
        return [v for k in sorted(set(a)|set(c)) for v in differences(a.get(k),c.get(k),path+'/'+k)]
    if isinstance(a, list) and isinstance(c, list) and len(a)==len(c):
        return [v for i,(x,y) in enumerate(zip(a,c)) for v in differences(x,y,path+'/'+str(i))]
    return [] if a==c else [{'path':path,'known':a,'unknown':c}]

def make_cases(fixture, semantic):
    neighbor, intervention = h.adjacent_fixture(fixture, semantic)
    return {'known':Case(fixture,semantic),'unknown':Case(neighbor,semantic)}, neighbor, intervention

def check(output):
    config, fixture, db = inputs()
    semantic = config['canonical_semantics']
    cases, neighbor, intervention = make_cases(fixture,semantic)
    # Normalize tool JSON formatting before semantic diff; no non-observation change allowed.
    left,right = deepcopy(fixture),deepcopy(neighbor)
    for data in (left,right):
        for msg in data['shared_history']:
            if msg['role']=='tool': msg['content']=json.loads(msg['content'])
    diff=differences(left,right)
    assert len(diff)==1 and diff[0]['path'].endswith('/variants/2299424241/available')
    assert diff[0]['known'] is True and diff[0]['unknown'] is None
    report={'fixture_semantic_difference':diff,'intervention':intervention,'tests':[]}
    for state,case in cases.items():
        snap=case.snapshot(db,b.USER_POLICY)
        for work_id in config['first_work'][state]:
            candidate=next(w for w in case.candidates() if w['work_id']==work_id)
            assert candidate['ready']
            case.validate_instruction(case.instruction(candidate))
            assert deepcopy(case).snapshot(db,b.USER_POLICY)==snap
        assert case.remaining_budget==config['budget_each']
        assert not next(w for w in case.candidates() if w['work_id']=='submit')['ready']
        report['tests'].append(state+': both first instructions ready; cloned full snapshot identical; old authorization blocks submit')
    # Literal test evidence, not model/user sampling and excluded from frozen replication.
    c=deepcopy(cases['unknown'])
    quote='I accept the 80% keyboard if it is in stock.'
    c.history.append({'role':'user','content':quote})
    rule={'grant':True,'variant_id':'2299424241','size':'80%','availability_required':True,'source_quote':quote}
    assert c.remember_conditional(rule,len(c.history)-1)
    assert c.goal['alternative_permission']=='unknown'
    assert not c.confirmations and not c.writes
    tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)))
    inventory=next(w for w in c.candidates() if w['work_id']=='inventory')
    c.deterministic(c.instruction(inventory),tools)
    assert c.goal['alternative_permission']=='80%'
    assert c.conditional_permission['sat']=='满足'
    assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
    args=deepcopy(fixture['approved_prefix']['old_plan'])
    args['new_item_ids']=['2299424241' if iid==c.changed_item else nid
                          for iid,nid in zip(args['item_ids'],args['new_item_ids'])]
    prepare=next(w for w in c.candidates() if w['work_id']=='prepare')
    c.deterministic(c.instruction(prepare,{'arguments':args}),tools)
    assert c.plan and not c.confirmations
    assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
    try:
        c.core.gate(args)
    except ValueError:
        pass
    else:
        raise AssertionError('new plan must require fresh explicit authorization')
    # Negative stock and unknown stock do not trigger the rule.
    for stock in (None,False):
        negative=deepcopy(cases['unknown']); negative.history.append({'role':'user','content':quote})
        negative.remember_conditional(rule,len(negative.history)-1)
        pid=negative.core.item(negative.changed_item)['product_id']
        negative.core.products[pid]['variants']['2299424241']['available']=stock
        negative.resolve_conditional(len(negative.history)-1)
        assert negative.goal['alternative_permission']=='unknown'
    report['tests'].append('conditional permission: unknown/false cannot activate; official true activates size only; prepared new plan still fails submit gate without explicit authorization')
    old=b.ROOT/'Codex工作区/实验/05_库存证据相邻状态/results/20261121T060441772846Z/snapshot'
    mapping={'harness.py':'run.py','engine.py':'engine.py','baseline_engine.py':'baseline_engine.py',
             'baseline_runner.py':'baseline_runner.py','exchange_core.py':'exchange_core.py'}
    report['implementation_hashes']={name:{'current':b.sha(HERE/name),'round05':b.sha(old/src)} for name,src in mapping.items()}
    assert all(v['current']==v['round05'] for v in report['implementation_hashes'].values())
    report['tests'].append('all five algorithm modules byte-identical to corrected Round 05')
    report['passed']=True
    save(output,report)
    return report

def freeze():
    check(HERE/'offline_check.json')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    batch=HERE/'results'/stamp
    frozen=batch/'frozen'; frozen.mkdir(parents=True)
    for name in FILES:
        source=HERE/name
        if source.is_dir(): shutil.copytree(source,frozen/name)
        else: shutil.copy2(source,frozen/name)
    shutil.copy2(HERE/'offline_check.json',frozen/'offline_check.json')
    manifest={'frozen_at_utc':stamp,'files':{str(p.relative_to(frozen)):b.sha(p) for p in frozen.rglob('*') if p.is_file()},
              'protected':protected(),'all_calls_must_be_fresh':True,'status':'frozen_before_api'}
    save(batch/'freeze.json',manifest)
    print(str(batch),flush=True)
    return batch

def execute():
    batch=HERE.parent
    assert HERE.name=='frozen', 'Execute the frozen copy only'
    manifest=b.read(batch/'freeze.json')
    assert all(b.sha(HERE/p)==sha for p,sha in manifest['files'].items())
    assert protected()==manifest['protected']
    assert not (batch/'started.json').exists(), 'No replacement or resume samples in a frozen batch'
    save(batch/'started.json',{'utc':datetime.now(timezone.utc).isoformat(),'argv':sys.argv})
    config,fixture,db=inputs(); policy=(HERE/'scenarios/official_policy.md').read_text(encoding='utf-8')
    client=h.Client(batch,reuse_from=None)
    assert not client.archived and client.reuse_from is None
    results={}; starting={}
    try:
        for repeat in (1,2):
            prefix='prefix_r'+str(repeat)
            try:
                semantic=client.ask(prefix,'agent','initial_semantics',[
                    {'role':'system','content':b.SEMANTIC_CHANGE},
                    {'role':'user','content':h.packed({'old_plan':fixture['approved_prefix']['old_plan'],
                        'new_user_message':b.CHANGE,'order_items':db['orders'][fixture['order_id']]['items']})}],max_tokens=700)
                save(batch/(prefix+'_semantics.json'),semantic)
                assert all(semantic.get(k)==v for k,v in config['canonical_semantics'].items()), 'prefix differs from preregistered semantics'
                cases,neighbor,intervention=make_cases(fixture,semantic)
                save(batch/(prefix+'_intervention.json'),intervention)
                save(batch/(prefix+'_unknown_fixture.json'),neighbor)
                for state,c in cases.items():
                    starting[(repeat,state)]=c.snapshot(db,b.USER_POLICY)
                    save(batch/f'r{repeat}_{state}_common_start.json',starting[(repeat,state)])
            except Exception as exc:
                for job in config['job_order']:
                    if job['repeat']==repeat:
                        result={**job,'task_success':False,'all_necessary_constraints':None,'business_request_correct':False,
                                'error':'initialization failure: '+type(exc).__name__+': '+str(exc)}
                        results[job['id']]=result; save(batch/(job['id']+'_result.json'),result)
                continue
            for job in [j for j in config['job_order'] if j['repeat']==repeat]:
                name,state=job['id'],job['state']; c=cases[state]
                first=next(w for w in c.candidates() if w['work_id']==job['first'])
                try:
                    result=b.rollout(name,c,db,first,client,batch,policy)
                    assert result['start_snapshot_sha256']==b.hash_value(starting[(repeat,state)])
                    assert c.snapshot(db,b.USER_POLICY)==starting[(repeat,state)]
                except Exception as exc:
                    result={**job,'task_success':False,'all_necessary_constraints':None,'business_request_correct':False,
                            'error':'unhandled harness defect: '+type(exc).__name__+': '+str(exc)}
                    save(batch/(name+'_exception.txt'),traceback.format_exc())
                    save(batch/(name+'_result.json'),result)
                results[name]=result
                save(batch/'results.json',results)
    finally:
        client.close()
        save(batch/'results.json',results)
        save(batch/'integrity_after.json',{'protected_unchanged':protected()==manifest['protected'],
            'frozen_unchanged':all(b.sha(HERE/p)==sha for p,sha in manifest['files'].items()),
            'calls':len(client.rows),'replayed':sum('reused_from' in r for r in client.rows),
            'finished_at_utc':datetime.now(timezone.utc).isoformat()})

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=['check','freeze','execute'])
    args=parser.parse_args()
    if args.action=='check': print(json.dumps(check(HERE/'offline_check.json'),ensure_ascii=False,indent=2))
    elif args.action=='freeze': freeze()
    else: execute()
