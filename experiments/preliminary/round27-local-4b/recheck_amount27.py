"""Paired diagnostic of the explicitly signed whole-exchange amount."""

import argparse
from datetime import datetime
from decimal import Decimal
import json
from pathlib import Path
import re
from unittest.mock import patch

import prepare27 as prep
import recheck27 as previous
import run27
import simulator27 as sim


WHOLE_LINE = re.compile(r"(?im)^\s*[-* ]*\b(?:combined new\s*[-–]?\s*minus\s*[-–]?\s*old difference|(?:whole|total) signed (?:price )?difference)\s*:\s*([^\r\n]+)")
SIGNED_TAIL = re.compile(r"\$?([+−-])\s*\$?\s*(\d[\d,]*\.\d{2})(?![\d.])\s*(?:\)|\*\*|\.)?\s*$")


def bind_signed_amount(payload, value):
    if payload["business"] != "exchange" or value.get("kind") != "proposal" or not value.get("asks"):
        return value
    text = payload["actual_assistant"]
    question = value.get("question_quote") or ""
    boundary = text.rfind(question) if question else -1
    if boundary < 0:
        return value
    evidence = []
    for line in WHOLE_LINE.finditer(text[:boundary]):
        calculation = line.group(1)
        found = SIGNED_TAIL.search(calculation)
        # Accept an explicit total or the signed result after '=', never an operand.
        prefix = calculation[:found.start()].strip() if found else ""
        if found and (not prefix or prefix.endswith("=")):
            amount = Decimal(found.group(2).replace(",", ""))
            if found.group(1) in ("−", "-"):
                amount = -amount
            evidence.append((amount, line.group().strip()))
    if len({amount for amount, _ in evidence}) == 1:
        amount, quote = evidence[-1]
        value.update(amount=float(amount), amount_quote=quote)
    return value


def former_failure_probe(first_recheck, core):
    key = "A_E_EDB06_r1_official"
    trace = prep.read_json(first_recheck / (key + "_trace.json"))
    for row in trace:
        reply = row.get("user_result") or {}
        extracted = reply.get("extraction") or {}
        checks = reply.get("checks") or {}
        if checks.get("amount") is not False or extracted.get("amount") != 8.42:
            continue
        speech = row["text"]
        corrected = bind_signed_amount({"business": "exchange", "actual_assistant": speech}, extracted.copy())
        if corrected.get("amount") != -8.42 or not core.contains(speech, corrected.get("amount_quote")):
            continue
        incomplete = speech.replace(" = -$8.42", "")
        unchecked = bind_signed_amount({"business": "exchange", "actual_assistant": incomplete}, extracted.copy())
        if unchecked != extracted:
            raise RuntimeError("An incomplete subtraction was misread as a signed total")
        return {"id": key, "old_amount": extracted["amount"], "corrected_amount": corrected["amount"],
                "literal_quote": corrected["amount_quote"], "incomplete_calculation_ignored": True, "former_checks": checks}
    raise RuntimeError("The recorded signed-amount defect did not reproduce")


def execute(primary, first_recheck, out):
    repair = prep.prepare_sources()
    import post26

    previous_result = prep.read_json(first_recheck / "RECHECK_SUMMARY.json")
    prior = {row["branch"]: row for row in previous_result["comparisons"]}
    frozen = prep.read_json(primary / "FREEZE.json")
    for name, digest in frozen["hashes_sha256"].items():
        if prep.file_hash(Path(name)) != digest:
            raise RuntimeError(f"Frozen baseline file changed: {Path(name).name}")
    plan = [item for item in frozen["plan"]["main"] if item["task"] == "E_EDB06"]
    assert len(plan) == 2
    out.mkdir(parents=True, exist_ok=False)
    probe = former_failure_probe(first_recheck, repair.c)
    prep.write_json(out / "SIGNED_AMOUNT_REPLAY.json", probe)
    prep.write_json(out / "FREEZE.json", {"created": datetime.now().astimezone().isoformat(),
        "source_batch": str(primary), "previous_recheck": str(first_recheck), "paired_tasks": plan,
        "original_freeze_sha256": prep.file_hash(primary / "FREEZE.json"),
        "previous_freeze_sha256": prep.file_hash(first_recheck / "FREEZE.json"),
        "files_sha256": {str(p): prep.file_hash(p) for p in (Path(__file__), Path(previous.__file__))},
        "change": "bind a unique visible explicitly signed whole-exchange delta before native rule checks"})
    with previous.repairs(repair.c):
        before_amount_binding = sim.bind_direct_question

        def corrected(payload, value):
            return bind_signed_amount(payload, before_amount_binding(payload, value))

        with patch.object(sim, "bind_direct_question", corrected), run27.backends(repair, out) as transport:
            results = []
            for item in plan:
                cfg = prep.read_json(prep.ROUND26 / "configs/tasks" / item["task"] / "case.json")
                row = repair.r.rollout(out, item["run"], cfg, transport, item["group"])
                start, final = [prep.read_json(out / (row["id"] + suffix)) for suffix in ("_start.json", "_final.json")]
                audited = post26.outcome(start, final)
                assert audited["correct"] == row["correct"]
                results.append({**row, "independent": audited})
                prep.write_json(out / "OUTCOMES.json", results)
    comparisons = [{"branch": row["id"], "group": row["group"], "previous_recheck_correct": prior[row["id"]]["recheck_correct"],
                  "signed_amount_recheck_correct": row["correct"], "error": row["error"]} for row in results]
    prep.write_json(out / "RECHECK_SUMMARY.json", {"scope": "signed amount diagnostic only", "compared": comparisons, "proof": probe})
    print(json.dumps(comparisons, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("primary", type=Path)
    parser.add_argument("first_recheck", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    execute(args.primary.resolve(), args.first_recheck.resolve(), args.out.resolve())
