"""Separate engineering replay for source-verified simulator defects in round 27."""

import argparse
from contextlib import contextmanager
from datetime import datetime
import json
from pathlib import Path
import re
from unittest.mock import patch

import prepare27 as prep
import run27
import simulator27 as sim


METHOD = r"\b(?:gift_card|credit_card|paypal)_[A-Za-z0-9]+\b"
CLOSING = r"(?:Is there anything else I can (?:do|help|assist)(?: you)?(?: with)?|Can I (?:help|assist)(?: you)? with anything else)\?"
STOP_CLAUSE = r"(?:no (?:changes|write operations) will be (?:made|performed)|(?:the|your) return request has been withdrawn|(?:the|your) order will (?:remain|be left) unchanged)"


def literal_list_choice(payload):
    if payload["business"] != "exchange":
        return None
    text = payload["actual_assistant"].rstrip()
    question = re.search(r"(?im)^\s*Please (?:(?:specify|tell me|select|choose) which [^\r\n]*(?:variant|SKU|replacement)|provide (?:the )?(?:new )?(?:item|SKU|replacement) ID)[^\r\n]*\Z", text)
    if question is None:
        return None
    prefix = text[:question.start()].rstrip()
    lines = []
    for line in reversed(prefix.splitlines()):
        match = re.match(r"\s*[-*]\s*(?:item\s+)?(\d{10})\s*:[^\r\n]*", line, re.I)
        if not match:
            break
        if not re.search(r"not available|unavailable|rejected|prohibited|out of stock", line, re.I):
            lines.append({"item_id": None, "variant_id": match.group(1), "payment_method_id": None,
                          "quote": line.strip(), "status": "active"})
    if not lines:
        headings = list(re.finditer(r"(?im)^\s*[^\r\n]{0,30}\bavailable (?:items|variants|alternatives)\b[^\r\n]*:\s*$", prefix))
        if not headings:
            return None
        listed = re.match(r"(?:\s*[-*]\s*(?:item\s+)?\d{10}\s*:[^\r\n]*\r?\n?)+", prefix[headings[-1].end():], re.I)
        if not listed:
            return None
        for line in reversed(listed.group().strip().splitlines()):
            match = re.match(r"\s*[-*]\s*(?:item\s+)?(\d{10})\s*:[^\r\n]*", line, re.I)
            if match and not re.search(r"not available|unavailable|rejected|prohibited|out of stock", line, re.I):
                lines.append({"item_id": None, "variant_id": match.group(1), "payment_method_id": None,
                              "quote": line.strip(), "status": "active"})
        if not lines:
            return None
    return {"kind": "spec_permission", "asks": True, "question_quote": question.group().strip(),
            "active_offers": list(reversed(lines)), "rejected_offer_ids": [], "topic": "none"}


class RepairedSimulator(sim.Simulator):
    def extract(self, messages, branch, trigger, limit=2100):
        payload = json.loads(messages[1]["content"])
        visible = literal_list_choice(payload)
        if visible is None or sim.problems(payload, visible, self.contains):
            return super().extract(messages, branch, trigger, limit)
        row = {"branch": branch, "role": "simulator", "status": "success", "request_sent": False,
               "trigger_reason": trigger, "binding_source": "literal_customer_request_after_offer_list",
               "evidence_binding": visible, "messages": messages}
        self.log.write(json.dumps(row, ensure_ascii=False) + "\n")
        self.log.flush()
        return visible


def bind_repairs(first, payload, value):
    text = payload["actual_assistant"]
    output = first(payload, value)
    if payload["business"] != "return":
        return output
    stop = re.search(STOP_CLAUSE, text, re.I)
    closing = re.search(CLOSING + r"\s*$", text, re.I)
    if stop and closing and "?" not in text[:closing.start()] and not re.search(r"\b(?:until|unless|before approval|not yet)\b", text, re.I):
        output.update(kind="stop", asks=False, question_quote="", stop_quote=stop.group(), topic="none", active_offers=[])
        return output
    question = output.get("question_quote") or ""
    if re.search(r"\bwhich\b.*\b(?:route|method)\b.*\b(?:accept|choose|prefer)\b", question, re.I):
        start = text.find(question)
        offers = []
        if start >= 0:
            after = text[start + len(question):]
            for line in after.splitlines():
                method = re.search(METHOD, line)
                route = re.search(r"\b(?:refund|return|original|gift card)\b", line, re.I)
                if method and route and not re.search(r"not available|unavailable|don't have|rejected|prohibited|not permitted", line, re.I):
                    offers.append({"item_id": None, "variant_id": None, "payment_method_id": method.group(),
                                   "quote": line.strip(), "status": "active"})
        if offers:
            output.update(kind="refund_permission", asks=True, topic="none", active_offers=offers)
    if output.get("kind") == "refund_permission":
        for offer in output.get("active_offers") or []:
            if isinstance(offer, dict) and isinstance(offer.get("payment_method_id"), str):
                offer["variant_id"] = None
    return output


@contextmanager
def repairs(core):
    bind = sim.bind_direct_question
    adjudicate = core.adjudicate

    def apply(payload, value):
        return bind_repairs(bind, payload, value)

    def score(world, text, ref, extraction):
        evidence = extraction.get("stop_quote") or ""
        if (world.business == "return" and getattr(world, "oracle_withdrawn", False)
                and extraction.get("kind") == "stop" and core.contains(text, evidence)
                and re.fullmatch(STOP_CLAUSE, evidence, re.I) and re.search(CLOSING + r"\s*$", text, re.I)):
            world.stopped = True
            world.terminal_reason = "withdrawal_acknowledged"
            reply = core.add_reply(world, ref, "Understood. Keep the database unchanged.", "stop")
            return {**reply, "extraction": extraction, "program_question_binding": "literal withdrawal acknowledgement before courtesy closure"}
        return adjudicate(world, text, ref, extraction)

    with patch.object(sim, "bind_direct_question", apply), patch.object(core, "adjudicate", score), patch.object(run27, "Simulator", RepairedSimulator):
        yield


def issue_replay(baseline, out, core):
    definitions = {"A_R_51_r1_official": {"kind": "refund_permission", "payment": "credit_card_8105988"},
                   "A_R_82_r1_official": {"kind": "stop", "asks": False},
                   "A_R_89_r1_official": {"kind": "stop", "asks": False},
                   "A_E_EDB05_r1_official": {"kind": "spec_permission", "offer": "7774234341"},
                   "A_E_EDB06_r1_official": {"kind": "spec_permission", "offer": "4938013542"}}
    audited = {}
    for line in (baseline / "simulator_calls.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        key = row["branch"]
        if key not in definitions or key in audited:
            continue
        payload = json.loads(row["messages"][1]["content"])
        spoken = payload["actual_assistant"]
        if key == "A_R_89_r1_official":
            if not (re.search(STOP_CLAUSE, spoken, re.I) and re.search(CLOSING + r"\s*$", spoken, re.I)):
                continue
        elif key != "A_E_EDB06_r1_official" and row["status"] != "failed":
            continue
        expected = definitions[key]
        if "offer" in expected:
            value = literal_list_choice(payload)
            if value is None:
                continue
        else:
            raw = row["response"]["choices"][0]["message"]["content"].strip()
            if raw.startswith("```") and raw.endswith("```"):
                raw = raw.split("\n", 1)[1][:-3].strip()
            try:
                value = sim.bind_direct_question(payload, json.loads(raw))
            except ValueError:
                continue
        issues = sim.problems(payload, value, core.contains)
        same_kind = value["kind"] == expected["kind"]
        if "payment" in expected:
            observed = {o["payment_method_id"] for o in value["active_offers"]}
            passed = same_kind and observed == {expected["payment"]} and not issues
        elif "offer" in expected:
            passed = same_kind and expected["offer"] in {o["variant_id"] for o in value["active_offers"]} and not issues
        else:
            passed = same_kind and value["asks"] is False and core.contains(payload["actual_assistant"], value["stop_quote"]) and not issues
        audited[key] = {"passed": passed, "known_original_issue": row.get("validation_issues") or "literal customer-facing speech misclassified",
                        "remaining_issues": issues}
    prep.write_json(out / "ISSUE_REPLAY.json", audited)
    if set(audited) != set(definitions) or not all(row["passed"] for row in audited.values()):
        raise RuntimeError("Targeted extraction replay failed")
    return [key.split("_r1_")[0].removeprefix("A_") for key in definitions]


def execute(baseline, out):
    repair = prep.prepare_sources()
    import post26

    if not (baseline / "SUMMARY.json").is_file():
        raise RuntimeError("Primary batch and audits must finish first")
    out.mkdir(parents=True, exist_ok=False)
    with repairs(repair.c):
        tasks = issue_replay(baseline, out, repair.c)
        original = prep.read_json(baseline / "FREEZE.json")
        plan = [item for item in original["plan"]["main"] if item["task"] in tasks]
        prep.write_json(out / "FREEZE.json", {"created": datetime.now().astimezone().isoformat(),
            "source_batch": str(baseline), "original_freeze_sha256": prep.file_hash(baseline / "FREEZE.json"),
            "recheck_sha256": prep.file_hash(Path(__file__)), "fixed_scope": "literal refund choice, withdrawal before courtesy close, and directly requested alternative from a literal list",
            "unaffected_original_hashes": original["hashes_sha256"], "paired_tasks": plan, "merge_with_primary": False})
        with run27.backends(repair, out) as transport:
            outcomes = []
            for item in plan:
                cfg = prep.read_json(prep.ROUND26 / "configs/tasks" / item["task"] / "case.json")
                row = repair.r.rollout(out, item["run"], cfg, transport, item["group"])
                start, end = [prep.read_json(out / (row["id"] + suffix)) for suffix in ("_start.json", "_final.json")]
                independent = post26.outcome(start, end)
                outcomes.append({**row, "independent": independent})
                prep.write_json(out / "OUTCOMES.json", outcomes)
        original_rows = {row["id"]: row for row in prep.read_json(baseline / "SCORES.json")}
        if any(row["correct"] != row["independent"]["correct"] for row in outcomes):
            raise RuntimeError("Targeted native-state audit disagrees with the replay runner")
        comparison = [{"branch": row["id"], "group": row["group"], "original_correct": original_rows[row["id"]]["correct"],
                       "recheck_correct": row["correct"], "original_error": original_rows[row["id"]]["error"],
                       "recheck_error": row["error"]} for row in outcomes]
        prep.write_json(out / "RECHECK_SUMMARY.json", {"scope": "diagnostic paired recheck; no primary scores replaced",
            "tasks": tasks, "runs": len(outcomes), "comparisons": comparison})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primary", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    execute(args.primary.resolve(), args.out.resolve())
