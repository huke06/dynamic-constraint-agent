import json
from copy import deepcopy
from engine import Case
from exchange_core import packed
import experiment16 as prior
PID='7765186836';TARGET='9013366374';ALT='1665571435';ITEM='3358616356'
QUOTE='Before submitting, black is no longer required: high ventilation is required, and blue and size M are my preferences. I accept item 9013366374 (blue, size M, high ventilation) only if it is currently in stock. I have not accepted any other alternative specification. Keep the same helmet exchange item and original Visa. This conditional willingness is not final approval of a new plan.'
OLD_COMPACT=Case.compact
def compact(c):
 d=OLD_COMPACT(c);historical={'prior_plan_and_approval':d['H'].pop('original_approval'),'compatibility':d['C'].pop('historical_plan_compatible',None),'notice':'Historical only, never an extra operation gate.'};d['H'].pop('historical_approval_notice',None)
 d['historical_information']=historical;d['user_intent_and_permission']={'alternative_status':'explicitly_rejected' if getattr(c,'user_declined',False) else 'accepted' if c.goal['alternative_permission']!='unknown' else 'not_yet_accepted','original_current_condition_quote':QUOTE,'source_ref':11,'variant_permission_is_not_transaction_authorization':True}
 d['execution_contract_policy']={'rule':'Only conditions explicitly in the selected work contract are execution gates. Historical compatibility is context, not a submit precondition. Not_yet_accepted does not mean explicitly_rejected.','submit_required_conditions':['identity','plan_current','authorization_current','not_written']}
 return d
Case.compact=compact
def construct(state):
 p=prior.read(prior.HERE/'scenarios/public/task70.json');fixture=deepcopy(p['fixture']);fixture['change_message']={'role':'user','content':QUOTE};sem={'item_id':ITEM,'hard_options':{'ventilation':'high'},'preferred_options':{'color':'blue','size':'M'}}
 # Original public approved plan remains historical; a new conditional request revokes its transaction authority.
 c=Case(fixture,sem);c.core.records['authorization']['status']='stale';c.goal['alternative_permission']='unknown';c.goal['permission_source']=None
 result=deepcopy(c.core.products[PID]);result['variants'][TARGET]['available']=False if state=='known_out' else None
 c.core.observe('get_product_details',{'product_id':PID},result,12);c.apply_user({'change':{'present':False},'authorization':{'approved':False},'permission_update':{'kind':'grant','variant_id':TARGET,'source_ref':11,'source_quote':QUOTE}},10,11);c.core.review([ITEM],12)
 if state!='known_out':
  rec=c.core.records['match:'+ITEM];c.core.put('match:'+ITEM,None,rec['depends_on'],[12],status='unknown')
 wrapper={'official_tool':'get_product_details','arguments':{'product_id':PID},'official_result':result,'source':12};c.history.append({'role':'observation','work':'inventory','content':packed(wrapper)});c.core.evidence['12']=deepcopy(c.history[-1]);c.permission_history=[deepcopy(c.conditional_permission)];c.plan=None;c.confirmations=[]
 return c
def environment(state):
 db=prior.read(prior.HERE/'scenarios/initial_database.json');db['products'][PID]['variants'][TARGET]['available']=state=='unknown_in';return db
def clarification(c):
 prod=c.core.products[PID];v=prod['variants'][TARGET];alt=prod['variants'][ALT];assert alt['available'] is True
 text=('The blue size M high-ventilation helmet '+TARGET+' exists; its current availability is '+('not yet verified' if v['available'] is None else 'out of stock' if v['available'] is False else 'in stock')+'. ')
 fields={'target':{'item_id':TARGET,'available':v['available'],'options':v['options'],'price':v['price']},'alternative':{'item_id':ALT,**deepcopy(alt)},'source':c.core.product_refs[PID]}
 text+='The following alternative is in stock: '+packed(fields['alternative'])+'. You have not accepted this alternative yet. Would you accept it or keep the original order? Variant acceptance is separate from final approval of the complete proposal.'
 return text,fields
class Client(prior.Client):
 def ask(self,branch,category,stage,messages,max_tokens=1400,case=None):
  if stage=='worker' and case and json.loads(messages[1]['content'])['u']['z']['work_id']=='clarify':
   self.pending[branch]=('clarify',case);text,fields=clarification(case);self.grounded.write(packed({'branch':branch,'assistant_ref':len(case.history),'text':text,'fields':fields})+'\n');self.grounded.flush();return text
  if category=='environment_user':
   wid,c=self.pending[branch];assert c.history[-1]['role']=='assistant'
   if wid=='clarify':
    stock=c.core.products[PID]['variants'][TARGET]['available'];reply={'reply':'Please verify the named blue size M helmet first. I have not decided to accept another specification.' if stock is None else 'I accept item 1665571435, the black size L high-ventilation helmet, if it is in stock. Please prepare the complete proposal and ask for final approval; I have not approved submission yet.','allowed_alternative':stock is False,'confirmed':False};key='pending_stock' if stock is None else 'accept_alternative'
   else:
    p=c.plan;assert p and p['arguments']['new_item_ids']==[c.goal['alternative_permission']];assert c.core.compile(p['arguments'])['fingerprint']==p['quote']['fingerprint'];reply={'reply':'I explicitly approve this exact complete proposal: '+packed({'arguments':p['arguments'],'difference':p['quote']['difference']})+'. This is the only exchange item. Submit exactly this proposal using my same original Visa ending 7312.','allowed_alternative':True,'confirmed':True};key='confirm_current_plan'
   row={'branch':branch,'trigger_work':wid,'trigger_assistant_ref':len(c.history)-1,'private_response_key':key,'reply':reply,'model_calls':0};self.events.append(row);self.controlled_stream.write(packed(row)+'\n');self.controlled_stream.flush();return reply
  return super().ask(branch,category,stage,messages,max_tokens,case)

OLD_VALIDATE=Case.validate_instruction
OLD_STATE=Case.state
def validate(c,u):
 try:
  contract=OLD_VALIDATE(c,u);event={'allowed':True,'work':u['z']['work_id'],'contract':deepcopy(contract),'history_length':len(c.history)}
 except Exception as ex:
  event={'allowed':False,'work':u.get('z',{}).get('work_id'),'feedback':getattr(ex,'feedback',str(ex)),'history_length':len(c.history)}
  c.actual_contract_checks=getattr(c,'actual_contract_checks',[])+[event];raise
 c.actual_contract_checks=getattr(c,'actual_contract_checks',[])+[event];return contract
def state(c):
 d=OLD_STATE(c);d['P']['actual_contract_checks']=deepcopy(getattr(c,'actual_contract_checks',[]));return d
Case.validate_instruction=validate
Case.state=state
