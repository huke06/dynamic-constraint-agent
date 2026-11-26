"""Round 27 simulator replay, pilot, frozen main comparison and continuations."""

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import subprocess

import prepare27 as prep
from simulator27 import MODEL as SIM_MODEL, Simulator


@contextmanager
def simulator(repair, out):
    with (out / "simulator_calls.jsonl").open("x", encoding="utf-8") as log:
        model = Simulator(log, repair.c.contains, prep.BASE_URL)
        try:
            yield model
        finally:
            model.close()


@contextmanager
def backends(repair, out):
    with prep.server(out), prep.local_transport(repair, out) as transport, simulator(repair, out) as model:
        local_json = transport.json

        def routed(messages, role, trigger, max_tokens=1700):
            if role == "simulator":
                return model.extract(messages, transport.branch, trigger, max_tokens)
            return local_json(messages, role, trigger, max_tokens)

        transport.json = routed
        yield transport


def replay(repair, out):
    old = prep.WORKSPACE / "results/round27-preflight/pilot01/model_calls.jsonl"
    rows = [json.loads(line) for line in old.read_text(encoding="utf-8").splitlines()]
    cases = []
    for group, phrase, variants in (
        ("official", "Which alternative variant would you like to use instead?",
         {"7160999700", "8759627937", "8964750292", "9956648681"}),
        ("framework", "Do you accept SKU 7160999700", {"7160999700"}),
    ):
        call = next(row for row in rows if row["branch"] == f"pilot_exchange_resource_{group}"
                    and row["role"] == "simulator" and phrase in row["messages"][1]["content"])
        cases.append((group + "_original", call["messages"], "spec_permission", True, variants, "none"))
    fixtures = (
        ("cap_question", "Does the negative cap mean a minimum refund or a maximum refund?", "exchange", "constraint_question", True, set(), "cap_direction"),
        ("internal_narration", "The original replacement is unavailable. I need to ask the user whether to pick a different variant.", "exchange", "other", False, set(), "none"),
        ("rejected_sku", "SKU 2698416822 is rejected and not allowed. The available replacement is SKU 1240311797. Do you accept SKU 1240311797 as the new specification?", "exchange", "spec_permission", True, {"1240311797"}, "none"),
        ("sku_with_cap", "Do you accept SKU 1240311797 as the replacement, at a difference of $18.50 within your maximum cap?", "exchange", "spec_permission", True, {"1240311797"}, "none"),
        ("refund_route", "The existing gift card gift_card_111 is permitted. Do you accept refund to gift_card_111? I will ask separately for final approval.", "return", "refund_permission", True, {"gift_card_111"}, "none"),
        ("complete_approval", "Return item 1234567890 for a total refund of $25.00 to your original payment method credit_card_111. Do you approve this complete return?", "return", "proposal", True, set(), "none"),
        ("natural_return_confirmation", "Do you confirm you want to proceed with returning item 1234567890 from order #TEST27 with a refund of $25.00 to paypal_111? Please respond with yes to confirm.", "return", "proposal", True, set(), "none"),
        ("explicit_stop", "Your entire return request has been withdrawn. I will not submit the return and the order will remain unchanged.", "return", "stop", False, set(), "none"),
    )
    for name, utterance, business, kind, asks, variants, topic in fixtures:
        payload = {"business": business, "actual_assistant": utterance, "public_order_id": "#TEST27",
                   "public_item_identities": [{"item_id": "1234567890"}], "recent_actual_user_messages": []}
        messages = [{"role": "system", "content": repair.c.EXTRACT}, {"role": "user", "content": json.dumps(payload)}]
        cases.append((name, messages, kind, asks, variants, topic))
    scores = []
    replay_logs = out / "replay"
    replay_logs.mkdir()
    with prep.server(replay_logs), simulator(repair, replay_logs) as model:
        for name, messages, kind, asks, variants, topic in cases:
            try:
                actual = model.extract(messages, name, "annotated_replay")
                offered = {offer.get("variant_id") or offer.get("payment_method_id") for offer in actual["active_offers"]}
                checks = {"kind": actual["kind"] == kind, "asks": actual["asks"] == asks,
                          "active_options": offered == variants, "topic": actual["topic"] == topic}
                scores.append({"case": name, "checks": checks, "passed": all(checks.values()), "extraction": actual})
            except RuntimeError as error:
                scores.append({"case": name, "passed": False, "error": str(error)})
            prep.write_json(out / "REPLAY.json", scores)
    print("Replay:", [(row["case"], row["passed"]) for row in scores], flush=True)
    return all(row["passed"] for row in scores)


def manifest():
    cfg = prep.ROUND26 / "configs"
    tasks = prep.read_json(cfg / "TASKS.json")
    checkpoints = prep.read_json(cfg / "DPO_CHECKPOINTS.json")
    return prep.formal_plan(tasks, checkpoints), checkpoints


def freeze(out, gate, plan):
    fingerprints = [Path(__file__), prep.ROUND / "prepare27.py", prep.ROUND / "simulator27.py",
                    prep.ROUND / "PROTOCOL.md", prep.ROUND26 / "configs/FREEZE.json",
                    prep.ROUND26 / "versions/statefix3/FREEZE.json", prep.GGUF, prep.SERVER,
                    prep.SERVER.with_name("ggml-cuda.dll")]
    state = {"created": datetime.now().astimezone().isoformat(), "status": "frozen_before_first_formal_request",
             "source_commit": subprocess.check_output(["git", "-C", prep.REPO, "rev-parse", "HEAD"], text=True).strip(),
             "hashes_sha256": {str(p): prep.file_hash(p) for p in fingerprints}, "plan": plan,
             "local": {"model": prep.MODEL, "base_model_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
                       "llama_cpp": "b10917 CUDA 13.3", "context": prep.CONTEXT, "parallel_slots": 1,
                       "temperature": 0, "thinking": False, "format_constraint": None},
             "simulator": {"model": SIM_MODEL, "backend": "llama.cpp localhost", "literal_offer_binding": True,
                           "temperature": 0, "thinking": False, "format": "json_object", "retry_limit": 1},
             "upstream_tau2": prep.TAU2_COMMIT, "preflight": str(gate),
             "business_budget": {k: v for k, v in prep.read_json(prep.ROUND26 / "configs/MODEL_BUDGET.json").items() if k != "model"}}
    prep.write_json(out / "FREEZE.json", state)


def formal(repair, out, gate):
    if not all(row["passed"] for row in prep.read_json(gate / "REPLAY.json")):
        raise RuntimeError("Annotated replay failed")
    if not all(prep.read_json(gate / "NATIVE_PROBE.json").values()):
        raise RuntimeError("Native tool probe failed")
    pilot = prep.read_json(gate / "OUTCOMES.json")
    if len(pilot) != 4 or not all(row["event_triggered"] for row in pilot):
        raise RuntimeError("Pilot did not reproduce the two public changes for both groups")
    plan, states = manifest()
    if len(plan["main"]) != 40 or len(plan["continuations"]) != 12:
        raise RuntimeError("Unexpected formal counts")
    plan["status"] = "frozen"
    freeze(out, gate, plan)
    checkpoints = {state["id"]: state for state in states}
    with backends(repair, out) as transport:
        rows = []
        for entry in plan["main"] + plan["continuations"]:
            if "task" in entry:
                task = prep.read_json(prep.ROUND26 / "configs/tasks" / entry["task"] / "case.json")
                row = repair.r.rollout(out, entry["run"], task, transport, entry["group"])
            else:
                state = checkpoints[entry["checkpoint"]]
                row = repair.r.rollout(out, entry["run"], deepcopy(state["cfg"]), transport,
                                       first=entry["forced_first_work"], first_params=state["clarify_parameters"])
            rows.append(row)
            prep.write_json(out / "OUTCOMES.json", rows)
            print(f"Formal {len(rows)}/52", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("replay", "pilot", "formal"))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--gate", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    repair = prep.prepare_sources()
    if args.phase == "formal":
        formal(repair, out, args.gate.resolve())
        return
    prep.offline_checks(repair, out)
    if not replay(repair, out):
        raise SystemExit("Annotated replay did not pass")
    if args.phase == "pilot":
        with backends(repair, out) as transport:
            probe = prep.native_tool_probe(repair, transport)
            prep.write_json(out / "NATIVE_PROBE.json", probe)
            if not all(probe.values()):
                raise SystemExit("Native probe did not pass")
            prep.pilot(repair, transport, out)


if __name__ == "__main__":
    main()
