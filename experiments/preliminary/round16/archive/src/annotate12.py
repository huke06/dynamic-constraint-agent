"""Post-run source-bound semantic annotations, never sets expected truth or verdict."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent.parent;B=R/'results/batch03';E=B/'evaluation'
def read(p):return json.loads(p.read_text('utf-8'))
review=read(E/'semantic_review.json')
for key,u in review['utterances'].items():
 raw=read(E/'extractions'/(key+'.json'))
 for i,c in enumerate(raw['claims']):
  d=json.loads(json.dumps(c));q=c.get('quote','');why=None
  if c['kind']=='enumeration' and q=='These are all exchange items.':d['kind']='exchange_scope';why='Exchange item scope, not exhaustive product catalogue.'
  elif c['kind']=='options' and 'options'in c and not isinstance(c.get('asserted'),dict):
   if not c.get('selector'):
    d={'kind':'nonassertion','quote':q,'reason':'Restates user request/preferences rather than named SKU facts.'};why='User-intent statement, separately reviewed.'
   else:d['asserted']=d['options'];why='Options object explicitly extracted in wrong JSON field; preserve literal values.'
  elif c['kind']=='stock' and "I can't submit the blue medium" in q:
   d={'kind':'nonassertion','quote':q,'reason':'Refuses stale original plan because user changed color, not an inventory assertion.'};why='Full clause explicitly ties inability to user requirement change.'
  elif c['kind']=='payment' and isinstance(c.get('asserted'),list):
   values=c['asserted'];d['asserted']={'id':values[0]['payment_method_id']};why='Single explicit payment method ID, not list of payment objects.'
  if why:u['patches'].append({'operation':'replace','index':i,'claim':d,'reason':why})
 name,ref=key.rsplit('_ref',1);trajectory=read(B/(name+'_trajectory.json'));entry=next(e for e in trajectory if e.get('assistant_ref')==int(ref));text=entry['assistant']
 def append(claim,reason):u['patches'].append({'operation':'append','claim':claim,'reason':reason})
 if text.startswith('Please explicitly confirm this complete exchange proposal: '):
  body=text.split('proposal: ',1)[1].split('. These are all exchange items.',1)[0];plan=json.loads(body)
  for row in plan['rows']:
   quote=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'))
   append({'kind':'options','quote':quote,'selector':{'variant_id':row['new_item_id']},'asserted':row['options']},'Bind duplicate row item IDs and specifications to explicit row, retaining exact JSON quote; independent program audit checks all fields.')
 if name=='t70_r1_known_candidate':
  quote='The medium-size black options (medium ventilation, or low ventilation) are all out of stock.'
  append({'kind':'enumeration','quote':quote,'selector':{'options':{'color':'black','size':'M'}},'scope':'all','asserted':[{'options':{'ventilation':'medium'}},{'options':{'ventilation':'low'}}]},'Both alternatives literally asserted; raw extractor missed catalogue existence of low-ventilation M pattern.')
 if name=='t70_r1_unknown_direct':
  quote='**Black, size M, low ventilation** — item 6048672633, **not available**'
  append({'kind':'options','quote':quote,'selector':{'variant_id':'6048672633'},'asserted':{'color':'black','size':'M','ventilation':'low'}},'Explicit item-to-size binding must be checked, not only stock false.')
 if name=='t70_r1_known_candidate':
  # This is an inability caused by changed user goal; not an unparsed tool fact.
  pass
(E/'semantic_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
prefs={n:{'status':'accurate','basis':'Assistant review of actual freeform work messages against public original change; no preference assertion in canonical confirmation template. Not independent blinded annotation.'} for n in read(B/'results.json')}
prefs['t52_r1_unknown_candidate']={'status':'inaccurate','quote':"So I can't meet all three of your requirements (30MP, CF card, 10x zoom)",'basis':'Public change makes 30MP/CF hard requirements; 10x is preference. Actual lower zoom was later authorized, which does not erase wording error.'}
(E/'preference_review.json').write_text(json.dumps(prefs,ensure_ascii=False,indent=2),encoding='utf-8')
print({'reviewed':len(review['utterances']),'patches':sum(len(x['patches']) for x in review['utterances'].values())})
