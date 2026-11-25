"""Generic variant permission; same adapter for every new task and branch."""
from copy import deepcopy
from adjacent_reference import Case as AdjacentCase
from baseline_engine import SAT, UNMET, UNKNOWN, NA


class Case(AdjacentCase):
    def __init__(self, fixture, semantics):
        super().__init__(fixture, semantics)
        self.permission_events=[]
        self.process_checks=[]
        self.communication_checks=[]
        self.user_state={'turns':0,'allowed_alternative':False,'confirmed':False}
        self.goal['permission_contract']='A named variant grant is effective only after observed available=true; never transaction authorization.'

    def remember_conditional(self, parsed, user_ref):
        if parsed.get('grant') is not True:
            return False
        pid=self.core.item(self.changed_item)['product_id']
        vid=parsed['variant_id']; variant=self.core.products[pid]['variants'].get(vid)
        if not variant or not all(variant['options'].get(k)==v for k,v in self.goal['hard_options'].items()):
            raise ValueError('permission entity absent or violates hard requirements')
        quote=parsed['source_quote']
        if not isinstance(quote,str) or not quote or quote not in self.history[user_ref]['content']:
            raise ValueError('permission requires exact user source quote')
        self.conditional_permission={'item_id':self.changed_item,'variant_id':vid,'options':deepcopy(variant['options']),
            'condition':{'product_id':pid,'variant_id':vid,'field':'available','value':True},
            'source':user_ref,'source_quote':quote,'sat':UNKNOWN}
        self.goal['conditional_permission']=deepcopy(self.conditional_permission)
        self.core.put('conditional_rule:'+self.changed_item,deepcopy(self.conditional_permission),sources=[user_ref])
        # Enforced regardless of the model's conditional/unconditional description.
        self.resolve_conditional(self.core.product_refs[pid])
        return True

    def resolve_conditional(self, inventory_ref):
        rule=getattr(self,'conditional_permission',None)
        if not rule: return
        pid,vid=rule['condition']['product_id'],rule['variant_id']
        stock=self.core.products[pid]['variants'][vid].get('available')
        rule['sat']=SAT if stock is True else UNMET if stock is False else UNKNOWN
        rule['inventory_source']=inventory_ref
        self.goal['conditional_permission']=deepcopy(rule)
        if stock is True:
            self.core.put('conditional_trigger:'+self.changed_item,{'variant_id':vid,'satisfied':True},
                ['conditional_rule:'+self.changed_item,'catalog:'+pid],[rule['source'],inventory_ref])
            self.goal['alternative_permission']=vid
            self.goal['permission_source']=rule['source']
            self.stage_change(rule['options'],rule['source'])
            self.core.records['requirement:'+self.changed_item]['depends_on']=['conditional_trigger:'+self.changed_item]
        else:
            self.goal['alternative_permission']='unknown'
        if hasattr(self,'permission_events'):
            self.permission_events.append({'variant_id':vid,'stock':stock,'permission':self.goal['alternative_permission'],
                                           'user_source':rule['source'],'inventory_source':inventory_ref})

    def apply_user(self, parsed, assistant_ref, user_ref):
        self.remember_conditional(parsed.get('permission',{}),user_ref)
        if parsed.get('approved'):
            quote=parsed.get('approval_quote')
            if not self.plan or not quote or quote not in self.history[user_ref]['content']:
                raise ValueError('approval needs a current proposal and exact actual user quote')
            result=self.core.confirm(parsed['arguments'],parsed['stated_difference'],user_ref,assistant_ref)
            if result['fingerprint']!=self.plan['quote']['fingerprint']:
                raise ValueError('approval refers to another plan')
            self.confirmations.append({'result':result,'assistant_ref':assistant_ref,'user_ref':user_ref})

    def candidates(self):
        result=super().candidates()
        rule=getattr(self,'conditional_permission',None)
        permitted=self.goal['alternative_permission']!='unknown'
        # Screening is optional computation, not a mandatory ritual after permission/plan.
        result=[w for w in result if not (w['work_id']=='screen' and (rule or permitted or self.plan))
                and not (w['work_id']=='clarify' and rule)]
        for w in result:
            if w['work_id']=='clarify':
                w['completion_test']='permission_rule_acquired'
                w['expected_output']='specific alternative permission, optionally conditional on availability, or a genuine remaining gap'
        return result

    def completed(self,test):
        if test=='permission_rule_acquired': return bool(getattr(self,'conditional_permission',None))
        return super().completed(test)

    def deterministic(self,instruction,tools):
        if instruction['z']['work_id']!='inventory': return super().deterministic(instruction,tools)
        # The reference derives a screen via the candidate menu; a permission can now
        # remove optional screen. Construct its factual output directly instead.
        self.validate_instruction(instruction)
        pid=instruction['z']['target']['product_id']
        result=tools.get_product_details(product_id=pid).model_dump(mode='json')
        ref=len(self.history)
        self.core.observe('get_product_details',{'product_id':pid},result,ref)
        self.resolve_conditional(ref)
        self.core.review([self.changed_item],ref)
        hard=self.goal['hard_options']
        feasible=[deepcopy(v) for v in result['variants'].values() if v['available'] is True
                  and all(v['options'].get(k)==v0 for k,v0 in hard.items())]
        self.screen={'item_id':self.changed_item,'available_hard_matches':feasible,
                     'preferred_options':deepcopy(self.goal['preferred_options']),
                     'preferred_available':any(all(v['options'].get(k)==v0 for k,v0 in self.goal['preferred_options'].items()) for v in feasible),
                     'source':ref}
        return {'official_tool':'get_product_details','arguments':{'product_id':pid},'official_result':result,
                'derived_available_options':deepcopy(self.screen),'source':ref}

    def compact(self):
        result=super().compact()
        result['observed_payment_method']=deepcopy(self.core.users[self.core.authenticated]['payment_methods'][self.core.payment])
        result['payment_label_rule']='id is an internal tool identifier, never a card number or last_four. Only source=credit_card has observed brand/last_four.'
        return result

    def state(self):
        result=super().state()
        result['P']['review_audit']=deepcopy(self.core.review_audit)
        return result
