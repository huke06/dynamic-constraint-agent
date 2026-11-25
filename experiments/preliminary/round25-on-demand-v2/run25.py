"""Compare stepwise decisions with on-demand dispatch in the same v2 framework."""

import argparse
from collections import Counter
from copy import deepcopy
import importlib.util
from pathlib import Path
import sys
import time


EXP = Path(__file__).resolve().parent
ROOT = EXP.parents[2]
A2 = ROOT / "experiments/preliminary/round24-official-and-trajectory/versions/a2"
spec = importlib.util.spec_from_file_location("round24_a2", A2 / "src/run24a2.py")
a2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a2)

from dynamic_constraint_agent_runtime import choose_dispatch


CASES = {
    "80": (A2 / "configs/A/80/case.json", "stable", None),
    "23": (A2 / "configs/A/23/case.json", "changed", None),
    "29": (A2 / "configs/A/29/case.json", "changed", None),
    "26": (a2.V / "configs/tasks/26/case.json", "stable", "conflict"),
}


def rollout(output, run_id, case, version, cap, mode, transport):
    world = a2.snapshot(case, version, transport, "framework", cap)
    transport.world = world
    transport.branch = run_id
    trace = []
    rejected = Counter()
    program_retry_allowed = True
    error = None
    start = time.perf_counter()
    a2.save(output / f"{run_id}_start.json", world.export())
    try:
        for _ in range(35):
            if world.writes or world.stopped:
                break
            if min(world.remaining_budget.values()) <= 0:
                error = "budget_exhausted"
                break
            dispatch = choose_dispatch(
                world, on_demand=mode == "on_demand",
                program_retry_allowed=program_retry_allowed,
            )
            if dispatch.route == "state_semantics":
                a2.semantic(world, transport, trace)
                program_retry_allowed = not world.pending and not world.needs_review
                a2.save(output / f"{run_id}_trace.json", trace)
                continue

            visible = deepcopy(world.model_state(True))
            work = dispatch.work if dispatch.route == "program" else a2.choose(world, transport, "candidate")
            trace.append({
                "module": "work_selection",
                "source": dispatch.route,
                "dispatch_reason": dispatch.reason,
                "choice": deepcopy(work),
                "visible_state": visible,
            })
            feedback = a2.execute(world, work, transport, trace)
            if feedback["allowed"]:
                program_retry_allowed = True
            else:
                if dispatch.route == "program":
                    program_retry_allowed = False
                key = a2.packed({
                    "type": work.get("work_type"), "object": work.get("object"),
                    "parameters": work.get("parameters", {}), "reason": feedback["reason"],
                })
                rejected[key] += 1
                if rejected[key] >= 3:
                    error = "repeated_same_rejection"
                    break
            if world.event_export:
                trace.append({"module": "public_change", "event": world.event_export})
                world.event_export = None
            a2.save(output / f"{run_id}_trace.json", trace)
        if not world.writes and not error:
            error = "stopped_without_write" if world.stopped else "loop_limit"
    except Exception as exc:
        from logging16 import sanitize
        error = type(exc).__name__ + ": " + sanitize(exc, getattr(transport.sdk, "secret", None))
        trace.append({"module": "failure", "error": error})
    final = world.export()
    a2.save(output / f"{run_id}_trace.json", trace)
    a2.save(output / f"{run_id}_final.json", final)
    a2.save(output / f"{run_id}_simulator.json", world.sim_records)
    result = {
        "id": run_id, "task": case["task_id"], "mode": mode, "error": error,
        "event_triggered": bool(world.change),
        "program_steps": sum(
            event.get("source") == "program" for event in trace
            if event["module"] == "work_selection"
        ),
        "seconds": time.perf_counter() - start, **a2.outcome(final),
    }
    print(result, flush=True)
    return result


def run(batch_name):
    if not batch_name.isascii() or not batch_name.replace("_", "").replace("-", "").isalnum():
        raise SystemExit("Use an ASCII batch name containing only letters, digits, _ or -.")
    a2.verify()
    output = EXP / "results" / batch_name
    output.mkdir(parents=True, exist_ok=False)
    sched = ROOT / "src/dynamic_constraint_agent_runtime.py"
    a2.save(output / "started.json", {
        "runner_sha256": a2.sha(Path(__file__)), "scheduler_sha256": a2.sha(sched),
        "cases": {tid: {"source": str(path.relative_to(ROOT)), "version": ver,
                         "cap_state": cap_state, "sha256": a2.sha(path)}
                  for tid, (path, ver, cap_state) in CASES.items()},
        "round23_v2_freeze_sha256": a2.sha(a2.V / "configs/FREEZE.json"),
        "round24_a2_freeze_sha256": a2.sha(A2 / "configs/FREEZE.json"),
        "model_alias": a2.b.MODEL, "repetitions": 2,
    })
    transport = a2.Transport(output)
    outcomes = []
    try:
        for tid, (path, version, cap_state) in CASES.items():
            case = a2.read(path)
            cap = case["caps"][cap_state] if cap_state else None
            for rep, modes in ((1, ("stepwise", "on_demand")), (2, ("on_demand", "stepwise"))):
                for mode in modes:
                    outcomes.append(rollout(output, f"t{tid}_r{rep}_{mode}", case, version, cap, mode, transport))
                    a2.save(output / "OUTCOMES.json", outcomes)
    finally:
        transport.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--run", metavar="NEW_BATCH")
    args = parser.parse_args()
    if args.list:
        a2.verify()
        for task in CASES:
            print(task, CASES[task][1], CASES[task][2])
        print(f"{len(CASES)} tasks, {len(CASES)*4} paired-mode trajectories.")
    else:
        run(args.run)
