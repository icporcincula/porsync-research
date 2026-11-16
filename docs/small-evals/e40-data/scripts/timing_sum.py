from pathlib import Path
import json, collections, statistics
rows = []
for l in open(Path(__file__).resolve().parents[1] / "timing/timing.jsonl", encoding="utf-8-sig"):
    l = l.strip()
    if l.startswith("{"):
        rows.append(json.loads(l))
print("n rows", len(rows), "errors", sum("error" in r for r in rows))
g = collections.defaultdict(list)
for r in rows:
    if "error" in r: continue
    s, arm, size = r["tag"].split("_")
    g[(arm, int(size))].append(r)
print("arm size n | gen tok/s median (first run1 / later runs2-5; cache state not isolated) | prefill tok/s median | wall_s median")
for size in (1000, 8000, 16000):
    for arm in "ABD":
        x = g[(arm, size)]
        if not x: continue
        cold = [r["gen_tps"] for r in x if r["run"] == 1]
        warm = [r["gen_tps"] for r in x if r["run"] > 1]
        print(f"{arm} {size:5d} n={len(x)} gen {statistics.median(cold):.1f} / {statistics.median(warm):.1f} | prefill {statistics.median(r['prompt_tps'] for r in x):.0f} | wall {statistics.median(r['wall_s'] for r in x):.1f}")
