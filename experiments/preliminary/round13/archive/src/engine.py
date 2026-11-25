"""Round 08: independent permission and transaction-authorization provenance."""
from copy import deepcopy
from legacy_engine import Case as Case07
from baseline_engine import SAT, UNMET, UNKNOWN, NA
from normalization import enums, normalize_options
class PendingVerification(ValueError): pass

class Case(Case07):
    def __init__(self,fixture,semantics):
        super().__init__(fixture,semantics)
        self.semantic_events=[]; self.authorization_events=[]; self.pending_verification=None

    def exact_source(self,update,ref):
        quote=update.get('source_quote')
        if update.get('source_ref')!=ref or not quote or quote not in self.history[ref].get('content',''):
            raise ValueError('update requires exact quote bound to its actual user message')

    def invalidate_plan(self,why,ref):
        self.plan=None; self.confirmations=[]
        for key in ('authorization','total'):
            if key in self.core.records: self.core.records[key]['status']='stale'
        self.authorization_events.append({'event':'plan_invalidated','why':why,'user_source':ref})

    def reset_permission(self,ref):
        self.conditional_permission=None; self.goal.pop('conditional_permission',None)
        self.goal['alternative_permission']='unknown'; self.goal['permission_source']=None
        for key in ('conditional_rule:'+self.changed_item,'conditional_trigger:'+self.changed_item):
            if key in self.core.records: self.core.records[key]['status']='stale'
        self.invalidate_plan('permission/requirements changed',ref)

    def apply_user(self,parsed,assistant_ref,user_ref):
        if self.history[user_ref]['role']!='user': raise ValueError('not a user source')
        change=parsed.get('change',{'present':False})
        permission=parsed.get('permission_update',{'kind':'none'})
        approval=parsed.get('authorization',{'approved':False})
        changed=False
        if change.get('present'):
            self.exact_source(change,user_ref)
            legal=enums(self.core.products[self.core.item(self.changed_item)['product_id']])
            hard,ha=normalize_options(change.get('hard_options',{}),legal)
            preferred,pa=normalize_options(change.get('preferred_options',{}),legal)
            if any(x['status']!='resolved' for x in ha+pa) or change.get('ambiguous'):
                self.pending_verification={'source':user_ref,'normalization':ha+pa,'change':deepcopy(change)}
                self.invalidate_plan('ambiguous change requires verification',user_ref)
                raise PendingVerification('current change has unresolved catalogue values')
            self.pending_verification=None
            self.reset_permission(user_ref)
            self.goal['hard_options'].update(hard); self.goal['preferred_options'].update(preferred)
            if hard or preferred: self.stage_change({**hard,**preferred},user_ref)
            payment=change.get('payment_method_id')
            if payment:
                if payment not in self.core.users[self.core.authenticated]['payment_methods']:
                    self.pending_verification={'payment':payment,'source':user_ref}
                    raise PendingVerification('unobserved payment change')
                self.goal['payment']=payment; self.core.payment=payment
                self.core.put('payment',payment,['profile:'+self.core.authenticated],[user_ref])
            selected=change.get('variant_id')
            if selected:
                self.remember_conditional({'grant':True,'variant_id':selected,'source_quote':change['source_quote']},user_ref)
            changed=True
            self.semantic_events.append({'event':'current_change_applied','source':user_ref,'change':deepcopy(change)})
        kind=permission.get('kind','none')
        if kind not in ('none','grant','reuse','revoke'): raise ValueError('unsupported permission update kind')
        if kind=='revoke':
            self.exact_source(permission,user_ref); self.reset_permission(user_ref); changed=True
        elif kind in ('grant','reuse'):
            old=getattr(self,'conditional_permission',None)
            cached=bool(old and permission.get('variant_id')==old['variant_id'] and permission.get('source_ref')==old['source']
                        and permission.get('source_quote')==old['source_quote'])
            if cached:
                self.exact_source(permission,old['source'])
                self.semantic_events.append({'event':'historical_permission_reused','source':old['source'],
                                             'current_user':user_ref,'variant_id':old['variant_id']})
            elif old and permission.get('variant_id')==old['variant_id'] and kind=='grant':
                self.exact_source(permission,user_ref)
                self.semantic_events.append({'event':'current_affirmation_preserves_original_permission',
                    'original_source':old['source'],'current_user':user_ref,'variant_id':old['variant_id']})
            else:
                if kind=='reuse': raise ValueError('reuse does not identify stored original permission')
                self.exact_source(permission,user_ref)
                if old and old['variant_id']!=permission.get('variant_id'):
                    self.reset_permission(user_ref); changed=True
                self.remember_conditional({'grant':True,'variant_id':permission['variant_id'],
                                           'source_quote':permission['source_quote']},user_ref)
        if approval.get('approved'):
            self.exact_source(approval,user_ref)
            if changed:
                self.authorization_events.append({'event':'same_turn_approval_not_used_after_change','source':user_ref})
                return
            if self.pending_verification or not self.plan: raise ValueError('authorization needs unambiguous current complete plan')
            if approval.get('arguments')!=self.plan['arguments']: raise ValueError('authorization arguments differ from current proposal')
            if self.history[assistant_ref].get('role')!='assistant': raise ValueError('approval must follow assistant proposal')
            result=self.core.confirm(approval['arguments'],approval['stated_difference'],user_ref,assistant_ref)
            if result['fingerprint']!=self.plan['quote']['fingerprint']: raise ValueError('authorization fingerprint mismatch')
            self.confirmations.append({'result':result,'assistant_ref':assistant_ref,'user_ref':user_ref,'source_quote':approval['source_quote']})
            self.authorization_events.append({'event':'current_plan_authorized','source':user_ref,'assistant_source':assistant_ref,
                'quote':approval['source_quote'],'fingerprint':result['fingerprint']})

    def state(self):
        result=super().state()
        result['P']['semantic_events']=deepcopy(getattr(self,'semantic_events',[]))
        result['P']['authorization_events']=deepcopy(getattr(self,'authorization_events',[]))
        result['C']['pending_verification']=deepcopy(getattr(self,'pending_verification',None))
        return result
