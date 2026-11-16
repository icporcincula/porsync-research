"""Bounded local E39 follow-up; no frontier executor or routing-default changes.

Run from the research repository with Python 3.12. The launcher owns server
lifecycle. Fault responses are deliberately injected, never natural OOM evidence.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CODE = ROOT / "tmp/patchsmith-audit"
os.environ.update(PS_ENDPOINT="http://127.0.0.1:8000/v1", PS_MODEL="edge0_120b",
                  PS_DATA_DIR=str(ROOT / "tmp/e39-local-validation/data"),
                  PS_CTX_BUDGET="30000", PS_MAX_TURNS="30", PS_BUDGET_MODE="context")
spec = importlib.util.spec_from_file_location("patchsmith", CODE / "__init__.py",
                                            submodule_search_locations=[str(CODE)])
plugin = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = plugin
spec.loader.exec_module(plugin)
from patchsmith import router, loop
from patchsmith.llm import LocalModel

def record(kind, **values):
    row = dict(kind=kind, timestamp=time.time(), **values)
    with (OUT / "results.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps(row), flush=True)

def request(prompt, tokens=32, timeout=None):
    start = time.monotonic()
    try:
        client = LocalModel(os.environ["PS_ENDPOINT"], "edge0_120b")
        client.request_timeout = timeout
        message, usage = client.complete(
            [{"role": "user", "content": prompt}], [], tokens)
        return dict(ok=True, seconds=time.monotonic()-start, usage=usage, content=message["content"])
    except Exception as exc:
        return dict(ok=False, seconds=time.monotonic()-start, error=str(exc))

def git(work, *args):
    return subprocess.run(["git", *args], cwd=work, capture_output=True, check=True)

def route_case(category):
    work = ROOT / "tmp/e39-local-validation" / category
    shutil.copytree(CODE / "tests/fixtures" / category, work)
    git(work, "init", "-q")
    git(work, "config", "user.name", "E39 Local Validation")
    git(work, "config", "user.email", "eval@example.invalid")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "Seed")
    task_spec = importlib.util.spec_from_file_location("bench", CODE / "eval/run_eval.py")
    bench = importlib.util.module_from_spec(task_spec)
    task_spec.loader.exec_module(bench)
    os.environ["PS_TEST_COMMAND"] = subprocess.list2cmdline([sys.executable, "-B", "-m", "unittest", "discover", "-q"])
    os.environ["PS_ROUTER_MODE"] = "route"
    args = dict(task=bench.TASKS[category], workdir=str(work), category=category,
                model="edge0_120b", max_turns=30, context_budget_tokens=30000)
    start = time.monotonic()
    res = loop.implement(args)
    status = git(work, "status", "--porcelain").stdout.decode()
    record("route", category=category, seconds=time.monotonic()-start,
           source_status=status, result=res)
    # This is a proposal smoke test. Never apply a generated patch to user code.
    os.environ.pop("PS_ROUTER_MODE")

record("manifest", commit=git(CODE, "rev-parse", "HEAD").stdout.decode().strip(),
       protocol="6-minute natural-load observation, existing categories only; injected faults; no promotion")
start = time.monotonic()
# Keep one health-history process for the actual default five-minute startup gate.
for index in range(13):
    health = router.probe(os.environ["PS_ENDPOINT"])
    record("health", elapsed=time.monotonic()-start, health=health,
           decision=router.decide("bug1", 100, health),
           inference=request("Return only the number 2.") if index % 2 == 0 else None)
    if index < 12:
        time.sleep(max(0, start + (index+1)*30 - time.monotonic()))

for category in ("bug1", "multifile", "feature"):
    route_case(category)

class Proxy(BaseHTTPRequestHandler):
    mode = "oom_once"
    count = 0
    def log_message(self, *args):
        pass
    def do_POST(self):
        type(self).count += 1
        n = type(self).count
        body = self.rfile.read(int(self.headers["Content-Length"]))
        if self.mode == "timeout_once" and n == 1:
            # Deliberately no backend work on the dropped request. This does not
            # model duplicate inference after a real server-side prefill stall.
            time.sleep(11)
            self.close_connection = True
            return
        bad = self.mode == "oom_always" or (n == 1 and self.mode in {"oom_once", "bad_request"})
        if bad:
            data = json.dumps({"error": "injected out of memory" if self.mode != "bad_request" else "injected invalid request"}).encode()
            self.send_response(400)
        else:
            with urlopen(Request("http://127.0.0.1:8000/v1/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"}), timeout=180) as response:
                data = response.read()
            self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

server = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
threading.Thread(target=server.serve_forever, daemon=True).start()
os.environ["PS_ENDPOINT"] = f"http://127.0.0.1:{server.server_port}/v1"
for mode in ("oom_once", "bad_request", "oom_always", "timeout_once"):
    Proxy.mode, Proxy.count = mode, 0
    result = request("Return only the number 2.", timeout=10 if mode == "timeout_once" else None)
    record("injected_fault", mode=mode, requests=Proxy.count, result=result)
server.shutdown()
server.server_close()
os.environ["PS_ENDPOINT"] = "http://127.0.0.1:8000/v1"
prompt = "The secret marker is cobalt-river-739.\n" + "word " * 28000 + "\nReturn only the secret marker from the beginning."
(OUT / "long-context-prompt.txt").write_text(prompt, encoding="utf-8")
record("long_context", result=request(prompt, tokens=64))
record("complete", health=router.probe(os.environ["PS_ENDPOINT"]))
