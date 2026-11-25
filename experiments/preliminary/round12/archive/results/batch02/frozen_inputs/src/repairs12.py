"""Shared state, selected-work feedback and program-grounded confirmation interfaces."""
import json
from copy import deepcopy
from engine import Case
from baseline_engine import Case as Base,SAT,UNMET,UNKNOWN
import baseline_runner as b
from exchange_core import packed
OLD_CONDITIONS=Case.conditions;OLD_COMPACT=Case.compact;OLD_STATE=Case.state
OLD_CANDIDATES=Case.candidates;OLD_APPLY=Case.apply_user;OLD_VALIDATE=Case.validate_instruction
def permission_state(c):
 r=getattr(c,'conditional_permission',None)
 return 'not_obtained' if not r else 'satisfied' if r['sat']==SAT else 'false' if r['sat']==UNMET else 'pending'
def conditions(c):
 d=OLD_CONDITIONS(c);d.pop('old_keyboard_match',None)
 try:c.core.compile(c.core.old_confirmations[0]['arguments']);match=SAT
 except Exception:match=UNMET
 d['historical_plan_compatible']=c.condition(match,['H.original_approval','g'])
 return d
def compact(c):
 d=OLD_COMPACT(c);d['permission_condition_state']=permission_state(c)
 d['permission_history']=deepcopy(getattr(c,'permission_history',[]))
 d['H']['historical_approval_notice']='Historical evidence only; current authorization is determined by C.authorization_current and current plan fingerprint.'
 return d
def state(c):
 d=OLD_STATE(c);d['H']['permission_history']=deepcopy(getattr(c,'permission_history',[]));return d
def candidates(c):
 ws=OLD_CANDIDATES(c)
 if permission_state(c)=='false' and not c.plan:
  ask=next((w for w in Base.candidates(c) if w['work_id']=='clarify'),None)
  if ask:
   ask['completion_test']='permission_rule_acquired';ask['expected_output']='Clarify a different acceptable variant; previous conditional permission remains recorded but its stock condition is false.'
   ws=[w for w in ws if w['work_id']!='clarify']+[ask]
 return ws
def refusal(c,u):
 wid=u.get('z',{}).get('work_id');w=next((w for w in c.candidates() if w['work_id']==wid),None)
 missing={k:v for k,v in (w or {}).get('preconditions',{}).items() if v['sat']!=SAT}
 if not w:missing={'work_applicability':{'sat':UNMET,'reason':'Work is not applicable in current plan/permission stage; it has not been executed.'}}
 return {'selected_work':wid,'object':u.get('z',{}).get('target'),'unmet_preconditions':missing,
  'permission_state':permission_state(c),'conditional_permission':deepcopy(getattr(c,'conditional_permission',None)),
  'catalogue_observation_sources':deepcopy(c.core.product_refs),
  'specific_gap':'Relevant inventory is unknown; a current official product query is missing.' if c.inventory_unknown() else 'Inventory evidence is known; inspect the selected work prerequisites and current authorization.',
  'same_selected_work_check_for_both_groups':True}
class Rejected(ValueError):
 def __init__(self,feedback):self.feedback=feedback;super().__init__(packed(feedback))
def validate(c,u):
 try:return OLD_VALIDATE(c,u)
 except ValueError:raise Rejected(refusal(c,u))
def apply(c,parsed,ar,ur):
 parsed=deepcopy(parsed);before=deepcopy(getattr(c,'conditional_permission',None))
 # Model extracts approval meaning and exact source only; program supplies plan parameters and amount.
 approval=parsed.get('authorization',{})
 if approval.get('approved') and c.plan:
  approval['arguments']=deepcopy(c.plan['arguments']);approval['stated_difference']=c.plan['quote']['difference']
 OLD_APPLY(c,parsed,ar,ur)
 history=getattr(c,'permission_history',[])
 for rule in (before,getattr(c,'conditional_permission',None)):
  if rule and rule not in history:history.append(deepcopy(rule))
 c.permission_history=history
def confirmation(c):
 assert c.plan
 args=deepcopy(c.plan['arguments']);quote=c.core.compile(args)
 assert quote['fingerprint']==c.plan['quote']['fingerprint']
 rows=[]
 for row in quote['rows']:
  pid=c.core.item(row['item_id'])['product_id'];v=c.core.products[pid]['variants'][row['new_item_id']]
  assert v['available'] is True
  rows.append({**deepcopy(row),'available':True,'inventory_source_ref':c.core.product_refs[pid]})
 return {'arguments':args,'rows':rows,'difference':quote['difference'],'payment_method':deepcopy(c.core.users[c.core.authenticated]['payment_methods'][c.core.payment]),'post_submit_status':'exchange requested','fingerprint':quote['fingerprint']}
AUTH='''Interpret only what the current user reply means. Inventory, amount, payment and plan validity are program checked; do not invent a stock barrier. Return JSON with permission_update {kind:"none"}, change {present:false} unless user changes requirements, and authorization {approved:true|false,source_ref:<current_user_ref>,source_quote:"exact user substring"}. A plain explicit approval of the supplied complete current proposal is approved=true. If new conditions, changes or ambiguity occur, report change with source_ref/source_quote, hard_options,preferred_options,ambiguous and approval=false. Never approve a hypothetical willingness as transaction authorization. Do not compute plan parameters.'''
class Client(b.Client):
 def __init__(self,out):super().__init__(out);self.program_stream=(out/'program_confirmations.jsonl').open('w',encoding='utf-8')
 def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
  if stage=='worker' and case and json.loads(messages[1]['content'])['u']['z']['work_id']=='confirm':
   plan=confirmation(case)
   text='Please explicitly confirm this complete exchange proposal: '+packed(plan)+'. These are all exchange items. The modification can be submitted only once. A negative difference means a refund; positive means a charge. No request has been submitted yet.'
   self.program_stream.write(packed({'branch':branch,'plan':plan,'text':text,'model_calls':0})+'\n');self.program_stream.flush();return text
  if stage=='user_semantics' and json.loads(messages[1]['content']).get('current_work')=='confirm':messages=[{'role':'system','content':AUTH},messages[1]]
  return super().ask(branch,category,stage,messages,max_tokens,case)
 def close(self):self.program_stream.close();super().close()
def install():
 Case.conditions=conditions;Case.compact=compact;Case.state=state;Case.candidates=candidates;Case.validate_instruction=validate;Case.apply_user=apply
