from construct18 import R,read
from world18 import World
from run18 import messages
from score18 import outcome
from tests18 import do
def check():
 checks={}
 for tid in read(R/'configs/tasks.json'):
  c=read(R/f'configs/tasks/{tid}/adapted.json');a=World(c,'stable');b=World(c,'changed')
  for g in ('free','framework'):checks[tid+g+'_first_prompt_identical']=messages(a,g)==messages(b,g)
  checks[tid+'_premature_stop_fails']=not outcome(do(a,'stop')['after'])['final_correct']
  b=World(c,'changed');do(b,'prepare',{'arguments':b.args()});do(b,'confirm',{'arguments':b.args()})
  if c['change_type']=='withdrawal':do(b,'stop')
  else:
   if c['change_type']=='resource':do(b,'clarify',{'variant_id':c['fallback']})
   do(b,'prepare',{'arguments':b.args()});do(b,'confirm',{'arguments':b.args()});do(b,'submit',{'arguments':b.args()})
  checks[tid+'_correct_changed_outcome_passes']=outcome(b.export())['final_correct']
  checks[tid+'_hidden_future_not_in_payload']='change_message' not in messages(World(c,'stable'),'free')[1]['content'] and 'fallback' not in messages(World(c,'stable'),'framework')[1]['content']
 assert all(checks.values()),checks
 return {'passed':True,'model_calls':0,'checks':checks}
