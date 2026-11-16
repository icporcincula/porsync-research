"""Verify released artifact hashes and E40 headline counts (no model calls)."""
import csv
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "MANIFEST.json").read_text())
for entry in manifest["files"]:
    actual = hashlib.sha256((root / entry["path"]).read_bytes()).hexdigest()
    assert actual == entry["sha256"], entry["path"]
rows = list(csv.DictReader((root / "docs/small-evals/e40-data/trials/trials.csv").open(encoding="utf-8-sig")))
assert len(rows) == 150
for arm, expected in [("A", 9), ("B", 8), ("C", 10)]:
    group = [r for r in rows if r["arm"] == arm]
    assert len(group) == 50
    assert sum(r["green"].lower() == "true" for r in group) == expected
    print(f"{arm}: {expected}/50; {sum(float(r['secs']) for r in group):.3f} attempt seconds")
print(f"Verified {len(manifest['files'])} artifact hashes and 150 trial rows.")
