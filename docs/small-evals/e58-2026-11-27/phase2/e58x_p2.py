#!/usr/bin/env python3
"""E58 Phase 2 (private, NOT a comparison): Hermes delivery check.

Hermes (v0.23.0) is driven by the same local Bonsai server (custom provider) and calls the installed `patchsmith`
plugin's implement_task (clean clone of tmp/patchsmith-audit HEAD, not the dirty working tree). The saved Phase 1 Sol brief is
supplied as the prompt text; Hermes must pass it to implement_task(mode=apply). Scoring reuses e58x_pool acceptance,
unchanged. Reuses e58x_server_run's pins and server command read-only. No performance claim.

  python scripts/e58x_p2.py smoke      # server + one trivial Hermes call (no scoring)
  python scripts/e58x_p2.py run [N]    # N tasks (default 5)
"""
from __future__ import annotations

import json, os, socket, subprocess, sys, time
from pathlib import Path

import psutil, requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e57_run as R  # noqa: E402
import e57_server_run as S  # noqa: E402
import e58x_pool as P  # noqa: E402
import e58x_run as X  # noqa: E402

ROOT = R.ROOT
OUT = ROOT / "tmp" / "e58x" / "p2"
WORK = Path("<LOCAL_WORKDIR>/p2work")
ARM = R.ARMS["B"]
PORT = R.PORTS["bonsai"]
URL = f"http://127.0.0.1:{PORT}/v1"


def start_server():
    pins = json.loads((ROOT / "tmp/e57/freeze-hashes.json").read_text())["pins"]
    with socket.socket() as s:
        if s.connect_ex(("127.0.0.1", PORT)) == 0:
            raise SystemExit("port already occupied")
    for p in psutil.process_iter(["name"]):
        if any(x in (p.info["name"] or "").lower() for x in ["llama-server", "strata-inkling", "ollama", "edge0-infer"]):
            raise SystemExit("another model process exists")
    if S.gpu_used_mib() > 1500:
        raise SystemExit("GPU not idle")
    if S.file_sha(S.SERVERS["bonsai"]) != pins["server_exe_sha256"]["bonsai"] or S.file_sha(S.MODELS["bonsai"]) != pins["model_sha256"]["bonsai"]:
        raise SystemExit("server or model differs from E57 pin")
    OUT.mkdir(parents=True, exist_ok=True)
    argv = S.build_cmd("bonsai")
    log = (OUT / "p2-server.log").open("w")
    proc = subprocess.Popen(argv, cwd=S.SERVERS["bonsai"].parent, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    t0 = time.monotonic()
    while time.monotonic() - t0 < 600:
        if proc.poll() is not None:
            raise RuntimeError(f"server exited {proc.returncode}")
        try:
            if requests.get(f"http://127.0.0.1:{PORT}/health", timeout=2).status_code == 200:
                return proc
        except requests.RequestException:
            pass
        time.sleep(1)
    raise TimeoutError("server not healthy")


def stop_server(proc):
    parent = psutil.Process(proc.pid)
    kids = parent.children(recursive=True)
    for p in kids + [parent]:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
    _, alive = psutil.wait_procs(kids + [parent], timeout=10)
    for p in alive:
        p.kill()


def hermes(query: str, tag: str, env_extra: dict, toolsets: str, max_turns: int, timeout: int):
    qf = OUT / f"{tag}.query.txt"
    qf.write_text(query, encoding="utf-8")
    argv = ["hermes", "chat", "--provider", "custom", "--base-url", URL, "--api-key", "local", "-m", ARM["alias"],
            "--query-file", str(qf), "--oneshot", "-Q", "--max-turns", str(max_turns), "--yolo", "--ignore-rules"]
    if toolsets:
        argv += ["-t", toolsets]
    t0 = time.monotonic()
    try:
        cp = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                            env={**os.environ, **env_extra}, stdin=subprocess.DEVNULL)
        out = {"rc": cp.returncode, "stdout": cp.stdout[-4000:], "stderr": cp.stderr[-2000:]}
    except subprocess.TimeoutExpired as exc:
        out = {"rc": "timeout", "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "", "stderr": ""}
    out["seconds"] = round(time.monotonic() - t0, 1)
    (OUT / f"{tag}.hermes.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def plugin_env(task):
    return {"PS_ENDPOINT": URL, "PS_TEST_COMMAND": P.test_command(task["lang"]), "PS_MODEL": ARM["alias"],
            "PS_MAX_TURNS": str(R.LIMITS["max_turns"]), "PS_CTX_BUDGET": str(R.LIMITS["harness_input_budget"]),
            "PS_COMPLETION_CAP": str(R.LIMITS["request_max_tokens"]), "PS_HARNESS": "v5",
            "PS_REQUEST_TIMEOUT": str(R.LIMITS["task_seconds"]), "PS_DATA_DIR": str(OUT / "ledger"), "PS_ROUTER_MODE": "route", "PS_ROUTER_CLEAN_MINUTES": "0", "PS_ROUTER_HTTP400_MINUTES": "0",
            "PS_BUDGET_MODE": "context"}


def smoke():
    proc = start_server()
    try:
        out = hermes("Reply with the single word ready, and list the names of the tools you can call.", "smoke", {}, "", 3, 300)
        print(json.dumps(out, indent=1)[:3000])
    finally:
        stop_server(proc)


PLUGIN_DIR = Path("<HERMES_HOME>/plugins/patchsmith")


def load_plugin_tools() -> dict:
    """Import the INSTALLED Hermes plugin and capture what register() hands the host (no LLM driver)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("patchsmith_hermes", PLUGIN_DIR / "__init__.py",
                                                  submodule_search_locations=[str(PLUGIN_DIR)])
    mod = importlib.util.module_from_spec(spec)
    sys.modules["patchsmith_hermes"] = mod
    spec.loader.exec_module(mod)
    tools = {}

    class Ctx:
        def register_tool(self, name, toolset, schema, handler, **kw):
            tools[name] = handler

        def register_command(self, *a, **k):
            pass

        def register_skill(self, *a, **k):
            pass

    mod.register(Ctx())
    return tools


def run_direct(n: int):
    proto = X.check_frozen()
    allowed = set(proto["task_sets"]["P1"]) & set(proto["task_sets"]["P2"])
    ids = [i for i in P.order_for(1) if i in allowed][:n]
    by_id = P.by_id(P.load_tasks())
    sealed = P.OUT / "sealed"
    OUT.mkdir(parents=True, exist_ok=True)
    proc = start_server()
    rows = []
    try:
        os.environ.update(plugin_env(by_id[ids[0]]))
        tools = load_plugin_tools()
        print("registered:", sorted(tools), flush=True)
        for pos, tid in enumerate(ids, 1):
            task = dict(by_id[tid])
            os.environ.update(plugin_env(task))
            brief = (X.BRIEF_DIRS["P2"] / f"{tid}.md").read_text(encoding="utf-8").strip()
            text = X.WRAP.format(brief=brief, base=by_id[tid]["prompt"])
            ws = WORK / f"p2-{tid}"
            if ws.exists():
                raise SystemExit(f"workspace exists, refusing rerun: {ws}")
            P.write_tree(ws, P.pristine_files(task))
            for cmd in (["init", "-q"], ["config", "user.email", "e58@example.invalid"], ["config", "user.name", "E58"],
                        ["add", "--", *sorted(P.pristine_files(task))], ["commit", "-qm", "seed"]):
                subprocess.run(["git", "-c", "core.hooksPath=NUL", *cmd], cwd=ws, check=True, capture_output=True)
            t0 = time.monotonic()
            res = json.loads(tools["implement_task"]({"task": text, "workdir": str(ws), "mode": "apply", "attempts": 1,
                                                       "category": "multifile", "model": ARM["alias"]}))
            applied = None
            if res.get("patch_path") and res.get("status") not in ("frontier_required", "error"):
                applied = json.loads(tools["apply_patch"]({"patch_path": res["patch_path"]}))
            secs = time.monotonic() - t0
            viol = P.scan_changes(task, ws)
            acc = P.acceptance(task, ws, sealed)
            row = {"task_id": tid, "tool_status": res.get("status"), "tool_reason": res.get("reason"), "turns": res.get("turns"),
                   "routing": res.get("routing"), "patch_path": bool(res.get("patch_path")),
                   "apply_patch": ({k: applied.get(k) for k in ("status", "reason", "note", "applied")} if applied else None),
                   "applied": res.get("applied"), "files_changed": res.get("files_changed"), "boundary_violations": viol,
                   "hidden_passed": acc["passed"], "tool_seconds": round(secs, 1), "note": (res.get("note") or "")[:300]}
            rows.append(row)
            print(json.dumps(row), flush=True)
            (OUT / "p2-direct-rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
        # default-config behaviour: no PS_ROUTER_MODE override
        os.environ.pop("PS_ROUTER_MODE", None)
        ws = WORK / "p2-default-mode"
        t = dict(by_id[ids[0]])
        P.write_tree(ws, P.pristine_files(t))
        for cmd in (["init", "-q"], ["config", "user.email", "e58@example.invalid"], ["config", "user.name", "E58"],
                    ["add", "--", *sorted(P.pristine_files(t))], ["commit", "-qm", "seed"]):
            subprocess.run(["git", "-c", "core.hooksPath=NUL", *cmd], cwd=ws, check=True, capture_output=True)
        d = json.loads(tools["implement_task"]({"task": t["prompt"], "workdir": str(ws), "mode": "apply"}))
        dflt = {k: d.get(k) for k in ("status", "reason", "note", "turns")}
        (OUT / "p2-default-mode.json").write_text(json.dumps(dflt, indent=1), encoding="utf-8")
        print("default-mode:", json.dumps(dflt), flush=True)
    finally:
        stop_server(proc)


def run(n: int):
    proto = X.check_frozen()
    allowed = set(proto["task_sets"]["P1"]) & set(proto["task_sets"]["P2"])
    ids = [i for i in P.order_for(1) if i in allowed][:n]
    by_id = P.by_id(P.load_tasks())
    sealed = P.OUT / "sealed"
    proc = start_server()
    rows = []
    try:
        for pos, tid in enumerate(ids, 1):
            task = dict(by_id[tid])
            brief = (X.BRIEF_DIRS["P2"] / f"{tid}.md").read_text(encoding="utf-8").strip()
            text = X.WRAP.format(brief=brief, base=by_id[tid]["prompt"])
            ws = WORK / f"p2-{tid}"
            if ws.exists():
                raise SystemExit(f"workspace exists, refusing rerun: {ws}")
            P.write_tree(ws, P.pristine_files(task))
            for cmd in (["init", "-q"], ["config", "user.email", "e58@example.invalid"], ["config", "user.name", "E58"],
                        ["add", "--", *sorted(P.pristine_files(task))], ["commit", "-qm", "seed"]):
                subprocess.run(["git", "-c", "core.hooksPath=NUL", *cmd], cwd=ws, check=True, capture_output=True)
            query = ("Call the implement_task tool exactly once with workdir set to " + str(ws) + ", mode set to \"apply\", "
                     "and task set to the exact text between the markers below, unchanged. Then reply with only the tool's status.\n"
                     "<<<TASK\n" + text + "\nTASK>>>")
            h = hermes(query, f"p2-{tid}", plugin_env(task), "patchsmith", 8, 1500)
            viol = P.scan_changes(task, ws)
            acc = P.acceptance(task, ws, sealed)
            row = {"task_id": tid, "hermes_rc": h["rc"], "hermes_seconds": h["seconds"], "boundary_violations": viol,
                   "hidden_passed": acc["passed"], "diff_nonempty": bool(subprocess.run(["git", "diff", "--stat"], cwd=ws, capture_output=True, text=True).stdout.strip()),
                   "hermes_tail": h["stdout"][-400:]}
            rows.append(row)
            print(json.dumps({k: row[k] for k in row if k != "hermes_tail"}), flush=True)
            (OUT / "p2-rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    finally:
        stop_server(proc)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1] == "smoke":
        smoke()
    elif sys.argv[1] == "direct":
        run_direct(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    else:
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
