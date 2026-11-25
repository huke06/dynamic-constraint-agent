"""Regression tests for adding on-demand dispatch to the frozen v2 framework."""

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
runner_path = ROOT / "experiments/preliminary/round23-framework-loop/versions/v2/run23.py"
spec = importlib.util.spec_from_file_location("round23_fixture", runner_path)
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)

from dynamic_constraint_agent_runtime import choose_dispatch
from dynamic_constraint_agent_v2.evaluation import outcome
from dynamic_constraint_agent_v2.execution import execute
from dynamic_constraint_agent_v2.state_model import BusinessState


class UnexpectedAPI:
    def json(self, *args, **kwargs):
        raise AssertionError("A deterministic execution step called the API")


class DispatchRegression(unittest.TestCase):
    def execute_program_step(self, world, kind):
        dispatch = choose_dispatch(world)
        self.assertEqual(dispatch.route, "program")
        self.assertEqual(dispatch.work["work_type"], kind)
        result = execute(world, dispatch.work, UnexpectedAPI(), [])
        self.assertTrue(result["allowed"], result)
        return result

    def test_stable_plan_progresses_with_only_user_reply_semantics(self):
        world = fixtures.snapshot("93", "feasible")
        self.execute_program_step(world, "prepare")
        self.execute_program_step(world, "confirm")
        self.assertEqual(choose_dispatch(world).route, "state_semantics")
        fixtures.fixture_parse(world)
        self.execute_program_step(world, "submit")
        self.assertTrue(outcome(world.export())["correct_registered"])
        self.assertEqual(choose_dispatch(world).route, "finished")

    def test_conflict_requires_a_decision_model(self):
        world = fixtures.snapshot("93", "conflict")
        self.assertEqual(choose_dispatch(world).route, "decision_model")
        self.assertGreaterEqual(len(world.comparison()["negotiable"]), 2)
        self.assertFalse(world.current_auth())

    def test_changed_request_requires_latest_semantics_and_new_approval(self):
        world = fixtures.snapshot("29", "dynamic")
        self.execute_program_step(world, "prepare")
        self.execute_program_step(world, "confirm")
        self.assertIsNotNone(world.change)
        self.assertEqual(choose_dispatch(world).route, "state_semantics")
        fixtures.fixture_parse(world)
        self.assertEqual(world.targets[world.cfg["scope"][0]], world.cfg["changed_target"])
        self.assertFalse(world.current_auth())
        self.execute_program_step(world, "prepare")
        self.execute_program_step(world, "confirm")
        fixtures.fixture_parse(world)
        self.execute_program_step(world, "submit")
        self.assertTrue(outcome(world.export())["correct_registered"])

    def test_withdrawn_approval_does_not_authorize_an_automatic_write(self):
        world = fixtures.snapshot("102", "withdrawn")
        self.assertTrue(world.current_plan())
        self.assertFalse(world.current_auth())
        self.assertEqual(choose_dispatch(world).route, "decision_model")

    def test_only_missing_catalogue_is_queried(self):
        config = fixtures.read(fixtures.EXP / "configs/tasks/93/case.json")
        config["initial_catalogues"] = False
        world = BusinessState(config, "stable", None)
        world.initialize_constraints()
        self.execute_program_step(world, "query")
        self.assertEqual(choose_dispatch(world).work["work_type"], "prepare")

    def test_observed_stock_change_returns_to_decision_model(self):
        root = ROOT / "experiments/preliminary/round24-official-and-trajectory/versions/a2"
        config = fixtures.read(root / "configs/A/23/case.json")
        world = BusinessState(config, "changed", None)
        world.initialize_constraints()
        self.execute_program_step(world, "prepare")
        self.execute_program_step(world, "confirm")
        fixtures.fixture_parse(world)
        self.assertFalse(world.stock(world.cfg["scope"][0]))
        self.assertEqual(choose_dispatch(world).route, "decision_model")
        self.assertFalse(world.current_auth())

    def test_stepwise_control_and_rejected_program_fallback(self):
        world = fixtures.snapshot("93", "feasible")
        self.assertEqual(choose_dispatch(world, on_demand=False).route, "decision_model")
        self.assertEqual(choose_dispatch(world, program_retry_allowed=False).route, "decision_model")
        world.needs_review = True
        self.assertEqual(choose_dispatch(world).route, "decision_model")


if __name__ == "__main__":
    unittest.main()
