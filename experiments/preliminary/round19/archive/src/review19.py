"""Post-run speech audit. Program arithmetic plus disclosed assistant semantic review."""
from decimal import Decimal
import json
from construct18 import R,read,save
p=read(R/'results/SPEECH_PACKET.json')['items'];auto=read(R/'results/AUTO_FACTS.json');reviews={};proof=[]
for item in p:
 n=item['id'];r=reviews.setdefault(n,{'status':'supported','issues':[],'simulator_deviations':[],'speech_items':0,'review_method':'same assistant inspected all main official speech and independent structured-template checks; no independent blinded gold. Empty native-call content contains no factual assertion.'});r['speech_items']+=bool(item['text']);text=item['text'];checks={};catalog=next(iter(item['latest_visible_catalog'].values()));order=next(iter(item['latest_visible_order'].values()))
 if text.startswith('Please independently approve this exact complete exchange proposal: '):
  data,_=json.JSONDecoder().raw_decode(text[len('Please independently approve this exact complete exchange proposal: '):]);args=data['arguments'];total=Decimal('0')
  for row in data['rows']:
   v=catalog['variants'][row['new_item_id']];old=next(i for i in order['items'] if i['item_id']==row['item_id']);delta=Decimal(str(v['price']))-Decimal(str(old['price']));total+=delta;checks['variant_'+row['new_item_id']]=v['available']is True and row['options']==v['options'] and Decimal(str(row['difference']))==delta and Decimal(str(row['old_price']))==Decimal(str(old['price'])) and Decimal(str(row['new_price']))==Decimal(str(v['price']))
  checks['difference']=Decimal(str(data['difference']))==total;checks['payment_mentioned']=args['payment_method_id'] in text;checks['scope']=args['item_ids']==[i['item_id'] for i in order['items'] if i['item_id']in args['item_ids']]
 elif text.startswith('The requested item ') and 'Alternative 'in text:
  import re
  a=re.search(r'item (\d+) exists.*?value is (true|false|null)',text);b=re.search(r'Alternative (\d+)',text)
  if a and b:checks['requested_stock']=catalog['variants'][a[1]]['available']==json.loads(a[2]);checks['alternative_exists']=b[1]in catalog['variants'];checks['alternative_price']=str(catalog['variants'][b[1]]['price'])in text
 elif text.startswith('The exchange request is registered;'):checks['actual_status']=order['status']=='exchange requested'
 elif text.startswith('I will stop the exchange'):checks['no_registered_exchange']=order['status']=='delivered'
 findings=[f for f in auto if f['id']==n and f['entry']==item['entry']]
 # The simulator call failed before extracting the second wrong boots quote.
 # Actual Agent text is still judged, not silently omitted.
 if n=='t27_changed_r1_official' and item.get('note') and '$3.99 refund' in text:
  findings.append({'id':n,'entry':None,'type':'incorrect_stated_difference','status':'contradicted','quote':'$260.56 − $236.57 = **$3.99 refund**','expected_amount':'-23.99','source':'actual speech preserved after simulator network failure'})
 for f in findings:
  r['issues'].append(f)
  if f['status']=='contradicted':r['status']='contradicted'
  elif r['status']=='supported':r['status']='pending'
  if f['type'].startswith('simulator_'):r['simulator_deviations'].append(f)
 if not all(checks.values()):r['status']='contradicted';r['issues'].append({'type':'template_fact_mismatch','quote':text,'checks':checks})
 proof.append({'id':n,'folder':item['folder'],'assistant_ref':item['assistant_ref'],'entry':item['entry'],'quote':text,'checks':checks,'findings':findings,'judgment':'contradicted' if any(f['status']=='contradicted' for f in findings) or not all(checks.values()) else 'supported','evidence_in':'SPEECH_PACKET.json contemporaneous catalogue/order, exact user interpretation retained'})
# No speech before a transport interruption is not a factual error; completion is
# assessed separately. Pilot failed branches remain failed even if their speech was true.
for folder in ('main','context','pilot01','pilot02','pilot03'):
 path=R/f'results/{folder}/results.json'
 if path.exists():
  for n in read(path):reviews.setdefault(n,{'status':'supported','issues':[],'simulator_deviations':[],'speech_items':0,'note':'No factual customer utterance before interruption; not a business success.'})
save(R/'results/FACT_REVIEW.json',reviews);save(R/'results/FACTS.json',{'method':'Predefined field arithmetic and time-local records, plus assistant reviewed official natural speech. Bare refund/charged amount labels treated as allocation, not settled payment, as frozen protocol specified. No independent reviewer.','items':proof});print({'trajectories':len(reviews),'problem_traces':{n:r['issues'] for n,r in reviews.items() if r['issues']},'nonempty_main_speech':sum(bool(x['text']) for x in p if x['folder']=='main')})
