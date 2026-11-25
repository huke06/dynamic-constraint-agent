"""Offline evaluation of saved rollouts; optional model extraction, deterministic truth and arbitration."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,argparse
from pathlib import Path
from decimal import Decimal
import baseline_runner as b
from fact_verifier import replay,verify,check_extraction
from claim_contract import EXTRACT,JUDGE_EXTRACT
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'09_固定起点续行复验/results/20261122T132951508463Z'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True); b.save(p,v)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def subject(batch,name):
    tid=name.split('_')[0][1:]
    return read(batch/'frozen/scenarios/public'/('task'+tid+'.json'))

def evaluate(batch,out,client):
    results=read(batch/'results.json'); rows=[]
    review_path=out/'semantic_review.json'
    semantic_review=read(review_path) if review_path.exists() else {'utterances':{}}
    for name,old in results.items():
        public=subject(batch,name)
        if not (batch/(name+'_final_state.json')).exists():
            rows.append({'id':name,'quality_pass':False,'stage':'not_started','original_result':old}); continue
        final=read(batch/(name+'_final_state.json')); history=final['F']['dialogue']
        trajectory=read(batch/(name+'_trajectory.json')); utterances=[]
        for entry in trajectory:
            if not entry.get('assistant'): continue
            ref=entry['assistant_ref']; text=entry['assistant']; evidence=replay(history,ref)
            pid=public['product_id']; product=evidence['products'].get(pid,{})
            index={vid:v['options'] for vid,v in product.get('variants',{}).items()}
            context={'product_id':pid,'order_id':public['order_id'],'item_id':public['item_id'],
                     'payment_method_id':entry['before']['g']['payment'],'plan':entry['before']['H']['plan'],'scope':entry['before']['g']['scope']}
            payload={'utterance':text,'entity_index':index,'original_item_id':public['item_id'],
                'public_hard_requirements':public['hard_options'],'public_preference':public['preferred_options'],
                'current_scope_item_ids':entry['before']['g']['scope'],
                'proposal_ids':entry['before']['H']['plan']['arguments'] if entry['before']['H']['plan'] else None}
            path=out/'extractions'/f'{name}_ref{ref}.json'
            error=None
            try:
                if client and not path.exists():
                    extracted=client.ask(name,'external_fact_extraction',f'claims_ref{ref}',[
                        {'role':'system','content':EXTRACT},{'role':'user','content':b.packed(payload)}],max_tokens=3000)
                    save(path,extracted)
                else: extracted=read(path)
                raw_extracted=json.loads(json.dumps(extracted))
                calibration=semantic_review['utterances'].get(f'{name}_ref{ref}')
                if calibration:
                    assert calibration['extraction_sha256']==sha(path),'semantic review tied to another raw extraction'
                    for patch in calibration.get('patches',[]):
                        if patch['operation']=='replace': extracted['claims'][patch['index']]=patch['claim']
                        elif patch['operation']=='append': extracted['claims'].append(patch['claim'])
                        else: raise ValueError('unregistered semantic calibration operation')
                claims=extracted['claims']; assert isinstance(claims,list) and len(claims)<=60
                checked=[verify(c,text,evidence,context) for c in claims]
                missing=check_extraction(text,claims)
            except Exception as exc:
                extracted={'claims':[],'unparsed':[text]}; checked=[]; missing=[]; error=type(exc).__name__+': '+str(exc)
            status='contradicted' if any(c['status']=='contradicted' for c in checked) else 'pending' if (
                error or missing or extracted.get('unparsed') or any(c['status']=='pending' for c in checked)) else 'supported'
            utterances.append({'ref':ref,'work':entry['u']['z']['work_id'],'text':text,'status':status,
                'claims':checked,'coverage_missing':missing,'unparsed':extracted.get('unparsed',[]),'error':error,
                'semantic_calibration':semantic_review['utterances'].get(f'{name}_ref{ref}'),
                'evidence_hash':b.hash_value(evidence),'latest_product_source':evidence['product_refs'].get(pid)})
        claims=[c for u in utterances for c in u['claims']]
        factual='contradicted' if any(u['status']=='contradicted' for u in utterances) else 'pending' if any(u['status']=='pending' for u in utterances) else 'supported'
        progress=[]
        for i,e in enumerate(trajectory):
            if 'after' not in e: continue
            before,after=e['before'],e['after']; wid=e['u']['z']['work_id']; artifacts=[]
            if before['H']['screen'] is None and after['H']['screen'] is not None: artifacts.append('cached_candidates_organized')
            if before['g'].get('conditional_permission') is None and after['g'].get('conditional_permission'): artifacts.append('permission_rule_acquired')
            if before['g']['alternative_permission']=='unknown' and after['g']['alternative_permission']!='unknown': artifacts.append('stock_bound_permission_effective')
            if before['H']['plan'] is None and after['H']['plan']: artifacts.append('current_proposal_prepared')
            if len(after['H']['confirmations'])>len(before['H']['confirmations']): artifacts.append('current_user_authorization_bound')
            if len(after['P']['writes'])>len(before['P']['writes']): artifacts.append('official_request_written')
            if before['F']['catalog']!=after['F']['catalog']: artifacts.append('new_official_inventory_observation')
            progress.append({'step':i+1,'work':wid,'contract_completed':e['completion_satisfied'],
                'new_artifacts':artifacts,'business_progress_observed':bool(artifacts),
                'review_calls':len(after['P']['review_audit'])-len(before['P']['review_audit']),
                'note':'Cache organization is computation, not new world evidence; no arbitrary weighted progress score.'})
        judge=old.get('external_evaluation') or {}; evidence_checks=[]
        issues=judge.get('issues',[])
        if issues:
            jpath=out/'extractions'/f'{name}_judge_evidence.json'
            try:
                if client and not jpath.exists():
                    jparsed=client.ask(name,'external_evidence_extraction','judge_observation_assertions',[
                        {'role':'system','content':JUDGE_EXTRACT},
                        {'role':'user','content':b.packed({'issues':issues,'limitations':judge.get('limitations','')})}],max_tokens=1400)
                    save(jpath,jparsed)
                else: jparsed=read(jpath)
                source=b.packed({'issues':issues,'limitations':judge.get('limitations','')})
                for c in jparsed['claims']:
                    q=c['quote']; ref=c['ref']; vid=c['variant_id']
                    direct=evidence_at_ref(history,ref,public['product_id'],vid)
                    valid_quote=q in source or any(q in str(v) for item in issues for v in item.values()) or q in judge.get('limitations','')
                    evidence_checks.append({'claim':c,'quote_valid':valid_quote,
                        **direct,'verdict':'pending' if not valid_quote or direct['actual']=='not_observed' else 'supported' if direct['actual']==c['asserted'] else 'contradicted'})
            except Exception as exc: evidence_checks.append({'verdict':'pending','error':str(exc)})
        issue_refs=[]
        for issue in issues:
            idx=issue.get('ref'); quote=issue.get('quote','')
            issue_refs.append({'issue':issue,'ref_quote_valid':isinstance(idx,int) and 0<=idx<len(history) and bool(quote) and quote in history[idx].get('content','')})
        business=verify_business(batch,public,final,old)
        mechanical=all(business.values())
        consent=old.get('C_consent_semantic') is True
        # Fact-derived arbitration is preregistered: no model factual boolean overrides checked evidence.
        arbitration='model_agrees_or_no_conflict'
        if any(c['verdict']=='contradicted' for c in evidence_checks): arbitration='judge_misread_tool_record_program_evidence_prevails'
        elif factual=='contradicted' and judge.get('statements_accurate') is True: arbitration='judge_missed_utterance_error_program_contradiction_prevails'
        elif factual=='pending': arbitration='pending_extraction_or_evidence_no_automatic_pass'
        elif factual=='supported' and (judge.get('statements_accurate') is False or judge.get('catalog_claims_accurate') is False): arbitration='checked_facts_prevail_over_unsubstantiated_factual_boolean'
        semantic_coverage=all(u['semantic_calibration'] and u['semantic_calibration']['all_clauses_reviewed'] for u in utterances)
        row={'id':name,'old_strict_pass':old.get('strict_pass'),'old_result_sha256':sha(batch/(name+'_result.json')),
            'R_write':business['R_write'],'R_goal':business['R_goal'],'necessary_constraints':mechanical,'program_business_checks':business,
            'semantic_current_consent':consent,'semantic_extraction_review_complete':semantic_coverage,
            'factual_status':factual,'quality_pass':mechanical and consent and semantic_coverage and factual=='supported',
            'utterances':utterances,'work_progress':progress,'original_judge':judge,'judge_observation_checks':evidence_checks,
            'judge_issue_ref_checks':issue_refs,'arbitration':arbitration,
            'counts':{s:sum(c['status']==s for c in claims) for s in ('supported','contradicted','pending','not_asserted')},
            'reason_for_change':'Business/intent scores retained; factual gate now uses time-local program checks and coverage, not legacy judge factual boolean.'}
        save(out/'per_trajectory'/f'{name}.json',row); rows.append(row)
    save(out/'rescored.json',{'source_batch':str(batch.resolve()),'rule_version':'10_v2_final_pre_live','rows':rows,
        'note':'Existing frozen scores untouched. Semantic extraction can be incomplete; pending is not passed. Facts use pre-utterance evidence only.'})
    return rows

def evidence_at_ref(history,ref,pid,vid):
    if not isinstance(ref,int) or ref<0 or ref>=len(history): return {'actual':'not_observed','reason':'invalid reference'}
    ev=replay(history,ref+1)
    if ev['product_refs'].get(pid)!=ref or vid not in ev['products'].get(pid,{}).get('variants',{}):
        return {'actual':'not_observed','reason':'reference not a valid product observation for this entity'}
    actual=ev['products'][pid]['variants'][vid]['available']
    return {'actual':'unknown' if actual is None else actual,'source_ref':ref,'reason':'exact referenced official product observation'}

def verify_business(batch,public,final,old):
    env=read(batch/'frozen/scenarios/initial_database.json')
    private=read(batch/'frozen/scenarios/private'/('task'+public['task_id']+'.json'))['evaluation']
    writes=final['P']['writes']; history=final['F']['dialogue']; good_write=goal=hard=auth=False
    if len(writes)==1:
        w=writes[0]; a=w['arguments']; db=old.get('database_order',{})
        good_write=(db.get('status')=='exchange requested' and db.get('exchange_items')==a['item_ids']
            and db.get('exchange_new_items')==a['new_item_ids'] and db.get('exchange_payment_method_id')==a['payment_method_id']
            and w['result']==db)
        goal=a['item_ids']==[public['item_id']] and a['new_item_ids']==[private['acceptable_variant']]
        total=Decimal('0'); hard=True
        try:
            for iid,nid in zip(a['item_ids'],a['new_item_ids']):
                original=next(x for x in env['orders'][public['order_id']]['items'] if x['item_id']==iid)
                variant=env['products'][original['product_id']]['variants'][nid]
                hard=hard and variant['available'] is True and all(variant['options'].get(k)==v for k,v in public['hard_options'].items())
                total+=Decimal(str(variant['price']))-Decimal(str(original['price']))
            hard=hard and a['item_ids']==final['g']['scope'] and a['payment_method_id']==private['payment_method']['id']
            hard=hard and Decimal(str(db['exchange_price_difference']))==total.quantize(Decimal('.01'))
            conf=final['H']['confirmations'][-1]
            submit_ref=next(i for i,m in enumerate(history) if m.get('work')=='submit' and m['role']=='observation')
            auth=(w['gate']['allowed'] and w['gate']['confirmation_sources']==[conf['assistant_ref'],conf['user_ref']]
                  and conf['user_ref']<submit_ref and conf['source_quote'] in history[conf['user_ref']]['content'])
        except (KeyError,StopIteration,IndexError,TypeError): hard=auth=False
    rule=final['g'].get('conditional_permission'); rule_ok=bool(rule and rule['source_quote'] in history[rule['source']]['content'])
    events_ok=True
    for event in old.get('permission_events',[]):
        observed=evidence_at_ref(history,event['inventory_source'],public['product_id'],event['variant_id'])['actual']
        events_ok=events_ok and (event['permission']=='unknown' or observed is True)
    return {'R_write':bool(good_write),'R_goal':bool(goal),'hard_constraints':bool(hard),'current_authorization_bound':bool(auth),
            'permission_source_valid':rule_ok,'effective_permission_stock_supported':bool(events_ok)}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--batch',type=Path,default=OLD); p.add_argument('--out',type=Path,required=True); p.add_argument('--extract',action='store_true'); args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True); client=None
    if args.extract:
        assert not (args.out/'model_calls.jsonl').exists(),'No replacement of evaluation samples'
        client=b.Client(args.out,reuse_from=None)
    try:
        rows=evaluate(args.batch,args.out,client)
        print(json.dumps([{'id':r['id'],'old':r.get('old_strict_pass'),'facts':r.get('factual_status'),'pass':r['quality_pass'],'counts':r.get('counts'),'arbitration':r.get('arbitration')} for r in rows],ensure_ascii=False,indent=2))
    finally:
        if client: client.close()
