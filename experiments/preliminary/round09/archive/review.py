"""Post-freeze evidence audit; findings supplied after reading every sampled utterance."""
import json,sys,re
from pathlib import Path
from decimal import Decimal
from input_boundary import validate
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def main(batch):
    results=read(batch/'results.json')
    calls=[json.loads(l) for l in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    definitions=read(batch/'fact_findings.json'); by_name={}; findings=[]
    for d in definitions['utterance_findings']:
        matches=[c for c in calls if c['branch']==d['id'] and c['stage']=='worker'
            and json.loads(c['messages'][1]['content'])['u']['z']['work_id']==d['work']
            and d['quote'] in c['response']['choices'][0]['message']['content']]
        assert len(matches)==1
        c=matches[0]; text=c['response']['choices'][0]['message']['content']
        f=read(batch/(d['id']+'_final_state.json'))
        refs=[i for i,m in enumerate(f['F']['dialogue']) if m.get('role')=='assistant' and m.get('content')==text]
        assert len(refs)==1
        finding={**d,'assistant_ref':refs[0],'response_id':c['response']['id']}
        findings.append(finding); by_name.setdefault(d['id'],[]).append(finding)
    for c in calls: validate(c['category'],c['stage'],c['messages'])
    assert not any(c['stage']=='initial_semantics' for c in calls)
    for issue in definitions['judge_evidence_issues']:
        t=read(batch/(issue['id']+'_trajectory.json'))
        f=read(batch/(issue['id']+'_final_state.json'))
        assert t[0]['result']['official_result']['variants']['1665571435']['available'] is True
        actual=json.loads(f['F']['dialogue'][12]['content'])
        assert actual['official_result']['variants']['1665571435']['available'] is True
        assert results[issue['id']]['T_catalog'] is False
        issue['actual_external_judge']=results[issue['id']]['external_evaluation']
        issue['tool_evidence_verified']=True
    rows=[]
    for name,result in results.items():
        if not (batch/(name+'_start.json')).exists():
            rows.append({'id':name,'status':'not_started','reason':result['error'],'utterances_checked':0}); continue
        tid=name.split('_')[0][1:]; public=read(batch/'frozen/scenarios/public'/('task'+tid+'.json'))
        state=read(batch/(name+'_final_state.json')); trajectory=read(batch/(name+'_trajectory.json'))
        profile=next(json.loads(m['content']) for m in public['fixture']['shared_history'] if m['role']=='tool'
                     and isinstance(json.loads(m['content']),dict) and 'payment_methods' in json.loads(m['content']))
        payment=profile['payment_methods'][state['g']['payment']]
        utterances=[]
        for e in trajectory:
            if not e.get('assistant'): continue
            observed=e['before']['F']['catalog'][public['product_id']]
            hard=public['hard_options']; pref=public['preferred_options']
            matching=[v for v in observed['variants'].values() if all(v['options'].get(k)==x for k,x in hard.items())]
            preferred=[v for v in matching if all(v['options'].get(k)==x for k,x in pref.items())]
            for m in re.finditer(r'ending\s+(?:in\s+)?(\d+)',e['assistant'],re.I):
                assert payment.get('source')=='credit_card' and m.group(1)==payment.get('last_four')
            utterances.append({'work':e['u']['z']['work_id'],'assistant_ref':e['assistant_ref'],'text':e['assistant'],
                'facts_at_time':{'hard_matching_variants':matching,'preferred_combination_variants':preferred,
                    'all_catalogue_variants':observed['variants'],'observed_payment':payment,
                    'order_original_item':next(i for i in e['before']['F']['order']['items'] if i['item_id']==public['item_id']),
                    'actual_write_status':result.get('database_order',{}).get('status')},
                'review_notes':'Every sampled worker utterance read against full observed catalogue, stock at that time, amounts/payment and exchange tool result. Contextual availability wording is not automatically recast as a universal existence assertion; explicit ungrounded existence/stock wording is recorded below.'})
        fs=by_name.get(name,[])
        status='contradiction' if any(v['severity']=='contradiction' for v in fs) else 'uncertain' if fs else 'no_identified_contradiction'
        rule=state['g'].get('conditional_permission'); conf=state['H']['confirmations'][-1] if state['H']['confirmations'] else None
        rows.append({'id':name,'status':status,'findings':fs,'utterances_checked':len(utterances),'utterances':utterances,
            'rule':rule,'final_confirmation':conf,
            'external_judge_evidence_issue':[v for v in definitions['judge_evidence_issues'] if v['id']==name]})
    audit={'type':'post-freeze assistant evidence review; no independent human gold annotation or frozen score overwrite',
        'rows':rows,'findings':findings,'judge_evidence_issues':definitions['judge_evidence_issues'],
        'review_count':sum(r['utterances_checked'] for r in rows),
        'quality_policy':'Frozen strict_pass plus no contrary/uncertain utterance finding required for resource ranking. A detected false-negative judge is documented without silently upgrading frozen score.',
        'input_boundary_audit':{'agent_requests_checked':sum(c['category']=='agent' for c in calls),
            'initial_semantic_requests':0,'restricted_schema_violations':0,
            'note':'Simulation/evaluation requests are separate. User-revealed preferences in actual replies are legitimate public evidence.'}}
    (batch/'claim_review.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'utterances':audit['review_count'],'contradiction_rows':sum(r['status']=='contradiction' for r in rows),
        'uncertain_rows':sum(r['status']=='uncertain' for r in rows),'input_boundary':audit['input_boundary_audit']},ensure_ascii=False,indent=2))
if __name__=='__main__': main(Path(sys.argv[1]))
