"""Read public Round08 fixture; split restricted simulation/evaluation inputs. No API."""
import json,hashlib
from pathlib import Path
from copy import deepcopy
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'08_同任务配对复验'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# These interpretations reference public user words, not the hidden fallback/evaluator.
PUBLIC={
 '70':{'item_id':'3358616356','product_id':'7765186836','hard_options':{'color':'black','ventilation':'high'},
       'preferred_options':{'size':'M'},'masked_variant':'1665571435',
       'claims':[('g.hard_options.color','Black and high ventilation are now required.','black'),
                 ('g.hard_options.ventilation','Black and high ventilation are now required.','high'),
                 ('g.preferred_options.size','Medium remains my first choice; do not assume I accept large.','M'),
                 ('g.alternative_permission','do not assume I accept large','unknown'),
                 ('scope/payment','Keep the same exchange item and original Visa payment method.','unchanged')]},
 '52':{'item_id':'5996159312','product_id':'8940227892','hard_options':{'resolution':'30MP','storage':'CF card'},
       'preferred_options':{'zoom':'10x'},'masked_variant':'6384525445',
       'claims':[('g.hard_options.resolution','I require 30MP resolution.','30MP'),
                 ('g.hard_options.storage','I need CF card storage instead of SD card','CF card'),
                 ('g.preferred_options.zoom','I still prefer 10x zoom; do not assume I accept a lower zoom.','10x'),
                 ('g.alternative_permission','do not assume I accept a lower zoom','unknown'),
                 ('scope/payment','Keep the same camera exchange and PayPal account.','unchanged')]}}

for tid,spec in PUBLIC.items():
    source=OLD/'scenarios'/('task'+tid+'.json'); old=read(source)
    fixture=deepcopy(old['fixture']); cfg=old['config']; ref=len(fixture['shared_history'])
    evidence=[]
    for field,quote,value in spec['claims']:
        assert quote in fixture['change_message']['content']
        evidence.append({'field':field,'normalized_value':value,'user_ref':ref,'quote':quote,
                         'interpretation':'Medium modifies size in the already discussed helmet sizing; not ventilation. Map to legal enum M.' if field.endswith('.size') else 'public explicit requirement, preference or preserved scope/payment'})
    if tid=='70':
        prior='The size is too small and you want medium, plus you want high ventilation.'
        assert prior in fixture['shared_history'][0]['content']
        evidence[2]['supporting_context']=[{'ref':0,'quote':prior},
            {'ref':8,'catalogue_field':'variants.9013366374.options.size','value':'M'},
            {'ref':9,'meaning':'given previous proposal explicitly lists size M, blue, high ventilation'}]
    interpretation={k:deepcopy(spec[k]) for k in ('item_id','hard_options','preferred_options')}
    interpretation['alternative_permission']='unknown'
    public={'task_id':tid,'fixture':fixture,'verified_interpretation':interpretation,
        'item_id':spec['item_id'],'product_id':spec['product_id'],'order_id':fixture['order_id'],
        'hard_options':spec['hard_options'],'preferred_options':spec['preferred_options'],
        'inventory_intervention':{'history_index':8,'product_id':spec['product_id'],'variant_id':spec['masked_variant'],
            'field':'available','known':True,'unknown':None,'source':'public observed product record; intervention target, not acceptance/answer'},
        'user_claim_evidence':evidence,'construction':'Offline author-checked public starting condition, not online semantic accuracy or gold transaction answer.'}
    save(HERE/'scenarios/public'/('task'+tid+'.json'),public)
    # This file is read only by environment simulation and final scoring, never Case construction.
    private={'private_user_policy':cfg['private_user_policy'],'evaluation':{k:cfg[k] for k in (
        'acceptable_variant','payment_method','item_id','product_id','order_id','hard_options')}}
    save(HERE/'scenarios/private'/('task'+tid+'.json'),private)

batch=OLD/'results/20261122T125916414502Z'
calls=[json.loads(l) for l in (batch/'model_calls.jsonl').read_text(encoding='utf-8').splitlines()]
history=[]
for row in calls:
    if row['branch'].startswith('t70'):
        raw=json.loads(row['response']['choices'][0]['message']['content'])
        history.append({'branch':row['branch'],'response_id':row['response']['id'],'messages':row['messages'],
            'raw_model_reply':row['response']['choices'][0]['message']['content'],'parsed':raw,
            'public_user_quote':read(HERE/'scenarios/public/task70.json')['fixture']['change_message']['content'],
            'field_differences':{'remove_preferred':{'ventilation':'medium'},'add_preferred':{'size':'M'}},
            'proposal_mapping':'3.1.1 state construction / field binding; not 3.1.4 first-work outcome',
            'used_as_round09_response':False})
assert len(history)==2
save(HERE/'sources/round08_helmet_state_construction.json',history)
save(HERE/'sources/source_hashes.json',{str(p):sha(p) for p in [OLD/'PROTOCOL.md',OLD/'RESULTS.md',batch/'model_calls.jsonl',OLD/'scenarios/task70.json',OLD/'scenarios/task52.json']})
cfg=read(HERE/'config.json'); cfg.update(experiment='09_fixed_start_replication',
    prefix='No online initial semantics. Hydrate checked public runtime JSON; compare all state/view/candidates to frozen snapshots before each branch.',
    initial_interpretation_source='public user quotes and observed catalogue only; no private fallback or standard answer',
    snapshot_public='snapshots/public',snapshot_private='scenarios/private',
    sampling='16 planned fresh suffixes, no replay/retry/replacement; failed start/work/evaluation stage recorded')
save(HERE/'config.json',cfg)
print('Public/restricted inputs separated; two historical field-binding failures archived. No API calls.')
