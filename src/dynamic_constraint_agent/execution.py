"""Module 3: work contract, actual native actions, typed feedback, state update."""
from copy import deepcopy
from exchange_core import packed
from runner20 import question,validate_job
ANALYSIS='''Facts are program-verified. Distinguish purchased object, CURRENT effective requested replacement and historical initial request. exact_feasible may be empty: that is a SUCCESSFUL finding, not a parser error. negotiable options are NOT yet permitted by user. Return JSON {"comparison_scope":"current exact requirements vs negotiable relaxations","tradeoffs":[{"variant_id":"observed negotiable ID","observation":"options changed vs CURRENT request","question":"neutral permission question"}],"analysis":"explain current conflict or feasibility; do not invent permission"}. Empty tradeoffs are allowed. Do not replace numerical program facts or claim all alternatives match current exact specification.'''
def execute(w,d,t,trace):
 before=w.export();original_choice=deepcopy(d);d=deepcopy(d);result=None;allowed=False;reason=None;native=None
 if d.get('object')==w.cfg['order_id'].lstrip('#'):d['object']=w.cfg['order_id']
 try:
  validate_job(w,d);kind=d['work_type'];i=w.cfg['scope'][0]
  if w.pending:raise ValueError('Pending actual user reply must first update current state.')
  if kind in('prepare','confirm','submit'):
   if d.get('parameters'):raise ValueError('Whole-plan work requires parameters={}; explicit stale or conflicting SKU arguments must not override current effective state.')
   for k in('variant_id','new_item_id','new_variant_id'):
    if k in d.get('parameters',{})and d['parameters'][k]!=w.targets[i]:raise ValueError('Selected SKU conflicts with latest effective permission; historical request cannot override current state.')
  if kind=='analyze':
   if d['object']!=i:raise ValueError('Analysis object must be original item ID.')
   facts=w.comparison();advice=None
   if facts['status']!='evidence_insufficient':
    advice=t.json([{'role':'system','content':ANALYSIS},{'role':'user','content':packed({'objects':w.model_state()['objects'],'constraint':w.model_state()['hard_constraint'],'verified_comparison':facts})}],'semantic','analyze_tradeoffs')
   result={'kind':'analysis_result','facts':facts,'model_advice':advice,'not_authorization':True};w.analysis_results.append(result);w.remaining_budget['operations']-=1;allowed=True
  elif kind=='clarify':
   v=d.get('parameters',{}).get('variant_id')
   if not w.feasible(v)or v==w.targets[i]:raise ValueError('Clarification requires a DIFFERENT observed feasible variant; latest current specification may already be permitted.')
   # Business facts/amount supplied by program, semantic model asks a local neutral question.
   q=question(w,t,d,trace);native=w.perform(d,q);result=native.get('result');allowed=native['allowed'];reason=native.get('rejection_reason')
  elif kind=='stop':
   if w.comparison()['negotiable']or w.feasible():raise ValueError('Feasible continuation remains; stopping requires actual refusal or exhausted alternatives.')
   native=w.perform(d);result=native['result'];allowed=native['allowed']
  else:
   if kind in('prepare','submit')and not w.feasible():raise ValueError('Cannot prepare/submit: CURRENT specification violates stock or signed whole-amount cap. Analyze or clarify a feasible alternative; diagnostic analysis is a separate successful work.')
   native=w.perform(d);result=native.get('result');allowed=native['allowed'];reason=native.get('rejection_reason')
 except (ValueError,KeyError,TypeError)as ex:reason=str(ex)
 feedback={'selected_work':original_choice,'normalized_work':deepcopy(d),'expected_order_id':w.cfg['order_id'],'allowed':allowed,'reason':reason,'result':deepcopy(result),'current_specifications':deepcopy(w.targets),'missing_prerequisites':w.model_state()['missing_prerequisites']};w.feedback.append(feedback)
 trace.append({'module':'task_execution_feedback','model_original_choice':original_choice,'normalized_work':deepcopy(d),'allowed':allowed,'rejection_reason':reason,'actual_native':native and {k:native.get(k)for k in('result','independent_submit_check')},'result':deepcopy(result),'before':before,'after':w.export(),'updated_model_state':w.model_state()});return feedback
