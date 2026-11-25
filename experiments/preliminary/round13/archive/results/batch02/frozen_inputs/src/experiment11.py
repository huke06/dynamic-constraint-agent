import sys,json,hashlib,shutil,traceback
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import run as old
import baseline_runner as b
from snapshots import load_start
from exchange_core import Ledger,packed
from contracts08 import SEMANTICS
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
DIRECT='''Choose the next work directly from current public business state and policy. Work vocabulary:
screen=analyze cached matches; inventory=obtain current product inventory; clarify=ask permissible alternatives;
prepare=prepare exact proposal; confirm=request final authorization; submit=write currently authorized request.
Decide one current work, not an entire plan. Return JSON {"work_id":"...","target":"original item id or order id","reason":"evidence-grounded rationale","expected":"completion condition"}.
Do not output or compare a candidate list. Do not assume permission or unknown stock. Execution checks may reject your choice and provide feedback.'''
CANDIDATE=b.CONTROLLER+'\nExplain the processing object, decision evidence and expected completion in u and comparison. Generate comparisons at runtime only.'
def decide(case,client,name,group,policy,feedback):
    payload={'state':case.compact(),'remaining_budget':case.remaining_budget,'execution_feedback':feedback}
    if group=='candidate':payload['W']=case.candidates()
    result=client.ask(name,'agent','controller',[{'role':'system','content':(DIRECT if group=='direct' else CANDIDATE)+'\n'+policy},{'role':'user','content':packed(payload)}],case=case)
    if group=='candidate':
        if not result.get('comparison'):raise ValueError('missing runtime comparison')
        instruction=result['u']
    else:
        # Resolve only the selected work contract AFTER model decision; list never enters direct input.
        wid=result['work_id']; c=next((w for w in case.candidates() if w['work_id']==wid),None)
        if c is None:raise ValueError('unknown or inapplicable work '+wid)
        if result['target'] not in (c['target'],case.changed_item,case.core.order_id):raise ValueError('wrong processing object')
        instruction=case.instruction(c);result['resolved_instruction']=instruction
    case.validate_instruction(instruction)
    return result,instruction
def original_start():
    public=read(HERE/'scenarios/public/task70.json');case=load_start('70','unknown'); f=public['fixture']
    # Original public task with observed catalogue and prepared proposal, before its approval.
    case.core=Ledger(f['shared_history']);case.core.seed(f['approved_prefix'],len(f['shared_history'])-2,len(f['shared_history'])-1)
    case.history=deepcopy(f['shared_history'][:-1]);case.core.records['authorization']['status']='stale'
    for key in list(case.core.evidence):
        if key.isdigit() and int(key)>=len(case.history):del case.core.evidence[key]
    args=f['approved_prefix']['old_plan'];v=case.core.products[public['product_id']]['variants'][args['new_item_ids'][0]]
    case.goal.update(hard_options=deepcopy(v['options']),preferred_options={},alternative_permission=args['new_item_ids'][0],permission_source=None,change_source=None)
    case.goal.pop('conditional_permission',None);case.conditional_permission=None
    case.plan={'arguments':deepcopy(args),'quote':case.core.compile(args)};case.confirmations=[]
    case.transitions=[];case.semantic_events=[];case.authorization_events=[];case.event_state={'change_injected':False}
    # Stock masking is present from the first visible observation, not retroactively changed.
    vid=public['inventory_intervention']['variant_id'];pid=public['product_id']
    for i,m in enumerate(case.history):
        if m['role']=='tool':
            x=json.loads(m['content'])
            if isinstance(x,dict) and x.get('product_id')==pid:x['variants'][vid]['available']=None;m['content']=packed(x);case.core.evidence[str(i)]=deepcopy(m)
    case.core.products[pid]['variants'][vid]['available']=None
    return case
def inject(case,client,name):
    p=read(HERE/'scenarios/public/task70.json');before=case.state();ref=len(case.history)
    message=p['fixture']['change_message'];case.history.append(deepcopy(message));case.core.evidence[str(ref)]=deepcopy(message)
    parsed=client.ask(name,'agent','event_semantics',[{'role':'system','content':SEMANTICS},{'role':'user','content':packed({'goal':case.goal,'plan':case.plan,'assistant':case.history[ref-2]['content'],'customer':message['content'],'current_work':'external_change','assistant_ref':ref-2,'current_user_ref':ref})}],max_tokens=1000,case=case)
    # Full requirement replacement: dimensions explicitly demoted to preferences cease to be hard.
    if parsed.get('change',{}).get('present'):
        for k in parsed['change'].get('preferred_options',{}):case.goal['hard_options'].pop(k,None);case.core.requirements[case.changed_item].pop(k,None)
    case.apply_user(parsed,ref-2,ref);case.event_state={'change_injected':True,'source':ref}
    assert case.plan is None and not case.confirmations
    return {'trigger':'old current proposal explicitly authorized, before any submission','before':before,'user_message':message,'source':ref,'semantic_parse':parsed,'after':case.state()}
def offline():
    import check_facts
    check_facts.OLD=ROOT.parent/'09_固定起点续行复验/results/20261122T132951508463Z'
    check=check_facts.check
    save(ROOT/'configs/fact_selfcheck.json',check())
    checks=[]
    for tid in ('70','52'):
        for state in ('known','unknown'):
            a=load_start(tid,state);c=load_start(tid,state);assert a.state()==c.state();checks.append(tid+' '+state+' identical')
    c=original_start();assert not c.confirmations and c.plan
    p=read(HERE/'scenarios/public/task70.json');pid=p['product_id'];vid=p['inventory_intervention']['variant_id']
    assert c.core.products[pid]['variants'][vid]['available'] is None
    db=read(HERE/'scenarios/initial_database.json');assert db['products'][pid]['variants'][vid]['available'] is True
    # Exercise event invalidation without a model, including old authorized fingerprint.
    args=c.plan['arguments'];oldfp=c.plan['quote']['fingerprint'];c.core.confirm(args,c.plan['quote']['difference'],len(c.history)-1,len(c.history)-2)
    c.reset_permission(len(c.history));assert c.plan is None and not c.confirmations
    assert c.core.records['authorization']['status']=='stale'
    save(ROOT/'configs/offline.json',{'passed':True,'checks':checks,'dynamic_catalogue_exists':True,'dynamic_underlying_stock':True,'dynamic_visible_stock':None,'old_authorization_invalidated':True,'original_fingerprint':oldfp,'boundary':'Original public task/dialogue and prepared original proposal supplied; original identity/catalogue search is not resampled.'})
def execute():
    batch=ROOT/'results/batch01';batch.mkdir(exist_ok=True);assert not (batch/'started.json').exists()
    manifest=read(ROOT/'configs/freeze.json');assert all(sha(ROOT/p)==v for p,v in manifest['files'].items())
    save(batch/'started.json',{'utc':datetime.now(timezone.utc).isoformat()})
    client=b.Client(batch); b.WORKER=old.WORKER;b.USER_PROMPT=old.USER_PROMPT;b.USER_SEMANTICS=SEMANTICS
    policy=(HERE/'scenarios/official_policy.md').read_text('utf-8');db=read(HERE/'scenarios/initial_database.json');results={}
    for tid,state in [('70','known'),('70','unknown'),('52','known'),('52','unknown'),('70','dynamic')]:
      for group in ('direct','candidate'):
        name=f't{tid}_r1_{state}_{group}';case=original_start() if state=='dynamic' else load_start(tid,state)
        cfg=old.load(tid)['config'];tools=b.RetailTools(b.RetailDB.model_validate(deepcopy(db)));entries=[];feedback=[];error=None
        save(batch/(name+'_start.json'),case.snapshot(db,cfg['private_user_policy']))
        try:
          for turn in range(12):
            if case.writes or case.remaining_budget['work_steps']<=0:break
            before=case.state()
            try:decision,u=decide(case,client,name,group,policy,feedback)
            except Exception as ex:
                feedback=[{'rejected':str(ex)}];entries.append({'turn':turn,'before':before,'rejection':str(ex),'state_after_rejection':case.state()});continue
            b.USER_POLICY=cfg['private_user_policy']
            if state=='dynamic' and not case.event_state['change_injected']:
                b.USER_POLICY='Before a later explicit change, approve the complete original helmet proposal: blue medium high ventilation, original Visa, difference $22.55. Do not change requirements yet. Explicitly approve exactly the original proposal when asked.'
            e=old.work(case,u,client,name,tools,policy);e.update(turn=turn,decision=decision);entries.append(e);feedback=[{'work':u['z']['work_id'],'result':e.get('result'),'completed':e['completion_satisfied']}]
            if state=='dynamic' and not case.event_state['change_injected'] and case.confirmations and not case.writes:
                event=inject(case,client,name);entries.append({'event':event});save(batch/(name+'_event.json'),event);feedback.append({'user_change':event['user_message']})
            save(batch/(name+'_trajectory.json'),entries)
          if not case.writes:error='budget/decision-attempt limit reached without write'
        except Exception as ex:error=type(ex).__name__+': '+str(ex);entries.append({'error':error,'traceback':traceback.format_exc()})
        completed=[e for e in entries if 'u' in e];r=old.scores(case,tools,cfg,completed)
        r.update(error=error,branch=name,event_triggered=case.event_state.get('change_injected'),start_sha256=b.hash_value(read(batch/(name+'_start.json'))))
        r['external_evaluation']=None;r['C_consent_semantic']=None;r['strict_pass']=False
        if case.writes:
          try:
            j=client.ask(name,'external_evaluation','judge',[{'role':'system','content':old.JUDGE+'\n'+policy},{'role':'user','content':packed({'goal':cfg['private_user_policy'],'dialogue':[{'index':i,**m} for i,m in enumerate(case.history)],'actual_writes':case.writes,'observed_payment_method':old.methods(case)})}],max_tokens=1400)
            r['external_evaluation']=j;r['C_consent_semantic']=j['consent_valid']
          except Exception as ex:r['evaluation_error']=str(ex)
        save(batch/(name+'_trajectory.json'),entries);save(batch/(name+'_final_state.json'),case.state());save(batch/(name+'_result.json'),r);results[name]=r;save(batch/'results.json',results)
        print(name,'write',r['R_write'],'error',error,flush=True)
    client.close()
    save(batch/'integrity.json',{'frozen_unchanged':all(sha(ROOT/p)==v for p,v in manifest['files'].items())})
if __name__=='__main__':
    if sys.argv[1]=='offline':offline()
    elif sys.argv[1]=='freeze':
        offline();files={str(p.relative_to(ROOT)):sha(p) for folder in ('src','configs') for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='freeze.json' and '__pycache__' not in p.parts}
        save(ROOT/'configs/freeze.json',{'utc':datetime.now(timezone.utc).isoformat(),'files':files})
    else:execute()
