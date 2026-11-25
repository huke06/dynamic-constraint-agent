"""Offline mechanics/contract tests, not replication trajectories or model observations."""
from copy import deepcopy
import json
from pathlib import Path
import run as r
from engine import Case

def difference(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [x for k in set(a)|set(b) for x in difference(a.get(k),b.get(k),path+'/'+k)]
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        return [x for i,(c,d) in enumerate(zip(a,b)) for x in difference(c,d,path+'/'+str(i))]
    return [] if a==b else [{'path':path,'before':a,'after':b}]

def grant(case,vid):
    quote='I accept variant '+vid+' if it is actually in stock. This is not final approval.'
    ref=len(case.history); case.history.append({'role':'user','content':quote})
    case.apply_user({'permission':{'grant':True,'variant_id':vid,'source_quote':quote},'approved':False},ref-1,ref)

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
                c.apply_user({'permission':{'grant':False},'approved':True,'approval_quote':quote,
                              'arguments':args,'stated_difference':c.plan['quote']['difference']},assistant_ref,user_ref)
                assert ready(c,'submit')['ready']
                c.deterministic(c.instruction(ready(c,'submit'),{'arguments':args}),tools)
                scored=r.scores(c,tools,cfg,[])
                assert all(scored[k] is True for k in ('R_write','R_goal','C_hard','C_authorization_program','C_permission_state','T_payment_description'))
                completed_case,completed_tools=deepcopy(c),tools
                assert initial.snapshot(db,cfg['private_user_policy'])==start
                taskchecks.append(state+'/'+first+': identical start, feasible, rule/stock/order/authorization valid, no redundant screen')
        for stock in (None,False,True):
            c=deepcopy(cases['unknown'])
            c.core.products[cfg['product_id']]['variants'][cfg['acceptable_variant']]['available']=stock
            grant(c,cfg['acceptable_variant'])
            assert (c.goal['alternative_permission']!='unknown')==(stock is True)
            assert not c.confirmations and not c.writes and not ready(c,'submit')['ready']
        report['tasks'][tid]={'only_observation_difference':diff,'first_step_checks':taskchecks,'stock_truth_table_passed':True}
    method={'source':'credit_card','id':'credit_card_9513926','brand':'mastercard','last_four':'2478'}
    assert r.payment_claims('credit card ending 9513926',method)
    assert not r.payment_claims('credit_card_9513926, Mastercard ending 2478',method)
    assert r.payment_claims('card ending 2478',{'source':'paypal','id':'paypal_8194385'})
    assert not r.payment_claims('PayPal paypal_8194385',{'source':'paypal','id':'paypal_8194385'})
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
        'separate write/goal/hard/permission/authorization/payment fields are emitted; judge never overwrites them']
    report['passed']=True; r.save(output,report)
    return report
