"""Independent time-local replay of actual utterances, using the reused verifier."""
import json
from decimal import Decimal
from pathlib import Path
from fact_verifier import replay
R=Path(__file__).resolve().parent.parent
def read(p):return json.loads(p.read_text('utf-8'))
out=[]
for folder in ('main','exploratory'):
 for n in read(R/f'results/{folder}/results.json'):
  path=R/f'results/{folder}/{n}_trajectory.json'
  if not path.exists():continue
  for index,e in enumerate(read(path)):
   ref=e.get('assistant_ref')
   if ref is None:continue
   h=e['after']['history'];text=h[ref]['content'];ev=replay(h,ref);cfg=e['before']['cfg'];pid=cfg['product_id'];prod=ev['products'][pid];kind=e['decision']['action'];checks={}
   if kind=='confirm':
    prefix='Please independently approve this exact complete exchange proposal: ';payload,end=json.JSONDecoder().raw_decode(text[len(prefix):]);args=payload['arguments'];order=ev['orders'][args['order_id']];method=ev['users'][order['user_id']]['payment_methods'][args['payment_method_id']];checks['payment_method']=payload['payment_method']==method;total=Decimal('0')
    for row in payload['rows']:
     v=prod['variants'][row['new_item_id']];orig=next(i for i in order['items'] if i['item_id']==row['item_id']);delta=Decimal(str(v['price']))-Decimal(str(orig['price']));total+=delta;checks['variant_'+row['new_item_id']]=v['available'] is True and v['options']==row['options'] and Decimal(str(row['new_price']))==Decimal(str(v['price'])) and Decimal(str(row['old_price']))==Decimal(str(orig['price'])) and Decimal(str(row['difference']))==delta
    checks['difference']=Decimal(str(payload['difference']))==total;checks['all_exchange_items']=args['item_ids']==[cfg['item_id']];checks['current_specification']=args['new_item_ids']==[e['before']['desired']];checks['no_settlement_claim']='settled'not in text and 'refunded'not in text
   else:
    vid=e['decision']['parameters']['variant_id'];requested=e['before']['desired'];v=prod['variants'][vid];t=prod['variants'][requested];checks['target_exists_and_stock']=f"The currently requested item {requested} exists; observed stock is {json.dumps(t['available'])}." in text;checks['alternative_exists_and_options']=f"Alternative {vid} exists with options "+json.dumps(v['options'],ensure_ascii=False,separators=(',',':'),sort_keys=True) in text;checks['price_and_stock']=f"price {v['price']}, and observed stock {json.dumps(v['available'])}." in text;checks['not_yet_accepted']=vid!=requested and not e['before']['withdrawn'];checks['permission_separate_from_approval']='Specification permission is separate from final transaction approval.' in text
   out.append({'folder':folder,'id':n,'entry':index,'assistant_ref':ref,'quote':text,'kind':kind,'evidence_product_ref':ev['product_refs'][pid],'evidence_order_ref':ev['order_refs'][cfg['order_id']],'exclusive_evidence_cutoff':ref,'checks':checks,'supported':all(checks.values())})
(R/'results/FACTS.json').write_text(json.dumps({'method':'reused fact_verifier.replay(history, exclusive assistant_ref); only prior tool evidence, never later inventory or results','utterances':out,'passed':all(x['supported'] for x in out)},ensure_ascii=False,indent=2),encoding='utf-8')
assert all(x['supported'] for x in out),[x for x in out if not x['supported']]
print({'utterances':len(out),'main':sum(x['folder']=='main' for x in out),'passed':True})
