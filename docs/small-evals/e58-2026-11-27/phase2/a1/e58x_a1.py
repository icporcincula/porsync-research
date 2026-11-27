#!/usr/bin/env python3
"""E58 Addendum A1 (private, NOT a comparison): Hermes-driven delivery check against a 64K-context Bonsai server.

Same as e58x_p2.run/smoke, but the server is started externally (same pinned weights/sampler, only -c 65536) and left
running; outputs go to tmp/e58x/a1 and workspaces to <LOCAL_WORKDIR>/a1work.

  python scripts/e58x_a1.py smoke
  python scripts/e58x_a1.py run [N]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e58x_p2 as M  # noqa: E402

ATTEMPT = sys.argv[3] if len(sys.argv) > 3 else "1"
M.OUT = M.ROOT / "tmp" / "e58x" / ("a1" if ATTEMPT == "1" else f"a1-attempt{ATTEMPT}")
M.WORK = Path("<LOCAL_WORKDIR>/a1work" if ATTEMPT == "1" else f"<LOCAL_WORKDIR>/a1work{ATTEMPT}")
M.OUT.mkdir(parents=True, exist_ok=True)
M.start_server = lambda: None
M.stop_server = lambda proc: None
APPLY_SENTENCE = ("If the result contains a patch_path and the status is not frontier_required, call apply_patch exactly once with that exact "
                  "patch_path. Then reply with only the final tool status.")
if ATTEMPT in ("3", "4", "5"):  # attempt 4 = attempt 3 + an instruction to call apply_patch on the returned patch_path. attempt 3: category named AND PS_* vars written to Hermes' own .env (it does not forward process env to plugins); restored after
    import atexit, shutil
    ENVF = Path("<HERMES_HOME>/.env")
    BAK = M.OUT / "hermes.env.bak"
    shutil.copy2(ENVF, BAK)
    atexit.register(lambda: shutil.copy2(BAK, ENVF))
    _orig = BAK.read_text(encoding="utf-8")
    _h3 = M.hermes

    def _hermes3(query, tag, env_extra, *a, **k):
        ENVF.write_text(_orig.rstrip("\n") + "\n" + "".join(f"{k_}={("'" + v + "'" if ATTEMPT == '5' else v)}\n" for k_, v in env_extra.items() if k_.startswith("PS_")), encoding="utf-8")
        q = query.replace('mode set to "apply", ', 'mode set to "apply", category set to "multifile", ', 1)
        if ATTEMPT in ("4", "5"):
            q = q.replace("Then reply with only the tool's status.", APPLY_SENTENCE, 1)
        return _h3(q, tag, env_extra, *a, **k)
    M.hermes = _hermes3
if ATTEMPT == "2":  # attempt 2: the instruction also names category="multifile" (attempt 1 omitted it; router escalated unknown_category)
    _h = M.hermes

    def _hermes(query, *a, **k):
        return _h(query.replace('mode set to "apply", ', 'mode set to "apply", category set to "multifile", ', 1), *a, **k)
    M.hermes = _hermes

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.argv[1] == "smoke":
        M.smoke()
    else:
        M.run(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
