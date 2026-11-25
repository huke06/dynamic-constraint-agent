"""Construct once from checked public evidence; restore JSON runtime without LLM parsing."""
from pathlib import Path
import json,hashlib,time
from copy import deepcopy
from engine import Case
from exchange_core import Ledger,packed
HERE=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(v): return hashlib.sha256(packed(v).encode()).hexdigest()
def neighbor(public):
    fixture=deepcopy(public['fixture']); change=public['inventory_intervention']
    msg=fixture['shared_history'][change['history_index']]
    product=json.loads(msg['content']); assert product['product_id']==change['product_id']
    assert product['variants'][change['variant_id']]['available'] is True
    product['variants'][change['variant_id']]['available']=None
    msg['content']=json.dumps(product,ensure_ascii=False)
    return fixture

def public_case(public,state):
    fixture=public['fixture'] if state=='known' else neighbor(public)
    return Case(fixture,public['verified_interpretation'])

def build():
    wall=time.perf_counter(); cpu=time.process_time(); manifest={}
    for tid in ('70','52'):
        public=read(HERE/'scenarios/public'/('task'+tid+'.json'))
        for state in ('known','unknown'):
            case=public_case(public,state)
            runtime={'case_fields':{k:deepcopy(v) for k,v in case.__dict__.items() if k!='core'},
                     'ledger_fields':deepcopy(case.core.__dict__)}
            document={'task_id':tid,'state_name':state,'state':case.state(),'agent_initial_view':case.compact(),
                'candidate_work':case.candidates(),'remaining_budget':case.remaining_budget,'runtime':runtime,
                'construction_input':'scenarios/public/task'+tid+'.json','private_data_used':False}
            path=HERE/'snapshots/public'/f't{tid}_{state}.json'; save(path,document)
            # Per-record evidence is read from observed history, not future results.
            evidence={'task_id':tid,'state_name':state,'user_claims':public['user_claim_evidence'],
                'observations':[{'ref':i,'role':m['role'],'tool_call_id':m.get('tool_call_id'),'observation':json.loads(m['content'])}
                    for i,m in enumerate(case.history) if m['role']=='tool'],
                'records':case.core.snapshot(),'dependency_graph':case.state()['D'],
                'not_granted':{'alternative_permission':case.goal['alternative_permission'],'permission_source':None,
                               'rule':None,'current_transaction_authorization':False},
                'catalogue_keeps_unpermitted_variants':True,'snapshot_hash':digest(document)}
            save(HERE/'snapshots/evidence'/f't{tid}_{state}.json',evidence)
            manifest[f't{tid}_{state}']={'snapshot_sha256':digest(document),'agent_view_sha256':digest(case.compact()),
                                        'state_sha256':digest(case.state()),'budget':case.remaining_budget}
    save(HERE/'snapshots/manifest.json',manifest)
    save(HERE/'snapshots/preparation.json',{'source':'checked public dialogue/observed tools only',
        'online_initial_semantic_calls':0,'model_tokens':0,'wall_seconds':time.perf_counter()-wall,
        'local_cpu_seconds':time.process_time()-cpu,'note':'Offline preparation, not rollout work; manual review effort is not converted into fabricated token/time cost.'})
    return manifest

def load_start(tid,state):
    doc=read(HERE/'snapshots/public'/f't{tid}_{state}.json'); runtime=doc['runtime']
    case=Case.__new__(Case); case.__dict__.update(deepcopy(runtime['case_fields']))
    case.core=Ledger.__new__(Ledger); case.core.__dict__.update(deepcopy(runtime['ledger_fields']))
    assert case.state()==doc['state'] and case.compact()==doc['agent_initial_view']
    assert case.candidates()==doc['candidate_work'] and case.remaining_budget==doc['remaining_budget']
    assert digest(doc)==read(HERE/'snapshots/manifest.json')[f't{tid}_{state}']['snapshot_sha256']
    return case

if __name__=='__main__': print(json.dumps(build(),ensure_ascii=False,indent=2))
