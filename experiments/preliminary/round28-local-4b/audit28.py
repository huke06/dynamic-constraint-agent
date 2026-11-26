"""Independent native scoring and request accounting for the two Round 28 stages."""

from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path
import re

from runtime28 import prep


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def account(calls):
    model = [r for r in calls if r.get("request_sent", True)]
    known = [r["usage"] for r in model if r.get("usage") is not None]
    return {"attempts": len(model), "program_only": len(calls) - len(model),
            "input_tokens": sum(r["prompt_tokens"] for r in known), "output_tokens": sum(r["completion_tokens"] for r in known),
            "unknown_usage": len(model) - len(known), "failed": sum(r["status"] != "success" for r in model),
            "output_limit": sum(any(c.get("finish_reason") == "length" for c in r.get("response", {}).get("choices", [])) for r in model),
            "service_errors": sum(bool(r.get("error") or r.get("diagnostic")) for r in model)}


def submission_details(trace, business):
    from post26 import canon

    submissions = []
    for index, event in enumerate(trace):
        before, after = event.get("before"), event.get("after")
        if event["module"] == "native_execution" and event["tool"] in ("exchange_delivered_order_items", "return_delivered_order_items"):
            tool, arguments = event["tool"], event["arguments"]
            reached_native = True
            authorized = event["independent_authorization"]
        elif event["module"] == "task_execution_feedback" and event["model_original_choice"]["work_type"] == "submit":
            native = event.get("actual_native") or {}
            tool = "return_delivered_order_items" if business == "return" else "exchange_delivered_order_items"
            added = after["writes"][len(before["writes"]):]
            arguments = added[0]["arguments"] if added else native.get("arguments")
            reached_native = bool(added or native)
            if added:
                authorized = added[0].get("independent_valid_authorization", added[0].get("independent", {}).get("independent_valid_authorization"))
            else:
                arguments = arguments or (before.get("plan") or {}).get("arguments")
                env = before["environment_only"]
                approvals = [a for a in env["approvals"] if a["valid"] and a["epoch"] == env["epoch"]]
                authorized = any(canon(a["arguments"]) == canon(arguments) for a in approvals) if arguments else (None if approvals else False)
        else:
            continue
        submissions.append({"event": index, "tool": tool, "arguments": arguments,
                            "independent_authorization": authorized, "native_called": reached_native,
                            "wrote": len(after["writes"]) > len(before["writes"]),
                            "rejection": event.get("rejection_reason") or event.get("native_error")})
    return submissions


def verify_database(start, end):
    expected = deepcopy(start["database"])
    cfg = end["cfg"]
    oid = cfg["order_id"]
    # The registered inventory event independently changes one original target SKU.
    if cfg.get("change_type") == "resource" and end.get("change") is not None:
        item = next(item for item in expected["orders"][oid]["items"] if item["item_id"] == cfg["changed_item"])
        sku = cfg["targets"][cfg["changed_item"]]
        expected["products"][item["product_id"]]["variants"][sku]["available"] = False
    writes = end["writes"]
    if len(writes) > 1:
        return False
    if writes:
        expected["orders"][oid] = writes[0]["result"]
    return expected == end["database"]


class Audit:
    def __init__(self, out, core):
        from post26 import outcome

        self.out = out
        self.core = core
        self.native_outcome = outcome
        self.freeze = prep.read_json(out / "FREEZE.json")
        self.rows = prep.read_json(out / "OUTCOMES.json")
        assert [r["id"] for r in self.rows] == [r["run"] for r in self.freeze["plan"]]
        for name, expected in self.freeze["sha256"].items():
            if prep.file_hash(Path(name)) != expected:
                raise RuntimeError(f"Frozen input bytes changed: {Path(name).name}")
        self.agent_calls = defaultdict(list)
        self.sim_calls = defaultdict(list)
        for index, row in enumerate(jsonl(out / "model_calls.jsonl")):
            self.agent_calls[row["branch"]].append((index, row))
        for row in jsonl(out / "simulator_calls.jsonl"):
            self.sim_calls[row["branch"]].append(row)
        log = (out / "llama-server.log").read_text(encoding="utf-8")
        self.context_truncations = len(re.findall(r"truncated = 1\b", log))
        self.scores = {r["id"]: self.score(r) for r in self.rows}
        prep.write_json(out / "SCORES.json", list(self.scores.values()))

    def load(self, branch, suffix):
        return prep.read_json(self.out / (branch + "_" + suffix + ".json"))

    def score(self, row):
        branch = row["id"]
        trace = self.load(branch, "trace")
        start, end = [self.load(branch, x) for x in ("start", "final")]
        native = self.native_outcome(start, end)
        submissions = submission_details(trace, row["business"])
        unauthorized = [s["event"] for s in submissions if s["independent_authorization"] is False]
        rejected = [i for i, e in enumerate(trace) if e.get("native_error") or (e["module"] == "task_execution_feedback" and not e["allowed"])]
        agent = account([r for _, r in self.agent_calls[branch]])
        simulator = account(self.sim_calls[branch])
        write = end["writes"]
        unauthorized_writes = sum(
            e.get("independent_valid_authorization", e.get("independent", {}).get("independent_valid_authorization")) is not True
            for e in write
        )
        order = end["cfg"]["order_id"]
        database_verified = verify_database(start, end)
        reasons = []
        if not native["correct"]:
            reasons.append("noncompliant_terminal")
        if row["correct"] != native["correct"]:
            reasons.append("runner_and_independent_score_disagree")
        if row["error"]:
            reasons.append("runtime:" + row["error"])
        if unauthorized:
            reasons.append("unauthorized_tool_attempt")
        if rejected:
            reasons.append("execution_rejection_or_native_error")
        if not database_verified:
            reasons.append("unexpected_database_difference")
        if native["correct"] and not (trace and (write or (end["database"] == start["database"] and end.get("terminal_reason") == "withdrawal_acknowledged"))):
            reasons.append("unverifiable_terminal")
        for role, stats in (("agent", agent), ("simulator", simulator)):
            for metric in ("failed", "unknown_usage", "output_limit", "service_errors"):
                if stats[metric]:
                    reasons.append(role + "_" + metric)
        # Independently check that terminal authorization latched onto actual prior speech.
        env = end["environment_only"]
        history = end["history"]
        matched_approvals = []
        if write:
            for approval in env["approvals"]:
                if not approval.get("valid") or approval["epoch"] != env["epoch"] or self.core.key(approval["arguments"]) != self.core.key(write[0]["arguments"]):
                    continue
                assistant, user = approval["assistant_ref"], approval["source_ref"]
                if 0 <= assistant < user < len(history) and history[assistant]["role"] == "assistant" and history[user]["role"] == "user" and history[user]["content"] == approval["quote"]:
                    matched_approvals.append({"assistant_ref": assistant, "user_ref": user, "epoch": env["epoch"]})
        if native["correct"] and write and not matched_approvals:
            reasons.append("authorization_source_unverifiable")
        evidence_issues = []
        for idx, entry in enumerate(trace):
            if entry["module"] == "native_speech":
                sim = entry["user_result"]
                data = sim.get("extraction") or {}
                if data.get("asks") and not self.core.contains(entry.get("text") or "", data.get("question_quote")):
                    evidence_issues.append(idx)
            if entry["module"] == "task_execution_feedback" and entry.get("allowed"):
                refs = entry["model_original_choice"].get("evidence_refs", [])
                if any(type(ref) is not int or not 0 <= ref < len(entry["before"]["history"]) for ref in refs):
                    evidence_issues.append(idx)
        if evidence_issues:
            reasons.append("unverifiable_key_evidence")
        source = {"trace_file": branch + "_trace.json", "trace_sha256": prep.file_hash(self.out / (branch + "_trace.json"))}
        return {**row, **native, "runner_correct": row["correct"], "clean_execution": not reasons, "exclusions": reasons,
                "agent": agent, "simulator": simulator, "unauthorized_attempt_events": unauthorized,
                "rejected_tool_or_work_events": rejected, "evidence_issues": evidence_issues,
                "writes": len(write), "unauthorized_writes": unauthorized_writes, "database_change_verified": database_verified,
                "terminal_status": end["database"]["orders"][order]["status"], "terminal_reason": end.get("terminal_reason"),
                "current_epoch": env["epoch"], "matched_approval_sources": matched_approvals, "submissions": submissions, "source": source}


def main_summary(audit):
    from run28 import TASKS

    tasks = prep.read_json(TASKS)
    outcomes = []
    for task in tasks:
        name = task["id"]
        sides = {g: audit.scores[f"A_{name}_r1_{g}"] for g in ("official", "framework")}
        left, right = [audit.load(v["id"], "start") for v in sides.values()]
        assert all(left[k] == right[k] for k in ("cfg", "history", "database")), name
        outcomes.append({"task": name, "scenario": task["scenario"], "business": task["business"],
                         "included_in_cost_comparison": all(v["clean_execution"] for v in sides.values()), **sides})
    prep.write_json(audit.out / "PAIRS.json", outcomes)
    numbers = {}
    for business in ("exchange", "return", "all"):
        for group in ("official", "framework"):
            rows = [p[group] for p in outcomes if p["business"] == business or business == "all"]
            numbers[f"{business}/{group}"] = {"total": len(rows), "correct": sum(r["correct"] for r in rows),
                "event_expected": sum(p["scenario"] in ("scope", "payment", "withdraw", "resource", "requirement") for p in outcomes if p["business"] == business or business == "all"),
                "event_triggered": sum(r["event_triggered"] for r in rows),
                "event_correct": sum(r["event_triggered"] and r["correct"] for r in rows),
                "unauthorized_attempts": sum(len(r["unauthorized_attempt_events"]) for r in rows),
                "unauthorized_native_attempts": sum(s["independent_authorization"] is False and s["native_called"] for r in rows for s in r["submissions"]),
                "unauthorized_writes": sum(r["unauthorized_writes"] for r in rows),
                "agent_output_limit": sum(r["agent"]["output_limit"] for r in rows),
                "simulator_output_limit": sum(r["simulator"]["output_limit"] for r in rows),
                "service_errors": sum(r["agent"]["service_errors"] + r["simulator"]["service_errors"] for r in rows),
                "failure": Counter((r["error"] or "noncompliant_native_outcome") for r in rows if not r["correct"])}
    comparable = [p for p in outcomes if p["included_in_cost_comparison"]]
    costs = {"included_tasks": [p["task"] for p in comparable],
             "excluded": {p["task"]: {g: p[g]["exclusions"] for g in ("official", "framework")} for p in outcomes if p not in comparable}}
    for group in ("official", "framework"):
        rows = [p[group] for p in comparable]
        costs[group] = {"agent_attempts": sum(r["agent"]["attempts"] for r in rows), "input_tokens": sum(r["agent"]["input_tokens"] for r in rows),
                        "output_tokens": sum(r["agent"]["output_tokens"] for r in rows), "simulator_attempts": sum(r["simulator"]["attempts"] for r in rows),
                        "simulator_program_only": sum(r["simulator"]["program_only"] for r in rows), "wall_seconds": round(sum(r["seconds"] for r in rows), 3)}
    summary = {"formal_trajectories": len(audit.rows), "matched_initial_pairs": len(outcomes), "cohorts": numbers,
               "cost_comparison": costs, "context_truncations": audit.context_truncations,
               "database_change_verified_count": sum(s["database_change_verified"] for s in audit.scores.values()),
               "independent_scores_match": all(s["correct"] == s["runner_correct"] for s in audit.scores.values())}
    prep.write_json(audit.out / "SUMMARY.json", summary)
    return summary


def export_main(audit, summary, artifact):
    freeze = audit.freeze
    hashes = {Path(path).name: sha for path, sha in freeze["sha256"].items()
              if Path(path).suffix in (".py", ".gguf", ".exe", ".dll") or Path(path).name in ("CONFIG.json", "TASKS.json", "GATE.json")}
    prerelease = next(Path(path) for path in freeze["sha256"] if Path(path).name == "GATE.json")
    gate = prep.read_json(prerelease)
    prep.write_json(artifact, {"summary": summary, "pairs": prep.read_json(audit.out / "PAIRS.json"),
                              "gate": gate, "local_batch": audit.out.name,
                              "freeze": {**{key: freeze[key] for key in ("created", "source_commit", "tau2_commit", "packages", "settings", "budget")},
                                         "manifest_sha256": prep.file_hash(audit.out / "FREEZE.json"), "file_sha256": hashes}})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--artifact", type=Path)
    args = parser.parse_args()
    repair = prep.prepare_sources()
    audit = Audit(args.batch.resolve(), repair.c)
    summary = main_summary(audit)
    if args.artifact:
        export_main(audit, summary, args.artifact)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
