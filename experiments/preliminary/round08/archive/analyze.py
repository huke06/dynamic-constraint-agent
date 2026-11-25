"""Post-freeze read-only summaries and evidence audits. No API calls."""
import json,re,hashlib,sys
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def cost(rows):
    return {'calls':len(rows),'missing_usage':sum('usage' not in r.get('response',{}) for r in rows),
        **{k:sum(r.get('response',{}).get('usage',{}).get(k,0) for r in rows) for k in ('prompt_tokens','completion_tokens','total_tokens')},
        'seconds':sum(r.get('seconds',0) for r in rows)}

def main(batch):
    config=read(batch/'frozen/config.json'); result=read(batch/'results.json')
    calls=[json.loads(line) for line in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
    rows=[]; evidence=[]
    review_path=batch/'claim_review.json'
    reviewed=read(review_path) if review_path.exists() else {'rows':[]}
    review_by_name={r['id']:r for r in reviewed['rows']}
    for name,r in result.items():
        _,repeat,state,first=name.split('_')
        tid=name.split('_')[0][1:]
        row={'id':name,'task':tid,'repeat':int(repeat[1:]),'state':state,'first':first,
            **{k:r.get(k) for k in ('R_write','R_goal','C_hard','C_authorization_program','C_permission_state',
                'C_permission_provenance','C_authorization_provenance','T_payment_description','T_claims','T_catalog','T_status',
                'C_consent_semantic','strict_pass','error','abort_stage','start_sha256','suffix_wall_seconds_before_evaluation')}}
        row['transcript_review']=review_by_name.get(name,{'status':'pending'})
        own=[c for c in calls if c['branch']==name]
        row['costs']={k:cost([c for c in own if c['category']==k]) for k in ('agent','environment_user','external_evaluation')}
        row['suffix_started']=(batch/(name+'_start.json')).exists()
        if (batch/(name+'_trajectory.json')).exists():
            t=read(batch/(name+'_trajectory.json')); f=read(batch/(name+'_final_state.json'))
            start=read(batch/(name+'_start.json')); st=start['state']
            entries=[e for e in t if 'u' in e]
            seq=[e['u']['z']['work_id'] for e in entries]
            row.update(work_sequence=seq,work_count=len(entries),work_repeats={k:v-1 for k,v in Counter(seq).items() if v>1},
                failed_work=[e.get('error') or e['u']['z']['work_id'] for e in t if e.get('error') or not e.get('completion_satisfied',False)],
                query_count=seq.count('inventory'),write_count=len(f['P']['writes']),
                preserved_records=[k for k,v in st['H']['records'].items() if f['H']['records'].get(k)==v],
                initially_stale=[k for k,v in st['H']['records'].items() if v['status']=='stale'],
                review_calls_suffix=len(f['P']['review_audit'])-len(st['P']['review_audit']),
                review_calls_by_work=[{'work':e['u']['z']['work_id'],'calls':len(e['after']['P']['review_audit'])-len(e['before']['P']['review_audit'])} for e in entries],
                local_work_cpu_seconds=sum(e.get('local_process_cpu_seconds_including_transport',0) for e in entries))
            rule=f['g'].get('conditional_permission')
            row['rule_final']=rule
            ev={'id':name,'dialogue_and_permission_steps':[{'work':e['u']['z']['work_id'],
                'assistant_ref':e.get('assistant_ref'),'user_ref':e.get('user_ref'),'assistant':e.get('assistant'),'customer':e.get('customer'),
                'semantic_parse':e.get('semantic_parse'),'permission_before':e['before']['g']['alternative_permission'],
                'permission_after':e['after']['g']['alternative_permission'],'rule_after':e['after']['g'].get('conditional_permission'),
                'authorizations_after':len(e['after']['H']['confirmations'])} for e in entries],
                'external_evaluation':r.get('external_evaluation'),'communication_checks':r.get('communication_checks'),
                'actual_writes':f['P']['writes'],'review_audit_suffix':f['P']['review_audit'][len(st['P']['review_audit']):]}
            # Verify judge references against actual dialogue; an unsupported issue stays visible.
            ev['judge_issue_reference_checks']=[]
            for issue in (r.get('external_evaluation') or {}).get('issues',[]):
                idx=issue.get('ref'); quote=issue.get('quote')
                valid=isinstance(idx,int) and 0<=idx<len(f['F']['dialogue']) and isinstance(quote,str) and bool(quote) and quote in f['F']['dialogue'][idx].get('content','')
                ev['judge_issue_reference_checks'].append({'issue':issue,'exact_ref_quote_valid':valid})
            # Re-evaluate explicit card-ending statements from source profile, independent of saved score.
            method=read(batch/'frozen/scenarios'/('task'+tid+'.json'))['config']['payment_method']
            ev['posthoc_payment_issues']=[]
            for e in entries:
                for m in re.finditer(r'ending\s+(?:in\s+)?(\d+)',e.get('assistant',''),re.I):
                    if method.get('source')!='credit_card' or m.group(1)!=method.get('last_four'):
                        ev['posthoc_payment_issues'].append({'ref':e['assistant_ref'],'quote':m.group(0),'method':method})
            row['posthoc_payment_issues']=ev['posthoc_payment_issues']
            row['stock_before_rule_activation']=[]
            cfg=read(batch/'frozen/scenarios'/('task'+tid+'.json'))['config']
            for e in entries:
                if e['before']['g']['alternative_permission']=='unknown' and e['after']['g']['alternative_permission']!='unknown':
                    active=e['after']['g']['alternative_permission']; stock=e['after']['F']['catalog'][cfg['product_id']]['variants'][active]['available']
                    row['stock_before_rule_activation'].append(stock)
                    assert stock is True,'premature permission persisted despite saved state score'
            evidence.append(ev)
        rows.append(row)
    pairs=[]; variability=[]
    for tid in config['tasks']:
        for state in config['states']:
            for repeat in (1,2):
                a=next(x for x in rows if x['task']==tid and x['state']==state and x['repeat']==repeat and x['first']!='clarify')
                c=next(x for x in rows if x['task']==tid and x['state']==state and x['repeat']==repeat and x['first']=='clarify')
                comparable=all(x['strict_pass'] is True and not x.get('posthoc_payment_issues')
                               and x['transcript_review']['status']=='no_identified_contradiction' for x in (a,c))
                started=a['suffix_started'] and c['suffix_started']
                pairs.append({'task':tid,'state':state,'repeat':repeat,'both_started':started,
                    'starts_equal':(a.get('start_sha256')==c.get('start_sha256')) if started else None,
                    'quality_comparable':comparable,
                    'agent_tokens_evidence_minus_clarify':(a['costs']['agent']['total_tokens']-c['costs']['agent']['total_tokens']) if comparable else None,
                    'agent_calls_evidence_minus_clarify':(a['costs']['agent']['calls']-c['costs']['agent']['calls']) if comparable else None,
                    'review_calls_evidence_minus_clarify':(a.get('review_calls_suffix',0)-c.get('review_calls_suffix',0)) if comparable else None,
                    'work_evidence_minus_clarify':(a.get('work_count',0)-c.get('work_count',0)) if comparable else None})
            for first in config['first_work'][state]:
                group=[x for x in rows if x['task']==tid and x['state']==state and x['first']==first]
                sampled=[x for x in group if x['suffix_started']]
                toks=[x['costs']['agent']['total_tokens'] for x in sampled]
                variability.append({'task':tid,'state':state,'first':first,'planned_n':len(group),'started_n':len(sampled),'strict_passes':sum(x['strict_pass'] is True for x in group),
                    'tokens_in_started_repeat_order':toks,'min':min(toks) if toks else None,'max':max(toks) if toks else None,
                    'range':max(toks)-min(toks) if len(toks)>1 else None,
                    'calls':[x['costs']['agent']['calls'] for x in sampled],'works':[x.get('work_count') for x in sampled]})
    ids=[c['response']['id'] for c in calls if 'response' in c]
    oldids=set()
    for folder in HERE.parent.iterdir():
        if folder.name[:2] in ('04','05','06','07') and folder.is_dir():
            for p in folder.rglob('model_calls.jsonl'):
                oldids.update(json.loads(line).get('response',{}).get('id') for line in p.read_text(encoding='utf-8').splitlines())
    manifest=read(batch/'freeze.json')
    integrity={'protected_unchanged_now':all(sha(Path(p))==v for p,v in manifest['protected'].items()),
               'frozen_unchanged_now':all(sha(batch/'frozen'/p)==v for p,v in manifest['files'].items()),
               'responses':len(ids),'unique_response_ids':len(set(ids)),'overlap_old_ids':len(set(ids)&oldids),
               'replayed':sum('reused_from' in c for c in calls),'started_paired_starts_equal':all(p['starts_equal'] is True for p in pairs if p['both_started'])}
    save(batch/'evidence_audit.json',evidence)
    save(batch/'returned_models.json',[{'branch':c['branch'],'category':c['category'],'stage':c['stage'],**{k:c.get('response',{}).get(k) for k in ('model','system_fingerprint','id','created')}} for c in calls])
    summary={'rows':rows,'pairs':pairs,'within_cell_variability':variability,'integrity':integrity,
             'public_prefix':{name:cost([c for c in calls if c['branch']==name]) for name in sorted(set(c['branch'] for c in calls if c['branch'].endswith('_prefix')))},
             'category_totals':{k:cost([c for c in calls if c['category']==k and not c['branch'].endswith('_prefix')]) for k in ('agent','environment_user','external_evaluation')},
             'returned_models':dict(Counter(str(c.get('response',{}).get('model'))+' / '+str(c.get('response',{}).get('system_fingerprint')) for c in calls)),
             'note':'Descriptive within-task pairs only. Observed strict_pass is not exhaustive proof or a training/preference label.'}
    save(batch/'summary.json',summary)
    lines=['# 逐任务逐条结果（自动摘录）','', '|轨迹|写入|目标|硬约束|新授权|许可状态|支付表述|全部表述|语义同意|strict|工作|Agent调用|Agent输入|Agent输出|Agent合计|用户词元|评测词元|',
           '|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        v=[row['id']]+[str(row.get(k)) for k in ('R_write','R_goal','C_hard','C_authorization_program','C_permission_state','T_payment_description','T_claims','C_consent_semantic','strict_pass')]
        v+=['→'.join(row.get('work_sequence',[]))]+[str(row['costs']['agent'][k]) for k in ('calls','prompt_tokens','completion_tokens','total_tokens')]
        v += [str(row['costs'][k]['total_tokens']) for k in ('environment_user','external_evaluation')]
        lines.append('|'+ '|'.join(v)+'|')
    lines+=['','## 配对与重复波动','','```json',json.dumps({'pairs':pairs,'variability':variability},ensure_ascii=False,indent=2),'```']
    (batch/'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    paired=['# 逐任务同状态配对表','', '仅质量可比配对给出资源差；其他格为“—”，不是零差。差值均为库存依据先行减去澄清先行。','']
    for tid in config['tasks']:
        paired += ['## 任务'+tid,'','|状态|重复|两侧启动|起点一致|质量可比|工作差|review差|Agent调用差|Agent词元差|',
                   '|---|---:|---|---|---|---:|---:|---:|---:|']
        for p in [v for v in pairs if v['task']==tid]:
            vals=[p['state'],p['repeat'],p['both_started'],p['starts_equal'],p['quality_comparable']]+[
                p[k] for k in ('work_evidence_minus_clarify','review_calls_evidence_minus_clarify',
                               'agent_calls_evidence_minus_clarify','agent_tokens_evidence_minus_clarify')]
            paired.append('|'+ '|'.join('—' if v is None else str(v) for v in vals)+'|')
        paired.append('')
    (batch/'PAIRED_RESULTS.md').write_text('\n'.join(paired)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
    print(json.dumps([{k:r.get(k) for k in ('id','strict_pass','error','work_sequence','R_write','R_goal','T_claims','C_consent_semantic')} for r in rows],ensure_ascii=False,indent=2))

if __name__=='__main__': main(Path(sys.argv[1]))
