"""Round 27 offline and local pilot checks. Formal batches are outside this entry point."""

import argparse
from collections import Counter
from contextlib import contextmanager
from copy import deepcopy
from hashlib import file_digest, sha256
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch


ROUND = Path(__file__).resolve().parent
REPO = ROUND.parents[2]
WORKSPACE = REPO.parent
ROUND26 = ROUND.parent / "round26-api-closeout"
TAU2 = WORKSPACE / "tools" / "tau2-official"
TAU2_COMMIT = "f8de30c298689cbe0117d76a378e7315a17e5bd8"
SERVER = WORKSPACE / "tools" / "llama.cpp-b10917" / "llama-server.exe"
GGUF = WORKSPACE / "models" / "gguf" / "Qwen3.5-4B-Q4_K_M.gguf"
MODEL = "qwen3.5-4b-q4-k-m"
CONTEXT = 32768
PORT = 18027
BASE_URL = f"http://127.0.0.1:{PORT}/v1"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def formal_plan(tasks, checkpoints):
    main = []
    for index, task in enumerate(tasks):
        groups = ("official", "framework") if index % 2 == 0 else ("framework", "official")
        for group in groups:
            main.append({
                "run": f'A_{task["id"]}_r1_{group}', "task": task["id"], "group": group,
                "business": task["business"], "scenario": task["scenario"],
            })
    continuations = []
    for checkpoint in checkpoints:
        state = checkpoint["id"]
        for repeat in (1, 2):
            works = checkpoint["first_works"] if repeat == 1 else reversed(checkpoint["first_works"])
            for work in works:
                continuations.append({
                    "run": f"B_{state}_r{repeat}_{work}", "checkpoint": state,
                    "repeat": repeat, "forced_first_work": work,
                })
    return {"status": "draft_not_frozen", "main": main, "continuations": continuations}


def file_hash(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def prepare_sources():
    os.environ.update(
        DCA_TAU2_ROOT=str(TAU2),
        TAU2_DATA_DIR=str(TAU2 / "data"),
        LITELLM_LOCAL_MODEL_COST_MAP="True",
        LITELLM_TELEMETRY="False",
    )
    sys.dont_write_bytecode = True
    tau_commit = subprocess.check_output(["git", "-C", TAU2, "rev-parse", "HEAD"], text=True).strip()
    if tau_commit != TAU2_COMMIT:
        raise RuntimeError(f"Unexpected τ²-bench commit {tau_commit}")
    agent = TAU2 / "src/tau2/agent/llm_agent.py"
    agent_bytes = agent.read_bytes().replace(b"\r\n", b"\n")
    archived = read_json(ROUND.parent / "round24-official-and-trajectory/versions/a2/configs/official_source.json")
    source_hashes = {sha256(agent_bytes).hexdigest(), sha256(agent_bytes.replace(b"\n", b"\r\n")).hexdigest()}
    if archived["sha256"] not in source_hashes:
        raise RuntimeError("Official LLMAgent differs from the archived source")

    # statefix3 includes the simfix4 → simfix2 → simfix1 adjudication chain.
    repair_dir = ROUND26 / "versions/statefix3"
    spec = importlib.util.spec_from_file_location("round27_round26_repairs", repair_dir / "repair.py")
    repair = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(repair)
    repair.r.verify()
    frozen = read_json(repair_dir / "FREEZE.json")
    for relative, expected in frozen["files"].items():
        if file_hash(REPO / relative) != expected:
            raise RuntimeError(f"Round 26 repair hash differs for {relative}")
    return repair


def offline_checks(repair, out):
    import offline26

    # Keep the original frozen outputs intact when reusing these checks.
    with patch.object(offline26, "save", lambda _path, data: write_json(out / "OFFLINE.json", data)):
        offline26.check()
    with patch.object(repair, "save", lambda _path, data: write_json(out / "STATEFIX_OFFLINE.json", data)):
        repair.offline()


@contextmanager
def server(out):
    import httpx

    with socket.socket() as check:
        check.bind(("127.0.0.1", PORT))
    args = [
        str(SERVER), "-m", str(GGUF), "-ngl", "99", "-fa", "on", "-c", str(CONTEXT),
        "-np", "1", "--host", "127.0.0.1", "--port", str(PORT), "--alias", MODEL,
        "--no-context-shift", "--chat-template-kwargs", '{"enable_thinking":false}',
    ]
    with (out / "llama-server.log").open("wb") as log:
        process = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 45
            with httpx.Client(trust_env=False, timeout=1) as http:
                while time.monotonic() < deadline:
                    if process.poll() is not None:
                        raise RuntimeError(f"llama-server exited with {process.returncode}")
                    try:
                        result = http.get(BASE_URL.removesuffix("/v1") + "/health")
                        if result.is_success:
                            break
                    except httpx.TransportError:
                        pass
                    time.sleep(0.5)
                else:
                    raise RuntimeError("llama-server did not become ready")
            yield
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


@contextmanager
def local_transport(repair, out):
    import httpx
    from openai import OpenAI
    from tau2.utils import llm_utils

    # Both Agent groups and the shared speech extractor use this same local client.
    with OpenAI(api_key="local", base_url=BASE_URL, timeout=60, max_retries=0,
                http_client=httpx.Client(trust_env=False, timeout=60)) as client:
        create = client.chat.completions.create

        def complete(**kwargs):
            kwargs.pop("extra_body", None)  # Server sets thinking through its chat template.
            return create(**kwargs)

        sdk = SimpleNamespace(client=client, secret=None)
        baseline = repair.c.a2.b
        with patch.object(client.chat.completions, "create", complete), patch.object(baseline, "MODEL", MODEL):
            with patch.object(baseline, "DeepSeek", lambda **_kwargs: sdk):
                transport = repair.c.Transport(out)
            try:
                with patch.object(llm_utils, "completion", transport.official_completion), patch.object(llm_utils, "get_response_cost", lambda _: None):
                    yield transport
            finally:
                transport.close()


def native_tool_probe(repair, transport):
    from tau2.data_model.message import MultiToolMessage, ToolMessage, UserMessage

    cfg = read_json(ROUND26 / "configs/PILOT_RETURN.json")
    world = repair.r.snapshot(cfg, transport, "official")
    order_id = cfg["order_id"]
    tool = world.tools.get_tools()["get_order_details"]
    agent = repair.c.LLMAgent([tool], "Copy order IDs exactly, including the leading #. Use the tool result when reporting order status.",
                              llm=MODEL, llm_args={"temperature": 0, "num_retries": 0, "max_tokens": 256})
    transport.world = world
    transport.branch = "native_tool_probe"
    question = UserMessage(role="user", content=f'Call get_order_details for the exact order ID "{order_id}". After the tool returns, state the order status.')
    message, state = agent.generate_next_message(question, agent.get_init_state())
    calls = message.tool_calls or []
    right_format = len(calls) == 1 and calls[0].name == "get_order_details" and bool(calls[0].id)
    right_arguments = right_format and calls[0].arguments == {"order_id": order_id}
    result = {"native_tool_call": right_format, "exact_arguments": right_arguments, "tool_result_consumed": False}
    if right_arguments:
        call = calls[0]
        order = repair.c.dump(world.tools.use_tool(call.name, **call.arguments))
        tool_message = ToolMessage(role="tool", id=call.id, content=json.dumps(order), error=False)
        next_reply, _ = agent.generate_next_message(MultiToolMessage(role="tool", tool_messages=[tool_message]), state)
        result["tool_result_consumed"] = not next_reply.tool_calls and order["status"].lower() in (next_reply.content or "").lower()
    return result


def pilot(repair, transport, out):
    return_case = read_json(ROUND26 / "configs/PILOT_RETURN.json")
    return_case["scenario"] = return_case["event"]["kind"]
    cases = {"return_scope": return_case}
    exchange = read_json(repair.c.a2.E / "configs/A/23/case.json")
    exchange.update(business="exchange", scenario="resource", cap="10000.00")
    cases["exchange_resource"] = exchange
    formal_orders = {task["order_id"] for task in read_json(ROUND26 / "configs/TASKS.json")}
    if any(config["order_id"] in formal_orders for config in cases.values()):
        raise RuntimeError("A pilot order overlaps the registered main comparison")
    rows = []
    for case, config in cases.items():
        for group in ("official", "framework"):
            rows.append(repair.r.rollout(out, f"pilot_{case}_{group}", deepcopy(config), transport, group))
            write_json(out / "OUTCOMES.json", rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("offline", "probe", "pilot"))
    parser.add_argument("--out", required=True, type=Path, help="New local directory for preflight artifacts")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    repair = prepare_sources()
    tasks = read_json(ROUND26 / "configs/TASKS.json")
    checkpoints = read_json(ROUND26 / "configs/DPO_CHECKPOINTS.json")
    mix = Counter(task["business"] for task in tasks)
    if mix != {"exchange": 8, "return": 12} or len({task["order_id"] for task in tasks}) != 20 or len(checkpoints) != 3:
        raise RuntimeError("Unexpected registered tasks or checkpoints")
    plan = formal_plan(tasks, checkpoints)
    write_json(out / "FORMAL_PLAN_DRAFT.json", plan)
    inherited_budget = read_json(ROUND26 / "configs/MODEL_BUDGET.json")
    del inherited_budget["model"]
    write_json(out / "SETTINGS.json", {
        "status": "preflight_not_frozen", "phase": args.phase, "model": MODEL,
        "source_model": "Qwen/Qwen3.5-4B", "source_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
        "gguf_sha256": file_hash(GGUF), "llama_cpp": "b10917 CUDA 13.3", "gpu": "RTX 5070 12 GB",
        "tau2_commit": TAU2_COMMIT, "round26_reuse": "statefix3 + simfix4 chain",
        "python": sys.version.split()[0], "packages": {pkg: importlib.metadata.version(pkg) for pkg in ("openai", "httpx", "pydantic", "litellm")},
        "endpoint": BASE_URL, "context": CONTEXT, "context_shift": False, "parallel_slots": 1, "temperature": 0,
        "thinking": False, "format_constraint": None, "simulator_model": MODEL,
        "round26_budget": inherited_budget,
        "formal_main_tasks": dict(mix), "formal_main_rollouts": len(plan["main"]),
        "checkpoints": [checkpoint["id"] for checkpoint in checkpoints],
        "formal_continuations": len(plan["continuations"]),
    })
    offline_checks(repair, out)
    if args.phase != "offline":
        with server(out), local_transport(repair, out) as transport:
            probe = native_tool_probe(repair, transport)
            write_json(out / "NATIVE_PROBE.json", probe)
            print(probe, flush=True)
            if not all(probe.values()):
                raise SystemExit("Native tool probe failed. Review the raw request and response before starting pilots.")
            if args.phase == "pilot":
                pilot(repair, transport, out)


if __name__ == "__main__":
    main()
