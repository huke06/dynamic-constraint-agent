import json,hashlib
from copy import deepcopy
from pathlib import Path
from construct18 import R,read
from world18 import World
from run18 import messages
def do(w,a,p={}):return w.execute({'action':a,'parameters':p,'reason':'offline fixture','claims':[]})
def check():
 checks={};saved={}
 for tid in read(R/'configs/tasks.json'):
  cfg=read(R/f'configs/tasks/{tid}/adapted.json');a=World(cfg,'stable');b=World(cfg,'changed');checks[tid+'_shared_prechange_history']=a.history==b.history and a.visible_state()==b.visible_state();checks[tid+'_free_no_state']=set(json.loads(messages(a,'free')[1]['content']))=={'interaction_history','remaining_budget'}
  initial=deepcopy(b.core.records);do(a,'prepare',{'arguments':a.args()});do(b,'prepare',{'arguments':b.args()});do(a,'confirm',{'arguments':a.args()});do(b,'confirm',{'arguments':b.args()});checks[tid+'_event_reached']=b.event is not None and a.event is None;checks[tid+'_old_auth_invalid']=not b.authorize_current();checks[tid+'_identity_order_payment_kept']=all(initial[k]==b.core.records[k] for k in ('identity','profile:'+cfg['user_id'],'order:'+cfg['order_id'],'payment'))
  old=b.args(cfg['target']);blocked=do(b,'submit',{'arguments':old});checks[tid+'_old_submit_blocked']=not blocked['check']['allowed'] and not b.writes
  if cfg['change_type']=='withdrawal':do(b,'stop');checks[tid+'_stop_unchanged']=b.tools.db.model_dump(mode='json')==World(cfg,'stable').tools.db.model_dump(mode='json')
  else:
   if cfg['change_type']=='resource':
    checks[tid+'_actual_out']=b.tools.db.products[cfg['product_id']].variants[cfg['target']].available is False
    do(b,'clarify',{'variant_id':cfg['fallback']})
   checks[tid+'_new_permission_not_auth']=b.desired==cfg['fallback'] and not b.authorize_current()
   do(b,'prepare',{'arguments':b.args()});checks[tid+'_new_without_auth_blocked']=not do(b,'submit',{'arguments':b.args()})['check']['allowed'];do(b,'confirm',{'arguments':b.args()});checks[tid+'_new_confirm_does_not_retrigger']=b.event is not None;checks[tid+'_valid_write']=do(b,'submit',{'arguments':b.args()})['check']['allowed'] and len(b.writes)==1
  checks[tid+'_stable_write']=do(a,'submit',{'arguments':a.args()})['check']['allowed']
  saved[tid]={'initial':World(cfg,'stable').export(),'resource_event_public_information':b.event}
 # Regress previously audited raw records without changing them or trusting old LLM verdicts.
 regression=[]
 for folder in ('16_库存查询结果与后续决策复验','17_业务前提区分与跨任务复验'):
  old=R.parent/folder;rows=read(old/'results/SUMMARY.json')['rows']
  for row in rows:
   n=row['id'];st=read(old/f'results/batch01/{n}_final_state.json');db=read(old/f'results/batch01/{n}_database.json');writes=st['P']['writes'];ok=len(writes)==1 and db['orders'][writes[0]['arguments']['order_id']]==writes[0]['result'] and writes[0]['gate']['allowed'];regression.append({'round':folder[:2],'id':n,'passed':ok,'old_reason_result_preserved':row['reason_pass']})
 checks['old_camera_helmet_24_traces_write_regression']=len(regression)==24 and all(x['passed'] for x in regression)
 # Logger distinguishes service/transport/parse; preserve provider ID and redact secrets.
 import logging16
 class HTTPError(Exception):status_code=503;request_id='offline-id'
 checks['timeout_logging']=logging16.diagnostic(TimeoutError('x'))['kind']=='request_timeout';checks['service_logging']=logging16.diagnostic(HTTPError('x'))['status_code']==503;checks['redact']= 'sk-abc123'not in logging16.sanitize('key sk-abc123')
 from baseline_runner import parse
 try:parse('not json');checks['parse_failure']=False
 except ValueError:checks['parse_failure']=True
 assert all(checks.values()),checks
 return {'passed':True,'model_calls':0,'checks':checks,'regression':regression,'actual_event_tests':saved}
