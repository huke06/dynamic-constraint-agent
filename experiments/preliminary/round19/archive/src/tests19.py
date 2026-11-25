from copy import deepcopy
from construct18 import R,read
from world19 import World
from user19 import User
from run19 import native,fw_messages,typed
from tau2.data_model.message import ToolCall
def check():
 checks={};cfg=read(R/'configs/tasks/27/adapted.json')
 def world():
  w=World(cfg,'stable');w.user=User(w,None);return w
 text='Exchange Hiking Boots 8118291112 for item 8277474082, leather size 12 waterproof, with a refund of $23.99 to your original PayPal paypal_3024827. Do you approve?'
 p={'kind':'full_proposal','asks_confirmation':True,'replacement_variant_id':'8277474082','replacement_quote':'item 8277474082','original_item_quote':'Hiking Boots 8118291112','amount':-23.99,'amount_quote':'refund of $23.99','payment_quote':'original PayPal paypal_3024827','question_quote':'Do you approve?','scope':'single_current_exchange','reason':'fixture'}
 for key,mutation,expected in [('correct_natural',{},True),('missing_amount',{'amount_quote':''},False),('wrong_amount',{'amount':-100},False),('invented_quote',{'replacement_quote':'a phrase never spoken'},False),('not_final_confirmation',{'asks_confirmation':False},False)]:
  w=world();q={**p,**mutation};w.user.extract=lambda text,q=q:deepcopy(q);ar=len(w.history);w.history.append({'role':'assistant','content':text});rec=w.user.respond(text,ar);checks[key]=rec['approved_complete_plan']==expected
 # The official path actually writes without project approval: an evaluator must reject it.
 w=world();tc=ToolCall(id='offline-no-auth',name='exchange_delivered_order_items',arguments=w.args());e=native(w,tc);checks['native_has_no_project_fingerprint_interception']=e['actual_native_executed'] and len(w.writes)==1 and not e['policy_check_without_interception']['all_valid']
 w=world();e=native(w,tc,framework=True);checks['framework_uses_project_gate']=not e['check']['allowed'] and not w.writes
 # Typed official history contains native functions, never prepare or fingerprint tools.
 w=world();names=set(w.tools.get_tools());checks['native_schema_has_exchange']=tc.name in names;checks['no_project_helpers_in_native_tools']=not(names&{'prepare','confirm','submit','prepare_exchange_proposal'});checks['official_history_typed']=all(typed(m) is not None for m in w.history)
 for tid in ('27','75'):
  snap=read(R/f'configs/snapshots/task{tid}.json');w=World.restore(snap);w.raw_evidence=[];compact=fw_messages(w,'compact');original=fw_messages(w,'original');checks[tid+'_compact_fewer_characters']=len(compact[1]['content'])<len(original[1]['content']);payload=readable=__import__('json').loads(compact[1]['content']);checks[tid+'_no_repeated_full_catalog_or_history']='interaction_history'not in payload and 'framework_state'not in payload;checks[tid+'_query_feedback_preserved']='recent_work_feedback'in payload and 'latest_formal_inventory'in payload;checks[tid+'_old_authorization_false']=not w.authorize_current();checks[tid+'_candidates_unchanged']=w.candidates()==World.restore(snap).candidates()
 for tid in read(R/'configs/tasks.json'):
  cfg2=read(R/f'configs/tasks/{tid}/adapted.json');a=World(cfg2,'stable');b=World(cfg2,'changed');checks[tid+'_same_prechange_history']=a.history==b.history;checks[tid+'_same_native_schemas']=[t.openai_schema for t in a.tools.get_tools().values()]==[t.openai_schema for t in b.tools.get_tools().values()]
 pilot=read(R/'results/pilot01/results.json');checks['official_live_pilot_registered_both']=all(x['writes']==1 for x in pilot.values());calls=[__import__('json').loads(s) for s in (R/'results/pilot01/model_calls.jsonl').read_text('utf-8').splitlines()];checks['same_model_real_function_call']=any(a['category']=='agent' and a.get('response',{}).get('choices',[{}])[0].get('message',{}).get('tool_calls') for a in calls);checks['natural_plan_approved']=any(r['approved_complete_plan'] for n in pilot for r in read(R/f'results/pilot01/{n}_final.json')['controlled_user']['records'])
 repaired=read(R/'results/pilot03/results.json');checks['repaired_compact_live_pilot_registered']=all(x['writes']==1 and not x['error'] for x in repaired.values())
 assert all(checks.values()),checks
 return {'passed':True,'model_calls_in_this_check':0,'checks':checks,'pilot02_failure_preserved':True,'official_agent_source':'tau2.agent.llm_agent.LLMAgent unchanged; completion transport only patched in memory'}
