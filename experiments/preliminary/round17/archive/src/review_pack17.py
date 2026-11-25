"""Create shuffled, label-masked reason packets; mapping is not part of the review packet."""
import json,random
from pathlib import Path
R=Path(__file__).resolve().parent.parent;B=R/'results/batch01'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def make():
 api=[json.loads(x) for x in (B/'model_calls.jsonl').read_text('utf-8').splitlines()];items=[]
 for index,x in enumerate(api):
  if x['stage']!='controller' or x['status']!='success':continue
  d=json.loads(x['response']['choices'][0]['message']['content']);state=json.loads(x['messages'][1]['content'])['state'];text=[{'work_id':d['work_id'],'reason':d.get('reason'),'expected':d.get('expected')}] if 'work_id'in d else d.get('comparison',[])
  items.append(({'statements':text,'current_target_stock':state['catalog']['7765186836']['variants']['9013366374']['available'],'user_permission_and_preferences':state['g'],'acceptance_status':state['user_intent_and_permission'],'current_conditions':state['C'],'historical_context':state['historical_information'],'current_contract_gate_policy':state['execution_contract_policy']},{'id':x['branch'],'call_index':index,'raw_decision':d}))
 random.Random(1701).shuffle(items);packet=[];mapping={}
 for i,(p,m) in enumerate(items,1):
  code=f'R{i:03d}';packet.append({'code':code,**p});mapping[code]=m
 (R/'results/REVIEW_PACKET.json').write_text(json.dumps({'limits':'Group/condition names and trace IDs removed; comparison style and content can still reveal source. Same author knows experimental context; not independent or fully blinded.','items':packet},ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'results/REVIEW_MAPPING.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
 print({'items':len(packet)})
if __name__=='__main__':make()
