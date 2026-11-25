"""Offline scenario construction from public local tau2 files. No model calls."""
import json
from pathlib import Path
from copy import deepcopy
from decimal import Decimal
import hashlib

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'tau2-official').exists())
DATA=ROOT/'tau2-official/data/tau2/domains/retail'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
db=read(DATA/'db.json'); tasks=read(DATA/'tasks.json')
definitions=[
 {'task_id':'70','hard_options':{'color':'black','ventilation':'high'},'preferred_options':{'size':'M'},
  'acceptable_variant':'1665571435','change':'Before you submit, I no longer want blue. Black and high ventilation are now required. Medium remains my first choice; do not assume I accept large. Keep the same exchange item and original Visa payment method. Tell me the alternatives before making a new plan.'},
 {'task_id':'52','hard_options':{'resolution':'30MP','storage':'CF card'},'preferred_options':{'zoom':'10x'},
  'acceptable_variant':'6384525445','change':'Before you submit, I need CF card storage instead of SD card, and I require 30MP resolution. I still prefer 10x zoom; do not assume I accept a lower zoom. Keep the same camera exchange and PayPal account. Tell me the alternatives before making a new plan.'}]
for cfg in definitions:
    task=next(t for t in tasks if t['id']==cfg['task_id'])
    args=deepcopy(next(a['arguments'] for a in task['evaluation_criteria']['actions'] if a['name']=='exchange_delivered_order_items'))
    order=db['orders'][args['order_id']]; uid=order['user_id']; item=next(i for i in order['items'] if i['item_id']==args['item_ids'][0])
    product=db['products'][item['product_id']]; method=db['users'][uid]['payment_methods'][args['payment_method_id']]
    difference=float(sum(Decimal(str(product['variants'][nid]['price']))-Decimal(str(next(i for i in order['items'] if i['item_id']==iid)['price']))
                         for iid,nid in zip(args['item_ids'],args['new_item_ids'])))
    history=[{'role':'user','content':task['user_scenario']['instructions']['reason_for_call']}]
    observations=[('find_user_id_by_name_zip',{'first_name':db['users'][uid]['name']['first_name'],'last_name':db['users'][uid]['name']['last_name'],'zip':db['users'][uid]['address']['zip']},uid),
                  ('get_user_details',{'user_id':uid},db['users'][uid]),('get_order_details',{'order_id':args['order_id']},order),
                  ('get_product_details',{'product_id':item['product_id']},product)]
    for idx,(name,parameters,result) in enumerate(observations):
        ident='given_'+str(idx)
        history.extend([{'role':'assistant','tool_calls':[{'id':ident,'type':'function','function':{'name':name,'arguments':json.dumps(parameters)}}]},
                        {'role':'tool','tool_call_id':ident,'content':json.dumps(result,ensure_ascii=False)}])
    history.extend([{'role':'assistant','content':'Please confirm this exact exchange plan: '+json.dumps({'arguments':args,'difference':difference,'new_options':product['variants'][args['new_item_ids'][0]]['options'],'payment_method':method})+'. These are all the exchange items. Submission is one-time.'},
                    {'role':'user','content':'Yes, I explicitly confirm that exact exchange, all listed items, the disclosed difference and payment method. Please proceed.'}])
    cfg.update(item_id=item['item_id'],product_id=item['product_id'],order_id=args['order_id'],user_id=uid,
               payment_method=method,canonical_semantics={'item_id':item['item_id'],'hard_options':cfg['hard_options'],'preferred_options':cfg['preferred_options'],'alternative_permission':'unknown'})
    alt=product['variants'][cfg['acceptable_variant']]
    cfg['private_user_policy']={'goal':'Exchange only the named item in the current order, preserving hard requirements and the same payment method.',
        'hard_options':cfg['hard_options'],'preferred_options':cfg['preferred_options'],
        'fallback':'If the preferred combination is unavailable, accept ONLY variant '+alt['item_id']+' with options '+json.dumps(alt['options'])+' if actually in stock. Do not accept other variants.',
        'reply_rule':'When the agent names this specific acceptable variant with unknown stock, state willingness CONDITIONAL on stock and ask it to check; this grants a rule now but does not assert stock. If its stock is known true, allow it. If asked vaguely, ask for concrete options. Do not invent inventory/prices.',
        'confirmation_rule':'Only explicitly approve a current complete proposal with exact item pair, amount and same payment disclosed. A variant permission is not approval. Reject contradictory payment descriptions; your payment method facts are '+json.dumps(method)}
    fixture={'task_id':cfg['task_id'],'order_id':args['order_id'],'shared_history':history,
        'approved_prefix':{'old_plan':args,'old_difference':difference,'old_confirmed':True},'change_message':{'role':'user','content':cfg['change']}}
    save(HERE/'scenarios'/('task'+cfg['task_id']+'.json'),{'config':cfg,'fixture':fixture,'official_task':task})
save(HERE/'scenarios/initial_database.json',db)
(HERE/'scenarios/official_policy.md').write_bytes((DATA/'policy.md').read_bytes())
save(HERE/'scenarios/source_hashes.json',{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [DATA/'db.json',DATA/'tasks.json',DATA/'policy.md']})
save(HERE/'config.json',{'model':'deepseek-flash','temperature':0,'thinking':False,'retries':0,'timeout':60,
    'tasks':['70','52'],'states':['known','unknown'],'repeats':2,'budget_each':{'agent_calls':24,'agent_tokens':60000,'work_steps':9},
    'first_work':{'known':['screen','clarify'],'unknown':['inventory','clarify']},
    'execution_order':'tasks 70 then 52; r1 known screen/clarify then unknown clarify/inventory; r2 unknown inventory/clarify then known clarify/screen',
    'prefix':'one fresh semantic parse per task-repeat, shared by four suffixes; canonical disagreement is initialization failure, no replacement',
    'sampling':'16 fresh suffixes, no replay/retries/replacement; provided history is scenario data, not full-task sampling',
    'labels':False})
print('Built 2 controlled variants from official base tasks 70 and 52; no API calls.')
