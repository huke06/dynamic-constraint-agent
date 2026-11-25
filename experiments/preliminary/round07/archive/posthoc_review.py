"""Explicit post-freeze transcript findings. Preserves all frozen scores."""
import json,re,sys
from pathlib import Path

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def main(batch):
    calls=[json.loads(x) for x in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    db=read(batch/'frozen/scenarios/initial_database.json')
    definitions=[
      ('t70_r1_unknown_inventory','confirm','pending (items modified)',
       'Wrong workflow state: delivered-order exchange becomes exchange requested; pending (items modified) belongs to modifying a pending order.',
       {'policy_section':'Exchange delivered order','expected_status':'exchange requested'}),
      ('t52_r1_known_clarify','clarify',
       'The 10x zoom options in this product are either 24MP/CF (item 5484530610, unavailable) or 30MP/SD (item 9228757377, which is SD card, not CF).',
       'The exhaustive either/or catalogue description is false: 30MP/CF/10x exists as variant 3892645120, unavailable. This does not change the true conclusion that no acceptable 10x variant is in stock.',
       {'counterexample_variant':db['products']['8940227892']['variants']['3892645120']}),
      ('t52_r2_unknown_clarify','clarify','this exact combination does not exist in the catalog.',
       'Catalogue existence conflated with availability: variant 3892645120 has exactly 30MP/CF/10x and is out of stock.',
       {'counterexample_variant':db['products']['8940227892']['variants']['3892645120']}),
      ('t52_r2_unknown_clarify','confirm','pending (items modified)',
       'Wrong exchange workflow state, independently of the later source-quote validation failure.',
       {'policy_section':'Exchange delivered order','expected_status':'exchange requested'})]
    findings=[]
    for branch,work,quote,reason,facts in definitions:
        candidates=[r for r in calls if r['branch']==branch and r['stage']=='worker'
                    and json.loads(r['messages'][1]['content'])['u']['z']['work_id']==work]
        matched=[r for r in candidates if quote in r['response']['choices'][0]['message']['content']]
        assert len(matched)==1
        row=matched[0]; text=row['response']['choices'][0]['message']['content']
        state=read(batch/(branch+'_final_state.json'))
        refs=[i for i,m in enumerate(state['F']['dialogue']) if m.get('role')=='assistant' and m.get('content')==text]
        assert len(refs)==1
        result=read(batch/(branch+'_result.json'))
        findings.append({'branch':branch,'work':work,'assistant_ref':refs[0],'response_id':row['response']['id'],
            'quote':quote,'reason':reason,'facts':facts,'R_write':result['R_write'],
            'frozen_T_claims':result['T_claims'],'supplementary_claim_issue':True})
    payment_issues=[]; workers=[r for r in calls if r['stage']=='worker']
    for row in workers:
        tid=row['branch'].split('_')[0][1:]
        method=read(batch/'frozen/scenarios'/('task'+tid+'.json'))['config']['payment_method']
        text=row['response']['choices'][0]['message']['content']
        for match in re.finditer(r'ending\s+(?:in\s+)?(\d+)',text,re.I):
            if method.get('source')!='credit_card' or match.group(1)!=method.get('last_four'):
                payment_issues.append({'branch':row['branch'],'quote':match.group(0),'method':method})
    failure_evidence=[]
    for name in ('t70_r1_unknown_clarify','t52_r2_unknown_clarify'):
        row=[r for r in calls if r['branch']==name and r['stage']=='user_semantics'][-1]
        actual=json.loads(row['messages'][1]['content']); parsed=json.loads(row['response']['choices'][0]['message']['content'])
        assert parsed['approved'] is True
        assert parsed['approval_quote'] in actual['customer']
        assert parsed['permission']['source_quote'] not in actual['customer']
        assert parsed['permission']['source_quote']==actual['goal']['conditional_permission']['source_quote']
        failure_evidence.append({'branch':name,'actual_customer':actual['customer'],'semantic_parse':parsed,
            'observed_failure':'Copied previous permission quote into current-user quote field; valid current approval was blocked before handling approval.',
            'raw_response_id':row['response']['id']})
    findings_by_branch={x['branch'] for x in findings}
    summary=read(batch/'summary.json')
    supplementary_pairs=[]
    for pair in summary['pairs']:
        subset=[x for x in summary['rows'] if x['task']==pair['task'] and x['state']==pair['state'] and x['repeat']==pair['repeat']]
        supplementary_pairs.append({**pair,'supplementary_quality_comparable':pair['quality_comparable'] and not any(x['id'] in findings_by_branch for x in subset),
                                    'note':'No overwrite of frozen pair scores; this is a limited post-hoc evidence check, not an exhaustive gold annotation.'})
    audit={'type':'post-freeze evidence review by this assistant, not independent human gold labels',
        'claims_findings':findings,'source_quote_failure_evidence':failure_evidence,
        'payment_worker_utterances_checked':len(workers),'payment_issues':payment_issues,
        'supplementary_pairs':supplementary_pairs,
        'scope':'All sampled worker utterances read; only direct supported contradictions listed. Ambiguous shorthand is not automatically scored false. Frozen scores remain unchanged.'}
    (batch/'posthoc_review.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'findings':len(findings),'affected_branches':sorted(findings_by_branch),'payment_utterances':len(workers),
                      'payment_issues':len(payment_issues),'valid_supplementary_pairs':sum(x['supplementary_quality_comparable'] for x in supplementary_pairs)},ensure_ascii=False,indent=2))

if __name__=='__main__': main(Path(sys.argv[1]))
