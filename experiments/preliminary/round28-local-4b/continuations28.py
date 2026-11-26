"""Register and run independently restorable Round 28 continuation checkpoints."""

import argparse
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from audit28 import Audit
from run28 import OUT, TASKS, freeze
from runtime28 import ROUND, backends, installed, prep


class ProbeTransport:
    def json(self, messages, role, trigger, max_tokens=1700):
        if role == "simulator":
            return {"kind": "other", "asks": False, "question_quote": "", "topic": "none", "active_offers": []}
        return {"analysis": "deterministic feasibility probe", "tradeoffs": [], "not_authorization": True}


def work(kind, object_id, params, refs, reason):
    return {"work_type": kind, "object": object_id, "parameters": params, "evidence_refs": refs,
            "expected": {"query": "obtain native evidence", "clarify": "obtain option permission; no transaction approval",
                         "confirm": "request current whole-transaction approval", "analyze": "compare observed alternatives"}[kind],
            "reason": reason}


def registration(repair, definitions):
    core, runner = repair.c, repair.r
    prior_states = {x["id"]: x for x in prep.read_json(prep.ROUND26 / "configs/DPO_CHECKPOINTS.json")}
    registered = []
    for row in definitions:
        previous = prior_states.get(row.get("prior_state"))
        cfg = deepcopy(previous["cfg"]) if previous else prep.read_json(TASKS.parent / "tasks" / row["fixture"] / "case.json")
        world = checkpoint_world(repair, runner.snapshot, cfg, None, "framework", row["state"])
        actions = {}
        if row["state"] == "missing_exchange_catalogues":
            for i, item in enumerate(cfg["scope"], 1):
                pid = world.item(item)["product_id"]
                assert world.product(item) is None
                actions[f"query_{i}"] = work("query", pid, {}, [0], "requested item requires current product catalogue and stock")
        elif row["state"] == "missing_return_evidence":
            assert not {"get_order_details", "get_user_details"}.intersection(world.observed)
            actions["query_order"] = work("query", cfg["order_id"], {"tool": "get_order_details"}, [0], "obtain native order status, items and original payment")
            actions["query_profile"] = work("query", cfg["user_id"], {"tool": "get_user_details"}, [0], "obtain native profile and observed refund routes")
        elif row["state"] == "observed_options_conflict":
            assert not world.feasible()
            for kind in ("analyze", "clarify"):
                actions[kind] = runner.forced(world, kind, previous["clarify_parameters"])
        elif row["state"] == "current_return_plan_ready":
            assert world.current_plan() and not world.current_auth()
            actions["confirm"] = work("confirm", cfg["order_id"], {}, [world.refs["get_order_details"]], "current plan is verified and requires independent approval")
            actions["refresh_order"] = work("query", cfg["order_id"], {"tool": "get_order_details"}, [world.refs["get_order_details"]], "refresh the still-observable native order before requesting approval")
        else:
            raise ValueError(row["state"])
        assert list(actions) == row["first_work_order"], row["id"]
        observed = world.model_state(True)
        initial = world.export()
        allowed = []
        for name, decision in actions.items():
            fixture = ProbeTransport()
            check = checkpoint_world(repair, runner.snapshot, cfg, fixture, "framework", row["state"])
            assert check.model_state(True) == observed and check.export() == initial
            feedback = executor(repair, cfg)(check, deepcopy(decision), fixture, [])
            if not feedback["allowed"]:
                raise RuntimeError(f"{row['id']} {name} infeasible: {feedback.get('reason')}")
            allowed.append(name)
        registered.append({**row, "cfg": cfg, "initial_visible": observed, "initial_full": initial,
                           "actions": actions, "priorities": deepcopy(previous["priorities"]) if previous else [],
                           "feasibility": allowed, "formal_first_work_model_autonomous": False})
    return registered


def executor(repair, cfg):
    return repair.r.return_execute if cfg["business"] == "return" else repair.r.exchange_execute


def checkpoint_world(repair, snapshot, cfg, transport, group, state):
    world = snapshot(cfg, transport, group)
    if state == "current_return_plan_ready":
        decision = repair.r.return_dispatch(world)
        assert decision.route == "program" and decision.work["work_type"] == "prepare"
        saved_budget = dict(world.remaining_budget)
        result = repair.r.return_execute(world, decision.work, None, [])
        assert result["allowed"]
        # This checkpoint starts after the verified existing plan, with a full common budget.
        world.remaining_budget = saved_budget
    return world


def run(repair, main, config, out):
    summary = prep.read_json(main / "SUMMARY.json")
    if summary["formal_trajectories"] != 40 or not summary["independent_scores_match"]:
        raise RuntimeError("The A batch and independent score gate must finish before B")
    records = registration(repair, prep.read_json(config)["checkpoints"])
    assert 4 <= len(records) <= 6 and len({r["base_task"] for r in records}) == len(records)
    prep.write_json(out / "REGISTERED.json", records)
    plan = []
    for row in records:
        order = row["first_work_order"]
        for repeat in (1, 2):
            for arm in (order if repeat == 1 else reversed(order)):
                plan.append({"run": f'B_{row["id"]}_r{repeat}_{arm}', "checkpoint": row["id"], "arm": arm, "repeat": repeat})
    freeze(out, "B_continuations", plan, (Path(__file__), ROUND / "audit28.py", ROUND / "samples28.py",
                                       config, out / "REGISTERED.json", main / "SUMMARY.json"))
    original_snapshot = repair.r.snapshot
    lookup = {r["id"]: r for r in records}
    outcomes = []
    with backends.backends(repair, out) as transport:
        for entry in plan:
            row = lookup[entry["checkpoint"]]

            def start(cfg, thread, group):
                world = checkpoint_world(repair, original_snapshot, cfg, thread, group, row["state"])
                assert world.model_state(True) == row["initial_visible"] and world.export() == row["initial_full"]
                return world

            def forced(world, name, params):
                return deepcopy(row["actions"][name])

            with patch.object(repair.r, "snapshot", start), patch.object(repair.r, "forced", forced):
                result = repair.r.rollout(out, entry["run"], deepcopy(row["cfg"]), transport, first=entry["arm"])
            outcomes.append(result)
            prep.write_json(out / "OUTCOMES.json", outcomes)
            print(f"Round 28 B {len(outcomes)}/{len(plan)}", flush=True)
    return Audit(out, repair.c)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main", type=Path)
    parser.add_argument("--config", type=Path, default=ROUND / "CHECKPOINTS.json")
    parser.add_argument("--out", type=Path, default=OUT / "B01")
    args = parser.parse_args()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    repair = prep.prepare_sources()
    with installed(repair):
        run(repair, args.main.resolve(), args.config.resolve(), args.out)
