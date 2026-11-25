from copy import deepcopy
def check():
 import experiment14 as e
 from engine import Case
 responses=e.read(e.ROOT/'configs/private_responses.json');c=e.base.load_start()
 assert c.goal['alternative_permission']=='unknown' and c.conditional_permission['sat']=='未满足'
 text,data=e.interface14.clarification(c);assert "don't accept" not in text and data['out_of_stock']['available'] is False
 e.base.recovery13.begin(c);assert not c.completed('current_reply_clarification_resolved')
 def reply(c,key,kind,grant=False):
  e.base.recovery13.begin(c);ar=len(c.history);c.history.append({'role':'assistant','content':e.interface14.clarification(c)[0]});ur=len(c.history);q=responses[key]['reply'];c.history.append({'role':'user','content':q})
  p={'permission_update':{'kind':'grant','variant_id':'6384525445','source_ref':ur,'source_quote':q} if grant else {'kind':'none'},'change':{'present':False},'authorization':{'approved':False},'clarification_resolution':{'kind':kind,'source_ref':ur,'source_quote':q}}
  c.apply_user(p,ar,ur)
 reply(c,'ambiguous_first','information_unclear',True)
 assert c.goal['alternative_permission']=='unknown' and not c.plan and not c.completed('current_reply_clarification_resolved')
 assert not next(w for w in c.candidates() if w['work_id']=='prepare')['ready']
 assert not next(w for w in c.candidates() if w['work_id']=='submit')['ready']
 reply(c,'ambiguous_followup','new_permission',True);assert c.goal['alternative_permission']=='6384525445' and c.completed('current_reply_clarification_resolved') and not c.confirmations
 c2=e.base.load_start();reply(c2,'reject','explicit_rejection');assert c2.user_declined and not c2.writes and not c2.candidates()
 c3=e.base.load_start();reply(c3,'accept','new_permission',True);assert not c3.confirmations
 w=next(w for w in c3.candidates() if w['work_id']=='prepare');db=e.read(e.HERE/'scenarios/initial_database.json');tools=e.b.RetailTools(e.b.RetailDB.model_validate(deepcopy(db)));args={'order_id':c3.core.order_id,'item_ids':[c3.changed_item],'new_item_ids':['6384525445'],'payment_method_id':c3.core.payment};c3.deterministic(c3.instruction(w,{'arguments':args}),tools)
 assert not next(w for w in c3.candidates() if w['work_id']=='submit')['ready']
 # Controlled replies cannot be emitted before an actual work/question.
 import io
 mock=e.interface14.Client.__new__(e.interface14.Client);mock.responses=responses;mock.private_branches={'probe':'ambiguous'};mock.counts={};mock.pending={};mock.events=[];mock.controlled_stream=io.StringIO();mock.grounded=io.StringIO()
 try:mock.ask('probe','environment_user','customer',[]);raise AssertionError('early user reply')
 except KeyError:pass
 import json
 probe=e.base.load_start();messages=[{'role':'system','content':''},{'role':'user','content':json.dumps({'u':{'z':{'work_id':'clarify'}}})}]
 text=mock.ask('probe','agent','worker',messages,case=probe);assert mock.counts=={}
 probe.history.append({'role':'assistant','content':text});first=mock.ask('probe','environment_user','customer',[]);assert first==responses['ambiguous_first']
 mock.pending['probe']=('confirm',probe)
 try:mock.ask('probe','environment_user','customer',[]);raise AssertionError('confirmation before follow-up')
 except AssertionError as ex:assert str(ex)!='confirmation before follow-up'
 probe.clarification_outcomes=[{'outcome':'information_unclear'}];probe.history.append({'role':'user','content':first['reply']})
 text=mock.ask('probe','agent','worker',messages,case=probe);probe.history.append({'role':'assistant','content':text});second=mock.ask('probe','environment_user','customer',[]);assert second==responses['ambiguous_followup']
 assert e.base.load_start().state()==e.base.load_start().state()
 return {'passed':True,'model_calls':0,'tests':['old false permission never activated','neutral clarification drawn from true tool records','ambiguous semantic outcome suppresses contradictory grant and cannot enable prepare/submit','explicit rejection terminates with no write','acceptance needs independent full proposal authorization','follow-up explicit acceptance can activate permission','same shared snapshot for every branch','user reply function triggered only by actual clarify/confirm; private branches remain outside Case and Agent payload']}
