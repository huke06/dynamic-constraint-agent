"""Offline mechanics/contract tests, not replication trajectories or model observations."""
from copy import deepcopy
import json
from pathlib import Path
import run as r
from engine import Case
from normalization import enums,normalize_value,normalize_semantics

def difference(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [x for k in set(a)|set(b) for x in difference(a.get(k),b.get(k),path+'/'+k)]
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        return [x for i,(c,d) in enumerate(zip(a,b)) for x in difference(c,d,path+'/'+str(i))]
    return [] if a==b else [{'path':path,'before':a,'after':b}]

def grant(case,vid):
    quote='I accept variant '+vid+' if it is actually in stock. This is not final approval.'
    ref=len(case.history); case.history.append({'role':'user','content':quote})
    case.apply_user({'permission_update':{'kind':'grant','variant_id':vid,'source_ref':ref,'source_quote':quote},
                    'authorization':{'approved':False}},ref-1,ref)

def ready(case,wid): return next(w for w in case.candidates() if w['work_id']==wid)

def check(output):
    db=r.read(r.HERE/'scenarios/initial_database.json'); report={'passed':False,'tests':[],'tasks':{}}
    for tid in ('70','52'):
        scenario=r.load(tid); cfg=scenario['config']; cases,changes=r.make_cases(scenario,cfg['canonical_semantics'])
        n,_=r.neighbor(scenario['fixture'],cfg)
        left,right=deepcopy(scenario['fixture']),deepcopy(n)
        for f in (left,right):
            for msg in f['shared_history']:
                if msg['role']=='tool': msg['content']=json.loads(msg['content'])
        diff=difference(left,right)
        assert len(diff)==1 and diff[0]['path'].endswith('/variants/'+cfg['acceptable_variant']+'/available')
        assert diff[0]['before'] is True and diff[0]['after'] is None
        taskchecks=[]
        for state,initial in cases.items():
            start=initial.snapshot(db,cfg['private_user_policy'])
            for first in ('screen','clarify') if state=='known' else ('inventory','clarify'):
                c=deepcopy(initial); tools=r.b.RetailTools(r.b.RetailDB.model_validate(deepcopy(db)))
                cand=ready(c,first); assert cand['ready']; c.validate_instruction(c.instruction(cand))
                assert c.snapshot(db,cfg['private_user_policy'])==start
                if first!='clarify': c.deterministic(c.instruction(cand),tools)
                grant(c,cfg['acceptable_variant'])
                if c.inventory_unknown():
                    assert c.goal['alternative_permission']=='unknown'
                    assert c.conditional_permission['sat']=='未知'
                    assert c.completed('permission_rule_acquired')
                    assert not any(w['work_id'] in ('clarify','screen') for w in c.candidates())
                    c.deterministic(c.instruction(ready(c,'inventory')),tools)
                assert c.goal['alternative_permission']==cfg['acceptable_variant']
                assert c.conditional_permission['sat']=='满足'
                assert not any(w['work_id']=='screen' for w in c.candidates())
                assert not ready(c,'submit')['ready']
                args={'order_id':cfg['order_id'],'item_ids':[cfg['item_id']],
                      'new_item_ids':[cfg['acceptable_variant']],'payment_method_id':c.goal['payment']}
                c.deterministic(c.instruction(ready(c,'prepare'),{'arguments':args}),tools)
                assert not any(w['work_id']=='screen' for w in c.candidates())
                assert not ready(c,'submit')['ready']
                try: c.core.gate(args)
                except ValueError: pass
                else: raise AssertionError('new plan bypassed explicit confirmation')
                assistant_ref=len(c.history); c.history.append({'role':'assistant','content':'Exact current plan: '+json.dumps(c.plan)})
                user_ref=len(c.history); quote='Yes, I explicitly approve this complete exact new plan.'
                c.history.append({'role':'user','content':quote})
                oldrule=deepcopy(c.conditional_permission)
                c.apply_user({'permission_update':{'kind':'reuse','variant_id':oldrule['variant_id'],
                    'source_ref':oldrule['source'],'source_quote':oldrule['source_quote']},
                    'authorization':{'approved':True,'source_ref':user_ref,'source_quote':quote,
                              'arguments':args,'stated_difference':c.plan['quote']['difference']}},assistant_ref,user_ref)
                assert c.conditional_permission==oldrule
                assert ready(c,'submit')['ready']
                c.deterministic(c.instruction(ready(c,'submit'),{'arguments':args}),tools)
                scored=r.scores(c,tools,cfg,[])
                assert all(scored[k] is True for k in ('R_write','R_goal','C_hard','C_authorization_program',
                    'C_permission_state','C_permission_provenance','C_authorization_provenance','T_payment_description'))
                completed_case,completed_tools=deepcopy(c),tools
                assert initial.snapshot(db,cfg['private_user_policy'])==start
                taskchecks.append(state+'/'+first+': identical start, feasible, rule/stock/order/authorization valid, no redundant screen')
        for stock in (None,False,True):
            c=deepcopy(cases['unknown'])
            c.core.products[cfg['product_id']]['variants'][cfg['acceptable_variant']]['available']=stock
            grant(c,cfg['acceptable_variant'])
            assert (c.goal['alternative_permission']!='unknown')==(stock is True)
            assert not c.confirmations and not c.writes and not ready(c,'submit')['ready']
        legal=enums(db['products'][cfg['product_id']])
        assert enums(cases['known'].core.products[cfg['product_id']])==enums(cases['unknown'].core.products[cfg['product_id']])
        raw=deepcopy(cfg['canonical_semantics'])
        if tid=='70': raw['preferred_options']['size']='medium'
        canonical,audit=normalize_semantics(raw,legal)
        assert audit['resolved'] and canonical==cfg['canonical_semantics']
        report['tasks'][tid]={'only_observation_difference':diff,'first_step_checks':taskchecks,'stock_truth_table_passed':True,
            'enum_only_prefix_equal':True,'normalization':audit}
        # Simultaneous change + yes: must rebuild and ask again, never use that yes.
        c=deepcopy(cases['known']); tools2=r.b.RetailTools(r.b.RetailDB.model_validate(deepcopy(db)))
        grant(c,cfg['acceptable_variant'])
        args={'order_id':cfg['order_id'],'item_ids':[cfg['item_id']],
              'new_item_ids':[cfg['acceptable_variant']],'payment_method_id':c.goal['payment']}
        c.deterministic(c.instruction(ready(c,'prepare'),{'arguments':args}),tools2)
        original=deepcopy(c.plan)
        ar=len(c.history); c.history.append({'role':'assistant','content':'Please approve '+json.dumps(c.plan)})
        quote='Yes, but change the selected variant or payment as requested, then ask me again.'
        ur=len(c.history); c.history.append({'role':'user','content':quote})
        change={'present':True,'source_ref':ur,'source_quote':quote,'hard_options':{},'preferred_options':{},'variant_id':cfg['acceptable_variant']}
        if tid=='52': change['payment_method_id']='credit_card_3951670'
        else: change.update(hard_options={'color':'red'},preferred_options={'size':'medium'},variant_id='8573379326')
        c.apply_user({'change':change,'authorization':{'approved':True,'source_ref':ur,'source_quote':quote,
            'arguments':args,'stated_difference':original['quote']['difference']}},ar,ur)
        assert c.plan is None and not c.confirmations and not ready(c,'submit')['ready']
        newargs={**args,'new_item_ids':[change['variant_id']],'payment_method_id':c.goal['payment']}
        c.deterministic(c.instruction(ready(c,'prepare'),{'arguments':newargs}),tools2)
        assert c.plan!=original and not ready(c,'submit')['ready']
        ar2=len(c.history); c.history.append({'role':'assistant','content':'New complete plan '+json.dumps(c.plan)})
        quote2='Yes, I approve only this new complete proposal.'
        ur2=len(c.history); c.history.append({'role':'user','content':quote2})
        c.apply_user({'authorization':{'approved':True,'source_ref':ur2,'source_quote':quote2,
            'arguments':newargs,'stated_difference':c.plan['quote']['difference']}},ar2,ur2)
        assert ready(c,'submit')['ready']
        # Old grant words cannot be relabelled as current authorization.
        invalid=deepcopy(c); invalid.confirmations=[]; invalid.core.records['authorization']['status']='stale'
        try:
            invalid.apply_user({'authorization':{'approved':True,'source_ref':invalid.conditional_permission['source'],
                'source_quote':invalid.conditional_permission['source_quote'],'arguments':newargs,
                'stated_difference':invalid.plan['quote']['difference']}},ar2,ur2)
        except ValueError: pass
        else: raise AssertionError('old permission accepted as current authorization')
        report['tasks'][tid]['changed_plan_requires_second_confirmation']=True
    method={'source':'credit_card','id':'credit_card_9513926','brand':'mastercard','last_four':'2478'}
    assert r.payment_claims('credit card ending 9513926',method)
    assert not r.payment_claims('credit_card_9513926, Mastercard ending 2478',method)
    assert r.payment_claims('card ending 2478',{'source':'paypal','id':'paypal_8194385'})
    assert not r.payment_claims('PayPal paypal_8194385',{'source':'paypal','id':'paypal_8194385'})
    assert normalize_value('size','M',['S','M','L'])['value']=='M'
    assert normalize_value('size','medium',['S','M','L'])['value']=='M'
    assert normalize_value('size','medium or large',['S','M','L'])['status']=='pending_verification'
    assert normalize_value('size','medium',['M','medium'])['status']=='pending_verification'
    # Demonstrate separate axes: a true official write does not imply truthful wording.
    completed_case.communication_checks.append({'assistant_ref':0,'payment_issues':[{'quote':'ending 9513926'}]})
    scored=r.scores(completed_case,completed_tools,cfg,[])
    assert scored['R_write'] is True and scored['T_payment_description'] is False
    wrong_goal={**deepcopy(cfg),'acceptable_variant':'not-the-accepted-variant'}
    assert r.scores(completed_case,completed_tools,wrong_goal,[])['R_goal'] is False
    assert r.scores(completed_case,completed_tools,wrong_goal,[])['R_write'] is True
    completed_case.permission_events.append({'permission':'premature','stock':None})
    scored=r.scores(completed_case,completed_tools,cfg,[])
    assert scored['R_write'] is True and scored['C_permission_state'] is False
    report['tests']=['2 tasks × 2 states × 2 feasible first-work offline continuations passed',
        'unknown/false/true stock truth table: model grant cannot bypass stock activation',
        'rule acquisition is distinct from effective permission and final authorization',
        'program menu removes repeated clarify/screen after rule/plan',
        'deterministic payment wording rejects ID-as-ending and invented PayPal card ending',
        'separate write/goal/hard/permission/authorization/payment fields are emitted; judge never overwrites them',
        'M/medium map to catalog M; ambiguous/unknown values remain pending; enum prefix reveals no stock',
        'old permission keeps its own exact source; new authorization binds current quote only',
        'simultaneous requirement/variant/payment changes invalidate old plan; new proposal needs second reply']
    import snapshots as sn
    from input_boundary import validate
    for tid in ('70','52'):
        public=r.read(r.HERE/'scenarios/public'/('task'+tid+'.json'))
        scenario=r.load(tid)
        for state in ('known','unknown'):
            frozen=sn.load_start(tid,state)
            rebuilt=sn.public_case(public,state)
            assert frozen.state()==rebuilt.state() and frozen.compact()==rebuilt.compact()
            assert frozen.goal['alternative_permission']=='unknown' and not frozen.confirmations and not frozen.plan
            target=public['inventory_intervention']['variant_id']
            observed=frozen.core.products[public['product_id']]['variants'][target]['available']
            assert observed is (True if state=='known' else None)
            if tid=='70':
                assert frozen.goal['hard_options']=={'color':'black','ventilation':'high'}
                assert frozen.goal['preferred_options']=={'size':'M'}
            for rep in (1,2):
                for first in (('screen','clarify') if state=='known' else ('inventory','clarify')):
                    branch=sn.load_start(tid,state)
                    assert branch.snapshot(db,scenario['config']['private_user_policy'])==frozen.snapshot(db,scenario['config']['private_user_policy'])
                    assert ready(branch,first)['ready'] and not ready(branch,'submit')['ready']
            validate('agent','controller',[{'role':'system','content':r.b.CONTROLLER},
                {'role':'user','content':r.packed({'state':frozen.compact(),'W':frozen.candidates(),'remaining_budget':frozen.remaining_budget})}])
        # Changing private answers/rules cannot affect public state construction.
        corrupted=deepcopy(scenario)
        corrupted['config']['acceptable_variant']='PRIVATE_ANSWER_SENTINEL'
        corrupted['config']['private_user_policy']={'goal':'PRIVATE_RULE_SENTINEL'}
        original,_=r.make_cases(scenario,public['verified_interpretation'])
        modified,_=r.make_cases(corrupted,public['verified_interpretation'])
        assert all(original[s].state()==modified[s].state() for s in ('known','unknown'))
    try:
        validate('agent','controller',[{'role':'system','content':'test'},{'role':'user','content':r.packed({'state':{'acceptable_variant':'forbidden'},'W':[],'remaining_budget':{}})}])
    except AssertionError: pass
    else: raise AssertionError('private answer leakage guard did not fire')
    report['tests']+=['4 frozen JSON starts match evidence-built states; 16 branch restores keep identical pair origins',
        'public starts do not change when private simulator/expected answer is changed',
        'agent payload boundary permits only public stage schemas and rejects restricted fields',
        'online initial semantic sampling removed; state/goal comes from checked public snapshot']
    report['passed']=True; r.save(output,report)
    return report
