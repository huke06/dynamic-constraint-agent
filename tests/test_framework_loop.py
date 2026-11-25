import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('run23',ROOT/'experiments/preliminary/round23-framework-loop/run23.py');run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
from dynamic_constraint_agent.execution import execute

class FakeSemantic:
 def json(self,messages,role,trigger):
  import json
  d=json.loads(messages[-1]['content'])
  if trigger=='analyze_tradeoffs':return {'comparison_scope':'exact vs negotiable','tradeoffs':[],'analysis':'Empty exact feasibility is a valid finding, not a parsing failure.'}
  v=d['offered_variant']['item_id'];return {'offered_variant_id':v,'question':f'Variant {v} is observed available. Will you accept this alternative?'}

class LoopRegression(unittest.TestCase):
 def test_empty_analysis_is_success_and_not_permission(self):
  w=run.snapshot('93','conflict');out=execute(w,run.job(w,'analyze'),FakeSemantic(),[])
  self.assertTrue(out['allowed']);self.assertEqual(out['result']['facts']['exact_feasible'],[]);self.assertTrue(out['result']['facts']['negotiable']);self.assertEqual(w.targets,w.cfg['targets']);self.assertFalse(w.current_auth());self.assertEqual(w.model_state()['analysis_feedback'][-1]['facts']['status'],'no_exact_match')
 def test_both_first_works_feed_valid_feedback_and_finish(self):
  for state in('conflict','feasible'):
   for first in('analyze','clarify'):
    w=run.snapshot('93',state);trace=[];offer=w.comparison()['negotiable'][0]['variant_id'];d=run.job(w,first,offer if first=='clarify'else None);self.assertTrue(execute(w,d,FakeSemantic(),trace)['allowed'])
    if first=='analyze':self.assertTrue(execute(w,run.job(w,'clarify',offer),FakeSemantic(),trace)['allowed'])
    ref=w.pending[0];run.fixture_parse(w);m=w.model_state()['objects'][0];self.assertEqual(m['purchased']['variant_id'],'2216662955');self.assertEqual(m['CURRENT_EFFECTIVE_SPECIFICATION']['variant_id'],offer);self.assertEqual(m['CURRENT_EFFECTIVE_SPECIFICATION']['source_ref'],ref);self.assertFalse(m['initial_request_history_only']['active']);self.assertFalse(w.current_auth())
    self.assertFalse(execute(w,run.job(w,'submit'),FakeSemantic(),trace)['allowed']);self.assertTrue(execute(w,run.job(w,'prepare'),FakeSemantic(),trace)['allowed']);self.assertTrue(execute(w,run.job(w,'confirm'),FakeSemantic(),trace)['allowed']);run.fixture_parse(w);self.assertTrue(execute(w,run.job(w,'submit'),FakeSemantic(),trace)['allowed']);self.assertEqual(len(w.writes),1);self.assertEqual(w.writes[0]['arguments']['new_item_ids'],[offer])
 def test_explicit_stale_sku_not_silently_overridden(self):
  w=run.snapshot('93','conflict');v=w.comparison()['negotiable'][0]['variant_id'];execute(w,run.job(w,'clarify',v),FakeSemantic(),[]);run.fixture_parse(w);d=run.job(w,'prepare');d['parameters']={'new_item_id':w.cfg['targets'][w.cfg['scope'][0]]};self.assertFalse(execute(w,d,FakeSemantic(),[])['allowed']);self.assertIsNone(w.plan)
 def test_analysis_invalidated_and_current_authorization_evidenced(self):
  w=run.snapshot('93','conflict');execute(w,run.job(w,'analyze'),FakeSemantic(),[]);v=w.comparison()['negotiable'][0]['variant_id'];execute(w,run.job(w,'clarify',v),FakeSemantic(),[]);run.fixture_parse(w);self.assertEqual(w.model_state()['analysis_feedback'],[]);self.assertFalse(w.analysis_results[0]['active']);execute(w,run.job(w,'prepare'),FakeSemantic(),[]);execute(w,run.job(w,'confirm'),FakeSemantic(),[]);run.fixture_parse(w);m=w.model_state();self.assertTrue(m['authorization_evidence']['valid_for_current_plan']);self.assertTrue(m['authorization_evidence']['quoted_user_replies']);self.assertEqual(m['missing_prerequisites'],[])
 def test_only_known_order_prefix_alias_is_normalized(self):
  w=run.snapshot('93','feasible');d=run.job(w,'prepare');d['object']=d['object'].lstrip('#');tr=[];self.assertTrue(execute(w,d,FakeSemantic(),tr)['allowed']);self.assertNotEqual(tr[-1]['model_original_choice']['object'],tr[-1]['normalized_work']['object']);d['object']='W_DIFFERENT';self.assertFalse(execute(w,d,FakeSemantic(),[])['allowed'])
 def test_old_processed_source_cannot_be_applied_again(self):
  w=run.snapshot('93','conflict');v=w.comparison()['negotiable'][0]['variant_id'];execute(w,run.job(w,'clarify',v),FakeSemantic(),[]);ref=w.pending[0];run.fixture_parse(w)
  with self.assertRaises(ValueError):w.apply({'updates':[],'processed_refs':[ref]})
 def test_dynamic_change_keeps_other_evidence_and_invalidates_old_auth(self):
  w=run.snapshot('29','dynamic');execute(w,run.job(w,'prepare'),FakeSemantic(),[]);b=w.cfg['scope'][1];p=w.item(b)['product_id'];keys=('requirement:'+b,'catalog:'+p,'match:'+b,'delta:'+b,'identity','payment');before={k:w.core.records[k].copy()for k in keys};execute(w,run.job(w,'confirm'),FakeSemantic(),[]);self.assertTrue(w.change);run.fixture_parse(w);self.assertEqual(w.targets[w.cfg['scope'][0]],w.cfg['changed_target']);self.assertFalse(w.current_auth());self.assertEqual(before,{k:w.core.records[k]for k in keys});self.assertFalse(execute(w,run.job(w,'submit'),FakeSemantic(),[])['allowed'])
 def test_withdrawal_requires_new_full_authorization(self):
  w=run.snapshot('102','withdrawn');self.assertTrue(w.current_plan());self.assertFalse(w.current_auth());self.assertFalse(execute(w,run.job(w,'submit'),FakeSemantic(),[])['allowed']);execute(w,run.job(w,'confirm'),FakeSemantic(),[]);run.fixture_parse(w);self.assertTrue(w.current_auth())
 def test_independent_states_only_cap_changes_and_no_hidden_answers(self):
  for tid in('11','16'):
   a=run.snapshot(tid,'conflict');b=run.snapshot(tid,'feasible');self.assertEqual(a.core.products,b.core.products);self.assertEqual(a.targets,b.targets);self.assertFalse(a.feasible());self.assertTrue(b.feasible());self.assertGreaterEqual(len(a.comparison()['negotiable']),2)
   direct=a.model_state();candidate=a.model_state(True);candidate.pop('candidate_work');self.assertEqual(direct,candidate);self.assertNotIn('oracle',direct);self.assertNotIn('evaluation_criteria',str(direct));self.assertNotIn('future_reply',direct)

if __name__=='__main__':unittest.main()
