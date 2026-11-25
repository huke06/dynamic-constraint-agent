"""Read-only post-freeze audit/report; never calls a model or changes frozen scores."""
import json
from pathlib import Path
from collections import Counter
import hashlib
import re
import sys

HERE=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def cost(rows):
    return {'calls':len(rows),'missing_usage':sum('usage' not in r.get('response',{}) for r in rows),
            **{key:sum(r.get('response',{}).get('usage',{}).get(key,0) for r in rows)
               for key in ('prompt_tokens','completion_tokens','total_tokens')},
            'api_seconds':sum(r.get('seconds',0) for r in rows)}

def main(batch):
    calls=[json.loads(line) for line in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    config=read(batch/'frozen/scenarios/config.json'); results=read(batch/'results.json')
    rows=[]
    for job in config['job_order']:
        name=job['id']; r=results[name]
        own=[c for c in calls if c['branch']==name]
        row={**job,'business_request_correct':r['business_request_correct'],'task_success':r['task_success'],
             'all_necessary_constraints':r['all_necessary_constraints'],'error':r.get('error'),
             'costs':{category:cost([c for c in own if c['category']==category])
                      for category in ('agent','environment_user','external_evaluation')}}
        if (batch/(name+'_trajectory.json')).exists():
            t=read(batch/(name+'_trajectory.json')); s=read(batch/(name+'_start.json'))['state']
            f=read(batch/(name+'_final_state.json'))
            row['work_sequence']=[e['u']['z']['work_id'] for e in t]
            row['work_count']=len(t)
            row['repeated_work']={k:v-1 for k,v in Counter(row['work_sequence']).items() if v>1}
            row['incomplete_work']=[{'work':e['u']['z']['work_id'],'error':e.get('error')} for e in t if not e.get('completion_satisfied')]
            row['official_tool_calls_suffix']={'get_product_details':row['work_sequence'].count('inventory'),
                                              'exchange_delivered_order_items':len(f['P']['writes'])}
            row['program_work_cpu_seconds']=sum(e.get('local_process_cpu_seconds_including_transport',0) for e in t)
            row['work_wall_seconds_including_io']=sum(e.get('work_wall_seconds_including_model_and_customer_io',0) for e in t)
            initial_records=s['H']['records']; final_records=f['H']['records']
            row['initial_stale']=[k for k,v in initial_records.items() if v['status']=='stale']
            row['unchanged_record_value_version_source']=[k for k,v in initial_records.items() if final_records.get(k)==v]
            row['changed_record_keys']=[k for k,v in initial_records.items() if final_records.get(k)!=v]
            row['reviewed_during_prepare']=[{'step':i+1,'items':[x['item_id'] for x in e.get('filtered_candidates',[])]}
                                          for i,e in enumerate(t) if e['u']['z']['work_id']=='prepare']
            row['authorization_evidence']=[{'step':i+1,'assistant_ref':e.get('assistant_ref'),'user_ref':e.get('user_ref'),
                                          'assistant':e.get('assistant'),'customer':e.get('customer'),
                                          'semantic_parse':e.get('semantic_parse')}
                                         for i,e in enumerate(t) if e['u']['z']['work_id'] in ('clarify','confirm')]
            row['conditional_permission_final']=f['g'].get('conditional_permission')
            row['conditional_timeline']=[{'step':i+1,'work':e['u']['z']['work_id'],
                                         'before':e['before']['g'].get('conditional_permission'),
                                         'after':e.get('after',{}).get('g',{}).get('conditional_permission'),
                                         'permission':e.get('after',{}).get('g',{}).get('alternative_permission'),
                                         'confirmations':len(e.get('after',{}).get('H',{}).get('confirmations',[]))}
                                        for i,e in enumerate(t)]
            row['permission_activated_while_stock_unknown']=[{'step':i+1,'work':e['u']['z']['work_id'],
                'customer':e.get('customer'),'semantic_parse':e.get('semantic_parse')}
                for i,e in enumerate(t)
                if e.get('after',{}).get('g',{}).get('alternative_permission')=='80%'
                and e['before']['g'].get('alternative_permission')=='unknown'
                and any(v.get('available') is None for p in e.get('after',{}).get('F',{}).get('catalog',{}).values()
                        for v in p['variants'].values())]
            row['confirmation_count']=len(f['H']['confirmations'])
            row['actual_writes']=f['P']['writes']
            row['start_snapshot_sha256']=r.get('start_snapshot_sha256')
        rows.append(row)
    pairs=[]
    for repeat in (1,2):
        for state in ('known','unknown'):
            a=next(x for x in rows if x['repeat']==repeat and x['state']==state and x['first']!='clarify')
            c=next(x for x in rows if x['repeat']==repeat and x['state']==state and x['first']=='clarify')
            valid=all(x['task_success'] is True and x['all_necessary_constraints'] is True for x in (a,c))
            d=a['costs']['agent']['total_tokens']-c['costs']['agent']['total_tokens']
            pairs.append({'repeat':repeat,'state':state,'starts_identical':a.get('start_snapshot_sha256')==c.get('start_snapshot_sha256'),
                          'comparable_quality':valid,'agent_token_inventory_minus_clarify':d,
                          'lower_agent_tokens':('tie' if d==0 else a['first'] if d<0 else 'clarify') if valid else 'indeterminate'})
    oldids=set()
    for folder in ('04_同状态候选续行','05_库存证据相邻状态'):
        for p in (HERE.parent/folder).rglob('model_calls.jsonl'):
            for line in p.read_text(encoding='utf-8').splitlines():
                oldids.add(json.loads(line).get('response',{}).get('id'))
    ids=[r['response']['id'] for r in calls if 'response' in r]
    returned=[{'branch':r['branch'],'category':r['category'],'stage':r['stage'],
               **{k:r.get('response',{}).get(k) for k in ('id','created','model','system_fingerprint')}} for r in calls]
    save(batch/'returned_models.json',returned)
    summary={'rows':rows,'paired_directions':pairs,'shared_prefix':{f'prefix_r{i}':cost([r for r in calls if r['branch']==f'prefix_r{i}']) for i in (1,2)},
             'category_totals':{k:cost([r for r in calls if r['category']==k and not r['branch'].startswith('prefix')]) for k in ('agent','environment_user','external_evaluation')},
             'freshness_audit':{'responses':len(ids),'unique_ids':len(set(ids)),'overlap_old_response_ids':len(set(ids)&oldids),
                                'replayed':sum('reused_from' in r for r in calls)},
             'returned_model_versions':dict(Counter((r.get('response',{}).get('model','MISSING')+' / '+str(r.get('response',{}).get('system_fingerprint'))) for r in calls)),
             'integrity':read(batch/'integrity_after.json')}
    save(batch/'summary.json',summary)
    # Supplementary evidence audit, kept distinct from unchanged frozen scores.
    db=read(batch/'frozen/scenarios/initial_database.json')
    payment=db['users']['yusuf_rossi_9620']['payment_methods']['credit_card_9513926']
    review=[]
    for row in rows:
        bad=[]
        for e in row.get('authorization_evidence',[]):
            for match in re.finditer(r'ending\s+(\d+)',e['assistant']):
                if match.group(1)!=payment['last_four']:
                    bad.append({'assistant_ref':e['assistant_ref'],'claim':match.group(0),'expected_last_four':payment['last_four']})
        review.append({'id':row['id'],'frozen_task_score':row['task_success'],
                       'frozen_constraint_score':row['all_necessary_constraints'],
                       'unsupported_payment_description':bad,
                       'premature_conditional_permission':row.get('permission_activated_while_stock_unknown',[]),
                       'supplementary_no_detected_issue':not bad and not row.get('permission_activated_while_stock_unknown')})
    save(batch/'posthoc_evidence_review.json',{'status':'post-freeze supplementary audit, not replacement scores or human annotation',
        'payment_ground_truth':payment,'rows':review,
        'scope':'Direct transcript/state checks only; no claim of exhaustive semantic correctness.',
        'strict_cost_preference':'All four pairs have at least one detected issue; no quality-controlled cost preference asserted.'})
    print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
    print(json.dumps([{k:r.get(k) for k in ('id','business_request_correct','task_success','all_necessary_constraints','error','work_sequence','repeated_work','incomplete_work','costs')} for r in rows],ensure_ascii=False,indent=2))

if __name__=='__main__': main(Path(sys.argv[1]))
