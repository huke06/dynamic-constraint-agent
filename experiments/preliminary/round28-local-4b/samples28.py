"""Verify continuation ordering and export traceable, grouped learning candidates."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from audit28 import Audit
from runtime28 import prep
from report27 import accepted_decision, preference, private_keys, write_jsonl


COST_FIELDS = ("agent_attempts", "agent_input_tokens", "agent_output_tokens", "simulator_attempts", "business_execution_steps")


def technical(score):
    return any(r.endswith(("_service_errors", "_unknown_usage", "_output_limit", "_failed")) or
               any(w in r.lower() for w in ("extraction_unverified", "response_parse_error", "timeout", "network_error", "runtime:apiconnection"))
               for r in score["exclusions"])


def compare(state, repeat, audit):
    arms = state["first_work_order"]
    ids = [f'B_{state["id"]}_r{repeat}_{arm}' for arm in arms]
    visible = [audit.load(key, "visible_start") for key in ids]
    full = [audit.load(key, "start") for key in ids]
    same = visible[0] == visible[1] == state["initial_visible"] and full[0] == full[1] == state["initial_full"]
    scores = [audit.scores[key] for key in ids]
    traces = [audit.load(key, "trace") for key in ids]
    allowed = [bool(t and t[0].get("allowed") and t[0]["model_original_choice"] == state["actions"][arm]) for t, arm in zip(traces, arms)]
    prefs = [preference(state, audit.load(key, "final")) if row["correct"] and state.get("priorities") else None for key, row in zip(ids, scores)]
    cost = [[row["agent"][key] for key in ("attempts", "input_tokens", "output_tokens")] + [row["simulator"]["attempts"],
            sum(event["module"] in ("task_execution_feedback", "native_execution", "native_speech") for event in trace)]
            for row, trace in zip(scores, traces)]
    hard = [(int(row["unauthorized_writes"] == 0), int(not row["unauthorized_attempt_events"])) for row in scores]
    correct = [row["correct"] for row in scores]
    level = "technical_or_restore_diagnostic"
    direction = "diagnostic"
    if same and all(allowed) and not audit.context_truncations and not any(technical(row) for row in scores):
        if hard[0] != hard[1]:
            direction, level = (arms[0] if hard[0] > hard[1] else arms[1]), "hard_constraints"
        elif correct[0] != correct[1]:
            direction, level = (arms[0] if correct[0] else arms[1]), "correct_terminal"
        elif not all(correct):
            direction, level = "diagnostic", "both_noncompliant"
        elif prefs[0] != prefs[1]:
            direction, level = (arms[0] if prefs[0] > prefs[1] else arms[1]), "explicit_user_preference"
        elif cost[0] != cost[1] and all(a <= b for a, b in zip(*cost)):
            direction, level = arms[0], "processing_cost_pareto"
        elif cost[0] != cost[1] and all(a >= b for a, b in zip(*cost)):
            direction, level = arms[1], "processing_cost_pareto"
        else:
            direction, level = "tie", "same_outcome_with_equal_or_incomparable_costs"
    return {"checkpoint": state["id"], "base_task": state["base_task"], "repeat": repeat, "branches": ids, "arms": arms,
            "same_visible_and_simulator_start": same, "first_work_allowed": allowed, "correct": correct,
            "hard_constraint_rank": hard, "explicit_preference_vectors": prefs, "cost_vectors": cost,
            "cost_fields": COST_FIELDS, "wall_seconds": [row["seconds"] for row in scores],
            "direction": direction, "basis": level, "clean_both": all(r["clean_execution"] for r in scores),
            "errors": [r["error"] for r in scores]}


def raw_autonomous(event, requests):
    decision = event["model_output"]
    for index, request in requests:
        if request["role"] != "cognitive" or request["status"] != "success":
            continue
        messages = request["messages"]
        content = request["response"]["choices"][0]["message"].get("content") or ""
        content = content.strip()
        if content.startswith("```") and content.endswith("```") and "\n" in content:
            content = content.split("\n", 1)[1][:-3].strip()
        try:
            visible = json.loads(messages[1]["content"])
            parsed = json.loads(content)
        except (ValueError, IndexError):
            continue
        if parsed == decision and visible == event["visible_state"] and not private_keys(visible):
            return {"messages": [*messages, {"role": "assistant", "content": content}]}, index, request["response"]["id"]
    return None


def clarify_sample(audit, score, i, trace, records):
    event, feedback = trace[i:i + 2]
    decision = event["model_output"]
    if not score["clean_execution"] or event.get("source") != "decision_model" or decision.get("work_type") != "clarify":
        return None
    if feedback["module"] != "task_execution_feedback" or not feedback["allowed"] or feedback.get("normalized_work", decision) != decision:
        return None
    refs = decision.get("evidence_refs") or []
    if not refs or any(type(r) is not int or not 0 <= r < len(feedback["before"]["history"]) for r in refs):
        return None
    option = decision.get("parameters", {}).get("variant_id") or decision.get("parameters", {}).get("payment_method_id")
    ref = (feedback.get("result") or {}).get("user_ref")
    if not option or not any(r.get("user_ref") == ref and r.get("accepted_offer") == option and not r.get("approved")
                             and option in r.get("reply", "") for r in records):
        return None
    result = raw_autonomous(event, audit.agent_calls[score["id"]])
    if result is None:
        return None
    sample, row, response = result
    return sample, {"branch": score["id"], "trace_event": i, "request_row_zero_based": row, "response_id": response,
                    "basis": "autonomous feasible clarification received literal option permission; independent transaction approval followed"}


def export(main, continuations, artifact, core, data_out=None):
    from dynamic_constraint_agent_v2.decision import PROMPT

    a = Audit(main, core)
    b = Audit(continuations, core)
    states = prep.read_json(continuations / "REGISTERED.json")
    pairs = [compare(state, repeat, b) for state in states for repeat in (1, 2)]
    prep.write_json(continuations / "PAIRS.json", pairs)
    output = data_out or (continuations / "samples")
    split = prep.read_json(prep.ROUND26 / "configs/PARTITIONS.json")["by_base_task"]
    sft, dpo = defaultdict(list), defaultdict(list)
    sft_manifest, dpo_manifest, rejects = [], [], []
    fingerprints = set()
    for label, audit in (("A", a), ("B", b)):
        if audit.context_truncations:
            continue
        request_hash = prep.file_hash(audit.out / "model_calls.jsonl")
        for branch, score in audit.scores.items():
            if score["group"] != "framework":
                continue
            trace = audit.load(branch, "trace")
            records = audit.load(branch, "simulator")
            base = score["business"] + ":" + score["task"]
            partition = split[base]
            for i, entry in enumerate(trace[:-1]):
                if entry["module"] != "work_selection" or entry.get("source") != "decision_model":
                    continue
                result = accepted_decision(score, branch, i, trace, audit.agent_calls[branch]) or clarify_sample(audit, score, i, trace, records)
                if result is None:
                    continue
                sample, provenance = result
                digest = core.hashed(sample)
                if digest in fingerprints:
                    continue
                fingerprints.add(digest)
                sft[partition].append(sample)
                sft_manifest.append({**provenance, "stage": label, "base_task": base, "split": partition, "line": len(sft[partition]),
                    "work": entry["model_output"]["work_type"], "sample_sha256": digest, "trace_sha256": score["source"]["trace_sha256"],
                    "requests_sha256": request_hash, "verified_end": True})
    for state in states:
        grouped = [p for p in pairs if p["checkpoint"] == state["id"]]
        winner = grouped[0]["direction"]
        if winner not in state["first_work_order"] or any(p["direction"] != winner or not p["clean_both"] for p in grouped):
            rejects.append({"checkpoint": state["id"], "directions": [p["direction"] for p in grouped], "reason": "no stable, fully auditable pair with both terminal outcomes"})
            continue
        loser = next(arm for arm in state["first_work_order"] if arm != winner)
        visible = state["initial_visible"]
        assert not private_keys(visible)
        prompt = (core.RETURN_DECISION if state["cfg"]["business"] == "return" else PROMPT) + "\n" + core.a2.POLICY
        record = {"prompt": [{"role": "system", "content": prompt}, {"role": "user", "content": core.packed(visible)}],
                  "chosen": [{"role": "assistant", "content": core.packed(state["actions"][winner])}],
                  "rejected": [{"role": "assistant", "content": core.packed(state["actions"][loser])}]}
        assert record["chosen"] != record["rejected"]
        partition = split[state["base_task"]]
        dpo[partition].append(record)
        dpo_manifest.append({"checkpoint": state["id"], "base_task": state["base_task"], "split": partition,
            "line": len(dpo[partition]), "sample_sha256": core.hashed(record), "matched_start_sha256": core.hashed(visible),
            "chosen_arm": winner, "rejected_arm": loser, "first_work_origin": "prespecified_experimental_intervention", "repeats": grouped,
            "trace_hashes": {key: b.scores[key]["source"]["trace_sha256"] for pair in grouped for key in pair["branches"]}})
    checked = {}
    output.mkdir(exist_ok=False)
    for name, dataset, manifest in (("sft", sft, sft_manifest), ("dpo", dpo, dpo_manifest)):
        for partition in ("train", "validation", "test"):
            path = output / f"{name}_{partition}.jsonl"
            write_jsonl(path, dataset[partition])
            written = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            for entry in [m for m in manifest if m["split"] == partition]:
                assert core.hashed(written[entry["line"] - 1]) == entry["sample_sha256"]
                assert checked.setdefault(entry["base_task"], partition) == partition
        prep.write_json(output / (name.upper() + "_MANIFEST.json"), manifest)
    summary = {"continuations": len(b.rows), "correct_continuations": sum(r["correct"] for r in b.scores.values()),
               "checkpoints": len(states), "matched_pairs": sum(p["same_visible_and_simulator_start"] for p in pairs),
               "run_issues": {"agent_output_limits": sum(s["agent"]["output_limit"] for s in b.scores.values()),
                              "simulator_output_limits": sum(s["simulator"]["output_limit"] for s in b.scores.values()),
                              "local_service_errors": sum(s["agent"]["service_errors"] + s["simulator"]["service_errors"] for s in b.scores.values()),
                              "context_truncations": b.context_truncations},
               "sft_candidates": len(sft_manifest), "sft_base_tasks": sorted({m["base_task"] for m in sft_manifest}),
               "sft_work": Counter(m["work"] for m in sft_manifest), "sft_stages": Counter(m["stage"] for m in sft_manifest),
               "dpo_candidates": len(dpo_manifest),
               "dpo_base_tasks": sorted({m["base_task"] for m in dpo_manifest}),
               "sft_splits": Counter(m["split"] for m in sft_manifest), "dpo_splits": Counter(m["split"] for m in dpo_manifest),
               "diagnostics_or_ties": rejects, "validation": "source/structure/hash/content and grouped partition checked; candidate data only"}
    prep.write_json(output / "SUMMARY.json", summary)
    prep.write_json(artifact, {"summary": summary, "checkpoints": [{k: s[k] for k in ("id", "base_task", "state", "goal", "hard_constraints", "user_preference", "feasibility")} for s in states],
                              "paired": pairs, "samples": {"sft": sft_manifest, "dpo": dpo_manifest}})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main", type=Path)
    parser.add_argument("continuations", type=Path)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--data-out", type=Path)
    args = parser.parse_args()
    repair = prep.prepare_sources()
    export(args.main.resolve(), args.continuations.resolve(), args.artifact.resolve(), repair.c,
           args.data_out.resolve() if args.data_out else None)
