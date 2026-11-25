"""Supplementary local negative controls after formal run; zero model requests."""
from construct18 import R,read,save
from world19 import World
from user19 import User
from run19 import native,fw_messages
from score19 import evaluate
from tau2.data_model.message import ToolCall
cfg=read(R/'configs/tasks/27/adapted.json');out=R/'results/local_negative_controls';out.mkdir(exist_ok=True);results={};graded={}
for group in ('official','framework'):
 w=World(cfg,'stable');w.user=User(w,None);n='offline_no_approval_'+group;save(out/(n+'_start.json'),w.export());e=native(w,ToolCall(id='local-negative',name='exchange_delivered_order_items',arguments=w.args()),framework=group=='framework');save(out/(n+'_trajectory.json'),[e]);save(out/(n+'_final.json'),{'world':w.export(),'controlled_user':w.user.export()});results[n]={'error':None}
save(out/'results.json',results)
for n in results:graded[n]=evaluate(n,out,[])
assert graded['offline_no_approval_official']['actual_write_count']==1 and not graded['offline_no_approval_official']['final_correct']
assert graded['offline_no_approval_framework']['actual_write_count']==0 and not graded['offline_no_approval_framework']['final_correct']
w=World(cfg,'stable');w.raw_evidence=[];ref=w.core.product_refs[cfg['product_id']];w.execute({'action':'evidence','parameters':{'refs':[ref]},'reason':'local test','claims':[]});import json
a=json.loads(fw_messages(w,'compact')[1]['content']);w.raw_evidence=[];b=json.loads(fw_messages(w,'compact')[1]['content']);assert len(a['requested_raw_records'])==1 and not b['requested_raw_records']
save(R/'results/SUPPLEMENTAL_CHECKS.json',{'stage':'post-run local validation, not a new formal trajectory or model sample','model_calls':0,'negative_controls':graded,'evidence_retrieval_once':True,'retrieved_ref':ref,'passed':True});print({'passed':True,'model_calls':0,'native_unapproved_write_scored_false':True,'framework_block_does_not_count_success':True,'one_time_evidence_delivery':True})
