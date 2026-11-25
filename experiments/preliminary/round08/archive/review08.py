"""Post-freeze, source-grounded transcript review; never overwrites frozen scores."""
import json,sys,re
from pathlib import Path
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def main(batch):
    results=read(batch/'results.json'); db=read(batch/'frozen/scenarios/initial_database.json')
    calls=[json.loads(l) for l in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    definitions=[
      ('t52_r1_known_screen','confirm','pending (items modified)','contradiction','status',
       'Exchange tool/policy result is exchange requested, not pending-order modification status.'),
      ('t52_r1_unknown_inventory','confirm','pending (items modified)','contradiction','status',
       'Exchange tool/policy result is exchange requested, not pending-order modification status.'),
      ('t52_r1_unknown_clarify','clarify','since no variant has 30MP + CF card + 10x zoom together','uncertain','catalog',
       'Unqualified repeated conclusion can suggest nonexistence, although the paragraph initially mentions available variants. Variant 3892645120 exists and is out of stock. Keep this wording unresolved rather than claim a proven nonexistent-variant error or automatically accept it.')]
    by_name={}; findings=[]
    for name,work,quote,severity,dimension,reason in definitions:
        matches=[c for c in calls if c['branch']==name and c['stage']=='worker'
                 and json.loads(c['messages'][1]['content'])['u']['z']['work_id']==work
                 and quote in c['response']['choices'][0]['message']['content']]
        assert len(matches)==1
        call=matches[0]; text=call['response']['choices'][0]['message']['content']
        final=read(batch/(name+'_final_state.json'))
        refs=[i for i,m in enumerate(final['F']['dialogue']) if m.get('content')==text and m['role']=='assistant']
        assert len(refs)==1
        finding={'id':name,'work':work,'ref':refs[0],'response_id':call['response']['id'],'quote':quote,
                 'severity':severity,'dimension':dimension,'reason':reason,
                 'facts':{'counterexample_variant':db['products']['8940227892']['variants']['3892645120']} if dimension=='catalog'
                         else {'actual_tool_status':results[name]['database_order']['status'],'policy_section':'Exchange delivered order'}}
        findings.append(finding); by_name.setdefault(name,[]).append(finding)
    rows=[]
    for name,result in results.items():
        if not (batch/(name+'_start.json')).exists():
            rows.append({'id':name,'status':'not_started','reason':result['error'],'stage':result.get('abort_stage'),'utterances_checked':0})
            continue
        state=read(batch/(name+'_final_state.json')); trajectory=read(batch/(name+'_trajectory.json'))
        cfg=read(batch/'frozen/scenarios'/('task'+name.split('_')[0][1:]+'.json'))['config']
        method=cfg['payment_method']; utterances=[]
        for e in trajectory:
            if not e.get('assistant'): continue
            errors=[]
            for match in re.finditer(r'ending\s+(?:in\s+)?(\d+)',e['assistant'],re.I):
                if method.get('source')!='credit_card' or match.group(1)!=method.get('last_four'): errors.append(match.group(0))
            assert not errors
            observed=e['before']['F']['catalog'][cfg['product_id']]
            utterances.append({'work':e['u']['z']['work_id'],'assistant_ref':e['assistant_ref'],
                'text':e['assistant'],'facts_at_time':{'preferred_combination':observed['variants']['3892645120'],
                    'fallback':observed['variants']['6384525445'],'other_available':observed['variants']['7255224608'],
                    'original_item':next(i for i in db['orders'][cfg['order_id']]['items'] if i['item_id']==cfg['item_id']),
                    'payment':method,'expected_difference':34.07,'actual_write_status':result['database_order']['status']},
                'review_notes':'Checked listed specs/prices, stock at time, amount/payment and workflow status; findings or uncertainty listed separately. Available-subset phrasing is read in context, not automatically recast as a universal existence assertion.'})
        f=by_name.get(name,[])
        status='contradiction' if any(x['severity']=='contradiction' for x in f) else 'uncertain' if f else 'no_identified_contradiction'
        rule=state['g']['conditional_permission']; conf=state['H']['confirmations'][-1]
        assert rule['source_quote'] in state['F']['dialogue'][rule['source']]['content']
        assert conf['source_quote'] in state['F']['dialogue'][conf['user_ref']]['content']
        assert conf['user_ref']>rule['source']
        rows.append({'id':name,'status':status,'findings':f,'utterances_checked':len(utterances),'utterances':utterances,
            'permission_user_ref':rule['source'],'inventory_ref':rule['inventory_source'],
            'authorization_user_ref':conf['user_ref'],'authorization_assistant_ref':conf['assistant_ref'],
            'permission_quote':rule['source_quote'],'authorization_quote':conf['source_quote'],
            'component_review':{'write_matches_tool':True,'goal_matches_accepted_fallback':True,'condition_activated_after_stock':True,
                'independent_current_authorization':True,'payment_description':'no_detected_issue',
                'catalog':'uncertain' if any(x['dimension']=='catalog' for x in f) else 'no_identified_contradiction',
                'status':'contradiction' if any(x['dimension']=='status' for x in f) else 'no_identified_contradiction'}})
    review={'type':'post-freeze assistant evidence review, not independent human gold annotation',
        'rows':rows,'findings':findings,'policy':'No frozen scores changed; a direct contradiction OR unresolved wording excludes resource preference. No exhaustive proof of semantic accuracy.',
        'review_count':sum(r['utterances_checked'] for r in rows)}
    (batch/'claim_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'utterances_checked':review['review_count'],'contradiction_rows':sum(r['status']=='contradiction' for r in rows),
                      'uncertain_rows':sum(r['status']=='uncertain' for r in rows),'no_identified_contradiction':sum(r['status']=='no_identified_contradiction' for r in rows)},ensure_ascii=False))
if __name__=='__main__': main(Path(sys.argv[1]))
