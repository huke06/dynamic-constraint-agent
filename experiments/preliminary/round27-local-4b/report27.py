"""Audit the completed frozen batch and export conservative learning candidates."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import re

import prepare27 as prep


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def usage(rows):
    known = [row["usage"] for row in rows if row.get("usage") is not None]
    return {
        "attempts": len(rows), "rejected_responses": sum(r["status"] != "success" for r in rows),
        "known_input_tokens": sum(r["prompt_tokens"] for r in known),
        "known_output_tokens": sum(r["completion_tokens"] for r in known),
        "unknown_usage_attempts": len(rows) - len(known),
        "request_seconds": round(sum(r["seconds"] for r in rows), 3),
    }


def private_keys(value):
    forbidden = {"environment_only", "oracle", "env_approvals", "changed_target", "future_event",
                 "evaluation_answer", "private_user_preferences", "change_type"}
    if isinstance(value, dict):
        return bool(forbidden.intersection(value)) or any(private_keys(v) for v in value.values())
    if isinstance(value, list):
        return any(private_keys(v) for v in value)
    return False


def accepted_decision(row, branch, index, trace, requests):
    event = trace[index]
    next_event = trace[index + 1] if index + 1 < len(trace) else {}
    if event.get("source") != "decision_model" or not row["clean_execution"]:
        return None
    decision = event["model_output"]
    if decision.get("work_type") != "query" or next_event.get("module") != "task_execution_feedback":
        return None
    before = next_event["before"]
    tool = decision.get("parameters", {}).get("tool")
    product = decision["object"]
    if row["business"] == "return":
        new_observation = tool not in before.get("observed", {}) and tool in next_event["after"].get("observed", {})
    else:
        new_observation = product not in before["core"]["products"] and product in next_event["after"]["core"]["products"]
    refs = decision.get("evidence_refs", [])
    if not (next_event["allowed"] and new_observation and refs and all(type(r) is int and 0 <= r < len(before["history"]) for r in refs)):
        return None
    if next_event.get("normalized_work", decision) != decision:
        return None
    for request_index, request in requests:
        if request["role"] != "cognitive" or request["status"] != "success":
            continue
        messages = request["messages"]
        raw = request["response"]["choices"][0]["message"]["content"].strip()
        content = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip() if raw.startswith("```") and "\n" in raw else raw
        try:
            visible = json.loads(messages[1]["content"])
            parsed = json.loads(content)
        except (IndexError, ValueError):
            continue
        if parsed == decision and visible == event["visible_state"] and not private_keys(visible):
            sample = {"messages": [*messages, {"role": "assistant", "content": content}]}
            source = {"branch": branch, "trace_event": index, "request_row_zero_based": request_index,
                      "response_id": request["response"]["id"], "basis": "allowed autonomous query added absent native evidence"}
            return sample, source
    return None


def preference(checkpoint, final):
    cfg = checkpoint["cfg"]
    args = final["writes"][0]["arguments"]
    if cfg["business"] == "return":
        return [int(args["payment_method_id"] == cfg["preferred_payment"])]
    original = cfg["scope"][0]
    mapping = dict(zip(args["item_ids"], args["new_item_ids"]))
    order = cfg["environment"]["orders"][cfg["order_id"]]
    product = next(i["product_id"] for i in order["items"] if i["item_id"] == original)
    options = final["database"]["products"][product]["variants"][mapping[original]]["options"]
    return [int(k in options and options[k] == cfg["initial_options"][original].get(k)) for k in checkpoint["priorities"]]


def dpo_paths(out, scores, snapshots, traces, core):
    from dynamic_constraint_agent_v2.decision import PROMPT

    comparisons = []
    candidates = []
    for state in prep.read_json(prep.ROUND26 / "configs/DPO_CHECKPOINTS.json"):
        name = state["id"]
        directions = []
        for repeat in (1, 2):
            ids = [f"B_{name}_r{repeat}_{action}" for action in ("analyze", "clarify")]
            visible = [prep.read_json(out / (key + "_visible_start.json")) for key in ids]
            same = visible[0] == visible[1]
            clean = all(scores[key]["clean_execution"] for key in ids)
            accepted = [bool(traces[key] and traces[key][0].get("allowed")) for key in ids]
            prefs = [preference(state, snapshots[key]) if scores[key]["correct"] else None for key in ids]
            direction = "pending"
            if clean and same and all(accepted):
                if prefs[0] != prefs[1]:
                    direction = "analyze" if prefs[0] > prefs[1] else "clarify"
                else:
                    costs = [tuple(scores[key]["agent"][field] for field in ("attempts", "known_input_tokens", "known_output_tokens")) for key in ids]
                    direction = "tie"
                    if costs[0] != costs[1] and all(a <= b for a, b in zip(*costs)):
                        direction = "analyze"
                    if costs[0] != costs[1] and all(a >= b for a, b in zip(*costs)):
                        direction = "clarify"
            comparisons.append({"checkpoint": name, "repeat": repeat, "branches": ids, "same_visible_input": same,
                                "correct": [scores[key]["correct"] for key in ids], "clean_both": clean,
                                "first_work_allowed": accepted, "preference_vectors": prefs, "direction": direction})
            directions.append(direction)
        winner = directions[0]
        if winner == directions[1] and winner in ("analyze", "clarify"):
            loser = "clarify" if winner == "analyze" else "analyze"
            chosen_id, rejected_id = [f"B_{name}_r1_{work}" for work in (winner, loser)]
            visible = prep.read_json(out / (chosen_id + "_visible_start.json"))
            if private_keys(visible):
                continue
            chosen = traces[chosen_id][0]["model_original_choice"]
            rejected = traces[rejected_id][0]["model_original_choice"]
            if chosen == rejected:
                continue
            system = (core.RETURN_DECISION if state["cfg"]["business"] == "return" else PROMPT) + "\n" + core.a2.POLICY
            record = {"prompt": [{"role": "system", "content": system}, {"role": "user", "content": core.packed(visible)}],
                      "chosen": [{"role": "assistant", "content": core.packed(chosen)}],
                      "rejected": [{"role": "assistant", "content": core.packed(rejected)}]}
            candidates.append((record, {"checkpoint": name, "base_task": state["cfg"]["business"] + ":" + state["cfg"]["task_id"],
                                        "chosen": chosen_id, "rejected": rejected_id, "repeats": directions,
                                        "basis": "preregistered forced first works, not autonomous targets"}))
    return comparisons, candidates


def analyze(out):
    repair = prep.prepare_sources()
    import post26

    freeze = prep.read_json(out / "FREEZE.json")
    for path, expected in freeze["hashes_sha256"].items():
        if prep.file_hash(Path(path)) != expected:
            raise RuntimeError(f"Frozen source has changed: {Path(path).name}")
    rows = prep.read_json(out / "OUTCOMES.json")
    planned = [e["run"] for group in ("main", "continuations") for e in freeze["plan"][group]]
    if len(rows) != 52 or [r["id"] for r in rows] != planned:
        raise RuntimeError("Formal outcomes are incomplete or out of frozen order")
    request_file = out / "model_calls.jsonl"
    ag = defaultdict(list)
    sim = defaultdict(list)
    for j, r in enumerate(jsonl(request_file)):
        ag[r["branch"]].append((j, r))
    for r in jsonl(out / "simulator_calls.jsonl"):
        sim[r["branch"]].append(r)
    scores, snapshots, traces = {}, {}, {}
    for row in rows:
        key = row["id"]
        start = prep.read_json(out / (key + "_start.json"))
        final = snapshots[key] = prep.read_json(out / (key + "_final.json"))
        trace = traces[key] = prep.read_json(out / (key + "_trace.json"))
        audited = post26.outcome(start, final)
        after = None
        for i, e in enumerate(trace):
            if e["module"] == "public_change":
                first = next((r for r in trace[i + 1:] if r["module"] in ("work_selection", "native_execution", "native_speech")), None)
                if first:
                    decision = first.get("model_output", {})
                    after = {"module": first["module"], "work": decision.get("work_type") or first.get("tool") or first.get("user_result", {}).get("kind"),
                             "object": decision.get("object", first.get("arguments")), "source": first.get("source")}
                break
        rejected = [e["rejection_reason"] for e in trace if e["module"] == "task_execution_feedback" and not e["allowed"]]
        native_errors = [e["native_error"] for e in trace if e.get("native_error")]
        unsafe = [e for e in trace if e.get("independent_authorization") is False]
        agent_usage = usage([r for _, r in ag[key]])
        sim_usage = usage(sim[key])
        length_limited = sum(r.get("response", {}).get("choices", [{}])[0].get("finish_reason") == "length" for _, r in ag[key])
        clean = audited["correct"] and row["correct"] and not any((row["error"], rejected, native_errors, unsafe, length_limited))
        clean = clean and all(u["rejected_responses"] == 0 and u["unknown_usage_attempts"] == 0 for u in (agent_usage, sim_usage))
        scores[key] = {**row, **audited, "runner_correct": row["correct"], "clean_execution": clean,
                       "final_current_authorization": audited["checks"].get("authorization"), "first_after_change": after,
                       "program_rejections": rejected, "native_errors": native_errors, "unauthorized_native_attempts": len(unsafe),
                       "agent": agent_usage, "simulator": sim_usage, "simulator_evidence_bindings": sum("evidence_binding" in r for r in sim[key]),
                       "agent_output_limit_hits": length_limited,
                       "write_count": len(final["writes"])}
    prep.write_json(out / "SCORES.json", list(scores.values()))
    if any(r["correct"] != r["runner_correct"] for r in scores.values()):
        raise RuntimeError("Native state recheck disagrees with the runner")
    pairs = defaultdict(dict)
    for e in freeze["plan"]["main"]:
        s = scores[e["run"]]
        pairs[e["task"]][e["group"]] = s
    paired_rows = []
    for name, sides in pairs.items():
        left, right = [prep.read_json(out / (sides[g]["id"] + "_start.json")) for g in ("official", "framework")]
        common_start = all(left[k] == right[k] for k in ("history", "database", "cfg"))
        if not common_start:
            raise RuntimeError(f"Pair {name} did not share initial public history, fixture and database")
        paired_rows.append({"task": name, "same_public_start_and_database": common_start, **sides})
    prep.write_json(out / "PAIRS.json", paired_rows)
    comparisons, dpo = dpo_paths(out, scores, snapshots, traces, repair.c)
    prep.write_json(out / "CONTINUATIONS.json", comparisons)
    partitions = prep.read_json(prep.ROUND26 / "configs/PARTITIONS.json")["by_base_task"]
    samples = out / "samples"
    samples.mkdir(exist_ok=True)
    sft = defaultdict(list)
    sft_manifest = []
    dpo_split = defaultdict(list)
    dpo_manifest = []
    seen = set()
    request_sha = prep.file_hash(request_file)
    for key, score in scores.items():
        for i, event in enumerate(traces[key]):
            if event["module"] != "work_selection":
                continue
            extracted = accepted_decision(score, key, i, traces[key], ag[key])
            if extracted is None:
                continue
            sample, source = extracted
            fingerprint = repair.c.hashed(sample)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            base = score["business"] + ":" + score["task"]
            split = partitions.get(base, "test")
            sft[split].append(sample)
            sft_manifest.append({**source, "base_task": base, "split": split, "line": len(sft[split]),
                                 "sha256": fingerprint, "request_file_sha256": request_sha})
    for record, info in dpo:
        split = partitions.get(info["base_task"], "test")
        dpo_split[split].append(record)
        dpo_manifest.append({**info, "split": split, "line": len(dpo_split[split]), "sha256": repair.c.hashed(record)})
    for split in ("train", "validation", "test"):
        write_jsonl(samples / f"sft_{split}.jsonl", sft[split])
        write_jsonl(samples / f"dpo_{split}.jsonl", dpo_split[split])
    prep.write_json(samples / "SFT_MANIFEST.json", sft_manifest)
    prep.write_json(samples / "DPO_MANIFEST.json", dpo_manifest)
    for kind, manifests in (("sft", sft_manifest), ("dpo", dpo_manifest)):
        for m in manifests:
            record = jsonl(samples / f'{kind}_{m["split"]}.jsonl')[m["line"] - 1]
            if repair.c.hashed(record) != m["sha256"]:
                raise RuntimeError("Export hash mismatch")
    summary = {"completed": len(rows), "main": len(pairs) * 2, "continuations": len(comparisons) * 2,
               "completed_at": datetime.now().astimezone().isoformat(), "cohorts": {}, "paired": {},
               "matched_public_starts": len(paired_rows),
               "continuation_directions": Counter(r["direction"] for r in comparisons),
               "sft_candidates": len(sft_manifest), "dpo_candidates": len(dpo_manifest),
               "candidate_review": "automated evidence screening; factual human review before training",
               "scoring": "independent native snapshots and same-generation authority; process issues retained"}
    log = (out / "llama-server.log").read_text(encoding="utf-8")
    summary["context"] = {"configured": freeze["local"]["context"],
                          "server_truncations": len(re.findall(r"truncated = 1\b", log)),
                          "largest_prompt_tokens": max((r["usage"]["prompt_tokens"] for calls in ag.values() for _, r in calls if r.get("usage")), default=0)}
    samples_log = out / "GPU_SAMPLES.jsonl"
    if samples_log.is_file():
        measurements = jsonl(samples_log)
        if measurements:
            summary["gpu"] = {"samples": len(measurements), "peak_sampled_device_used_mib": max(r["gpu_used_mib"] for r in measurements),
                              "total_device_mib": measurements[0]["gpu_total_mib"], "scope": "whole GPU including desktop"}
    for business in ("exchange", "return"):
        targets = [s for s in pairs.values() if s["official"]["business"] == business]
        summary["paired"][business] = dict(Counter(
            "both" if p["official"]["correct"] and p["framework"]["correct"] else
            "official_only" if p["official"]["correct"] else "framework_only" if p["framework"]["correct"] else "neither" for p in targets))
        for group in ("official", "framework"):
            entries = [p[group] for p in targets]
            summary["cohorts"][f"{business}/{group}"] = {"n": len(entries), "correct": sum(s["correct"] for s in entries),
                "clean_execution": sum(s["clean_execution"] for s in entries), "events": sum(s["event_triggered"] for s in entries),
                "planned_event_tasks": sum(s["scenario"] in {"resource", "requirement", "scope", "payment", "withdraw"} for s in entries),
                "correct_after_event": sum(s["correct"] and s["event_triggered"] for s in entries),
                "unauthorized_native_attempts": sum(s["unauthorized_native_attempts"] for s in entries),
                "unauthorized_written_trajectories": sum(s["write_count"] > 0 and s["final_current_authorization"] is False for s in entries),
                "agent_output_limit_hits": sum(s["agent_output_limit_hits"] for s in entries),
                "failed_reason": dict(Counter((s["error"] or "native_outcome_mismatch") for s in entries if not s["correct"]))}
    eligible = [p for p in pairs.values() if p["official"]["clean_execution"] and p["framework"]["clean_execution"]]
    summary["execution_clean_pair_costs"] = {"pairs": len(eligible), "classification": "automated screen, factual review pending",
        **{g: {"agent_attempts": sum(p[g]["agent"]["attempts"] for p in eligible),
                "agent_input_tokens": sum(p[g]["agent"]["known_input_tokens"] for p in eligible),
                "agent_output_tokens": sum(p[g]["agent"]["known_output_tokens"] for p in eligible),
                "simulator_attempts": sum(p[g]["simulator"]["attempts"] for p in eligible),
                "wall_seconds": round(sum(p[g]["seconds"] for p in eligible), 2)} for g in ("official", "framework")}}
    prep.write_json(out / "SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    analyze(parser.parse_args().out.resolve())
