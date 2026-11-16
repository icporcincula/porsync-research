from pathlib import Path
import csv, itertools, random, collections, statistics
rows = list(csv.DictReader(open(Path(__file__).resolve().parents[1] / "trials/trials.csv", encoding="utf-8-sig")))
def rn(x): return int(str(x).lstrip("r"))
g = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    g[r["fx"]][r["arm"]].append((rn(r["round"]), r["green"].strip().lower() == "true", float(r["secs"])))
fx = sorted(g)
print("fixture  A_pass B_pass C_pass  diff(B-A)")
d = []
for f in fx:
    a = sum(x[1] for x in g[f]["A"]); b = sum(x[1] for x in g[f]["B"]); c = sum(x[1] for x in g[f]["C"])
    d.append(b - a); print(f"{f:14s} {a} {b} {c}  {b-a:+d}")
obs = sum(d)
# exact sign-flip permutation test across fixtures (cluster = task), two-sided, on sum of B-A pass differences
nz = [x for x in d if x != 0]
cnt = tot = 0
for signs in itertools.product([1, -1], repeat=len(nz)):
    tot += 1
    if abs(sum(s * x for s, x in zip(signs, nz))) >= abs(obs): cnt += 1
print(f"observed sum diff={obs:+d} over {len(fx)} fixtures; exact sign-flip p={cnt/tot:.3f} ({len(nz)} non-zero clusters)")
# paired per-round discordance (McNemar exact, ignores clustering)
b_only = a_only = 0
for f in fx:
    A = {x[0]: x[1] for x in g[f]["A"]}; B = {x[0]: x[1] for x in g[f]["B"]}
    for r in A:
        if A[r] and not B[r]: a_only += 1
        if B[r] and not A[r]: b_only += 1
from math import comb
n = a_only + b_only
p = min(1, 2 * sum(comb(n, k) for k in range(0, min(a_only, b_only) + 1)) / 2 ** n)
print(f"discordant: A-only={a_only} B-only={b_only} McNemar exact p={p:.3f} (not cluster-aware)")
# task-cluster bootstrap CI for pass/hr ratio B/A
random.seed(1)
def stat(sample):
    out = []
    for arm in "AB":
        pas = sum(x[1] for f in sample for x in g[f][arm]); t = sum(x[2] for f in sample for x in g[f][arm])
        out.append(pas / t * 3600)
    return out
ra = stat(fx); print(f"pass/hr A={ra[0]:.2f} B={ra[1]:.2f} ratio B/A={ra[1]/ra[0]:.2f}")
rat = []
for _ in range(5000):
    s = [random.choice(fx) for _ in fx]; a, b = stat(s)
    if a > 0: rat.append(b / a)
rat.sort(); print(f"cluster-bootstrap 95% CI for B/A pass-per-hour ratio: {rat[int(.025*len(rat))]:.2f} - {rat[int(.975*len(rat))]:.2f} (n_valid={len(rat)})")
# median secs per arm, and by-fixture time ratio
for arm in "ABC":
    s = [x[2] for f in fx for x in g[f][arm]]; print(arm, "median secs", round(statistics.median(s), 1), "mean", round(statistics.mean(s), 1))
