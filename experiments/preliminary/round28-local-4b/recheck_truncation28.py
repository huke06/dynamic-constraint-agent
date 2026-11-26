"""Replay the frozen A extraction failure and two live controls in isolation."""

import argparse
import json
from pathlib import Path

from audit28 import jsonl
from run28 import OUT, freeze
from runtime28 import backends, installed, prep


def replay(main, out, repair):
    log = main / "simulator_calls.jsonl"
    calls = jsonl(log)
    probes = [
        ("truncated_narration", "A_E_EDB08_r1_official", lambda row, _: row["status"] == "failed"),
        ("signed_approval_control", "A_E_EDB06_r1_official", lambda row, p: row["status"] == "success" and "-$8.42" in p["actual_assistant"]),
        ("refund_route_control", "A_R_51_r1_official", lambda row, _: row["status"] == "success"),
    ]
    replays = [(name, next((i, row) for i, row in enumerate(calls)
                           if row["branch"] == branch and match(row, json.loads(row["messages"][1]["content"]))))
               for name, branch, match in probes]
    freeze(out, "A_extraction_diagnostic", [{"id": name, "source_row_zero_based": i, "branch": row["branch"]}
                                          for name, (i, row) in replays], (Path(__file__), log))
    note = ("Use short, literal quotes. Never copy the whole assistant message into a field. "
            "Only questions directed to the customer count. Internal planning, narrative about what to ask next, "
            "and unfinished text are not authorization questions. For no complete, customer-facing request, "
            "return kind other, asks false, empty question_quote and proposal_quote, and no active offers.")
    records = []
    with prep.server(out), backends.simulator(repair, out) as model:
        for name, (index, row) in replays:
            messages = [{"role": "system", "content": repair.c.EXTRACT + "\n" + note}, row["messages"][1]]
            value = model.extract(messages, name, "isolated_truncated_speech_replay")
            records.append({"id": name, "source_row_zero_based": index, "source_status": row["status"],
                            "new_kind": value["kind"], "asks": value["asks"], "amount": value.get("amount"),
                            "binding": value})
            prep.write_json(out / "REPLAY.json", records)
    assert records[0]["new_kind"] == "other" and not records[0]["asks"]
    assert records[1]["new_kind"] == "proposal" and records[1]["amount"] == -8.42
    assert records[2]["new_kind"] == "refund_permission"
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main", type=Path)
    parser.add_argument("--out", type=Path, default=OUT / "targeted01")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    repair = prep.prepare_sources()
    with installed(repair):
        replay(args.main.resolve(), args.out.resolve(), repair)
