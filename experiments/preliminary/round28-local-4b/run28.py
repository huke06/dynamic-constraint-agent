"""Gate, freeze, and run the Round 28 local paired comparison."""

import argparse
from datetime import datetime
import importlib.metadata
import json
from pathlib import Path
import subprocess

from runtime28 import ROUND, PREVIOUS, installed, prep, backends, authorize_question, shared, signed, sim

LOCAL = prep.WORKSPACE / "results"
OLD = LOCAL / "round27-formal"
OUT = LOCAL / "round28-local-4b"
CONFIG = ROUND / "CONFIG.json"
TASKS = prep.ROUND26 / "configs/TASKS.json"


def freeze(out, phase, plan, extra=()):
    files = [Path(__file__), ROUND / "runtime28.py", CONFIG, prep.GGUF, prep.SERVER,
             prep.SERVER.with_name("ggml-cuda.dll"), TASKS, prep.ROUND26 / "configs/FREEZE.json",
             prep.ROUND26 / "versions/statefix3/FREEZE.json", *extra]
    files += [PREVIOUS / name for name in ("prepare27.py", "run27.py", "simulator27.py", "recheck27.py", "recheck_amount27.py")]
    settings = prep.read_json(CONFIG)
    assert settings["agent_model"] == prep.MODEL and settings["context"] == prep.CONTEXT
    record = {"created": datetime.now().astimezone().isoformat(), "phase": phase, "plan": plan,
              "settings": settings, "budget": {k: v for k, v in prep.read_json(prep.ROUND26 / "configs/MODEL_BUDGET.json").items() if k != "model"},
              "source_commit": subprocess.check_output(["git", "-C", prep.REPO, "rev-parse", "HEAD"], text=True).strip(),
              "tau2_commit": prep.TAU2_COMMIT,
              "packages": {k: importlib.metadata.version(k) for k in ("openai", "httpx", "pydantic", "litellm")},
              "sha256": {str(f): prep.file_hash(f) for f in files}}
    prep.write_json(out / "FREEZE.json", record)


def withdrawal_regression(repair):
    core, runner = repair.c, repair.r
    trace = prep.read_json(OLD / "A_B_04/A_R_89_r1_framework_trace.json")
    failed = [step for step in trace if step.get("rejection_reason") == "invalid evidence source"]
    assert failed and failed[0]["model_original_choice"]["evidence_refs"] == [len(failed[0]["before"]["history"])]
    world = runner.snapshot(failed[0]["before"]["cfg"], None, "framework")
    for field in ("history", "parsed_history", "pending", "withdrawn"):
        setattr(world, field, failed[0]["before"][field])
    before = world.export()["database"]
    decision = runner.return_dispatch(world)
    assert decision.route == "program" and decision.work["evidence_refs"] == [len(world.history) - 1]
    feedback = runner.return_execute(world, decision.work, None, [])
    assert feedback["allowed"] and world.terminal_reason == "withdrawal_acknowledged" and world.export()["database"] == before and not world.writes
    cfg = prep.read_json(prep.ROUND26 / "configs/tasks/R_RDB01/case.json")
    active = runner.snapshot(cfg, None, "framework")
    method = cfg["event"]["payment_method_id"]
    ref = len(active.history)
    quote = f"Change the refund method to {method}. Old approval is withdrawn; ask for new approval."
    active.history.append({"role": "user", "content": quote})
    active.pending = [ref]

    class Fixture:
        def json(self, *args, **kwargs):
            return {"processed_refs": [ref], "updates": [{"source_ref": ref, "quote": quote, "kind": "refund_permission", "payment_method_id": method},
                    {"source_ref": ref, "quote": quote, "kind": "authorization_withdrawal"}]}

    active.interpret(Fixture(), [])
    assert not active.withdrawn and active.payment == method and not active.current_auth()
    assert (runner.return_dispatch(active).work or {}).get("work_type") != "stop"
    assert runner.return_dispatch(active).route == "program"
    return {"original_r89_history_length": len(failed[0]["before"]["history"]), "original_bad_refs": failed[0]["model_original_choice"]["evidence_refs"],
            "accepted_ref": decision.work["evidence_refs"][0], "terminal_database_unchanged": True, "authorization_only_continues": True}


def negative_fixtures(repair, out):
    fixtures = [
        ("partial", "Do you approve only the first item of the complete return?", "partial_confirmation"),
        ("conditional", "Would you approve this whole return if there were no fees?", "conditional_or_withheld_confirmation"),
        ("amount_check", "Can you confirm only the refund amount?", "amount_inquiry_only"),
        ("amount_question", "What is the total refund amount?", "no_current_authorization_question"),
        ("whole", "Do you approve this complete return?", None),
    ]
    core = repair.c
    results = []
    for name, text, expected in fixtures:
        extraction = {"kind": "proposal", "asks": True, "question_quote": text}
        actual = authorize_question(text, extraction, core.contains)
        assert actual == expected, (name, actual)
        results.append({"case": name, "program_guard": actual})
    replay = out / "negative_live"
    replay.mkdir()
    with prep.server(replay), backends.simulator(repair, replay) as model:
        for row, (_, question, expected) in zip(results, fixtures):
            utterance = "The complete return covers item 1234567890 with refund $25.00 to paypal_111. " + question
            payload = {"business": "return", "actual_assistant": utterance, "public_order_id": "#REPLAY28", "public_item_identities": [{"item_id": "1234567890"}], "recent_actual_user_messages": []}
            msgs = [{"role": "system", "content": core.EXTRACT}, {"role": "user", "content": json.dumps(payload)}]
            value = model.extract(msgs, row["case"], "authorization_guard_replay")
            row["live_kind"] = value["kind"]
            assert (value["kind"] == "proposal") == (expected is None), (row, value)
    return results


def gate(repair, out):
    prep.offline_checks(repair, out)
    historic = shared.issue_replay(OLD / "A_B_04", out, repair.c)
    amount = signed.former_failure_probe(OLD / "targeted_recheck01", repair.c)
    withdrawal = withdrawal_regression(repair)
    generic = generic_replays(repair.c)
    assert backends.replay(repair, out), "Round 27 replay regression"
    negative = negative_fixtures(repair, out)
    pilot_dir = out / "pilot"
    pilot_dir.mkdir()
    with backends.backends(repair, pilot_dir) as transport:
        native = prep.native_tool_probe(repair, transport)
        assert all(native.values()), native
        prep.pilot(repair, transport, pilot_dir)
    pilot = prep.read_json(pilot_dir / "OUTCOMES.json")
    assert len(pilot) == 4 and all(row["correct"] and row["event_triggered"] for row in pilot)
    prep.write_json(out / "GATE.json", {"passed": True, "historical_replays": historic,
                    "signed_amount_probe": amount, "withdrawal": withdrawal, "authorization_replays": negative, "generic_replays": generic,
                    "native": native, "pilot": [{k: r[k] for k in ("id", "correct", "event_triggered")} for r in pilot]})


def generic_replays(core):
    choices = {"business": "return", "actual_assistant": "Which refund method do you accept?\n1. Return to original payment: paypal_110\n2. Refund to gift_card_120 is not available."}
    result = sim.bind_direct_question(choices, {"kind": "refund_permission", "asks": True, "question_quote": "Which refund method do you accept?", "topic": "refund_policy", "active_offers": []})
    assert result["kind"] == "refund_permission" and [e["payment_method_id"] for e in result["active_offers"]] == ["paypal_110"]
    choices = {"business": "exchange", "actual_assistant": "Available replacement variants:\n- 1111111111: available\n- 2222222222: unavailable\n\nPlease specify which SKU you prefer."}
    result = shared.literal_list_choice(choices)
    assert result["kind"] == "spec_permission" and [e["variant_id"] for e in result["active_offers"]] == ["1111111111"]
    question = "Do you approve the complete exchange?"
    utterance = "Combined new-minus-old difference: $129.50 - $111.00 = +$18.50\n" + question
    result = sim.bind_direct_question({"business": "exchange", "actual_assistant": utterance}, {"kind": "proposal", "asks": True, "question_quote": question, "amount": -18.5, "topic": "none", "active_offers": []})
    assert result["amount"] == 18.5
    result = sim.bind_direct_question({"business": "return", "actual_assistant": "No write operations will be performed. Can I assist you with anything else?"}, {"kind": "other", "asks": False, "question_quote": "", "topic": "none", "active_offers": []})
    assert result["kind"] == "stop"
    text = "Would you confirm this complete return only if there are no fees?"
    clipped = "Would you confirm this complete return"
    assert authorize_question(text, {"kind": "proposal", "asks": True, "question_quote": clipped}, core.contains) == "conditional_or_withheld_confirmation"
    return {"refund_option_not_amount": True, "only_available_replacement": True, "positive_signed_whole_delta": True, "courtesy_close": True, "clipped_condition_denied": True}


def main_runs(repair, out, gate_path):
    assert prep.read_json(gate_path / "GATE.json")["passed"]
    tasks = prep.read_json(TASKS)
    plan = prep.formal_plan(tasks, [])["main"]
    assert len(plan) == 40
    freeze(out, "A_main", plan, (gate_path / "GATE.json",))
    rows = []
    with backends.backends(repair, out) as transport:
        for entry in plan:
            case = prep.read_json(TASKS.parent / "tasks" / entry["task"] / "case.json")
            rows.append(repair.r.rollout(out, entry["run"], case, transport, entry["group"]))
            prep.write_json(out / "OUTCOMES.json", rows)
            print(f"Round 28 A {len(rows)}/40", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("gate", "main"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--gate", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    repair = prep.prepare_sources()
    with installed(repair):
        if args.phase == "gate":
            gate(repair, out)
        else:
            main_runs(repair, out, args.gate.resolve())
