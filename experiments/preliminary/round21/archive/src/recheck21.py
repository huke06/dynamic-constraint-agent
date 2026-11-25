"""Freeze and run the predeclared round-21 repair recheck as a fresh batch."""

import argparse
import re
from datetime import datetime, timezone

from construct20 import R, read, save, sha


CASES = {
    "80": ("stable", "unchanged_basic_control"),
    "49": ("stable", "missing_inventory_and_offer_choice"),
    "23": ("changed", "inventory_change"),
    "107": ("changed", "inventory_change"),
    "29": ("changed", "requirement_change"),
}
FROZEN = R / "configs" / "recheck21_freeze.json"


def freeze():
    if FROZEN.exists():
        raise SystemExit("Freeze exists. Use a new experiment version for changes.")
    report = R / "results" / "offline_regression.json"
    if not read(report)["passed"]:
        raise SystemExit("Run the offline regression before freezing.")
    files = {
        path.relative_to(R).as_posix(): sha(path)
        for directory in (R / "src", R / "configs") for path in directory.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    files[report.relative_to(R).as_posix()] = sha(report)
    save(FROZEN, {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "files": files, "cases": CASES, "repeats": 2,
    })
    print(f"Frozen {len(files)} file hashes; {len(CASES) * 2 * 2} planned trajectories.")


def run(batch_name):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", batch_name):
        raise SystemExit("Use only letters, digits, underscores, and hyphens in the batch name.")
    record = read(FROZEN)
    if any(sha(R / path) != digest for path, digest in record["files"].items()):
        raise SystemExit("A frozen input changed. Start a new experimental version.")
    out = R / "results" / batch_name
    out.mkdir(exist_ok=False)
    save(out / "started.json", {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "freeze_sha256": sha(FROZEN),
    })
    from official20 import native_roll
    from runner20 import rollout
    from transport20 import Transport

    transport = Transport(out)
    try:
        transport.install()
        outcomes = {}
        for task_id, (version, _) in CASES.items():
            config = read(R / "configs" / "stage2" / task_id / "case.json")
            for repeat, order in ((1, ("official", "ondemand")), (2, ("ondemand", "official"))):
                for group in order:
                    name = f"{config['tier']}_t{task_id}_r{repeat}_{group}"
                    if group == "official":
                        outcome = native_roll(config, version, name, transport, out)
                    else:
                        outcome = rollout(config, version, group, name, transport, out)
                    outcomes[name] = outcome
                    save(out / "results.json", outcomes)
    finally:
        transport.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--freeze", action="store_true")
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--run", metavar="NEW_BATCH")
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.list:
        for task_id, (version, reason) in CASES.items():
            print(task_id, version, reason)
        print(f"{len(CASES) * 2 * 2} trajectories, {len(CASES)} independent tasks.")
    else:
        run(args.run)

