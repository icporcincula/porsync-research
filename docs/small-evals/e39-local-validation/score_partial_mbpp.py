"""Score only archived thinking-on samples; NOT a complete MBPP+ estimate."""
import hashlib
import json
from pathlib import Path
import shutil

if __name__ == "__main__":
    import evalplus.evaluate as evaluator
    root = Path(__file__).resolve().parent
    source = Path(r"C:\e39\evalplus\out_think\mbpp\edge0_120b_openai_temp_0.0.jsonl")
    samples = root / "partial-thinking-mbpp.jsonl"
    shutil.copyfile(source, samples)
    ids = {json.loads(line)["task_id"] for line in samples.read_text().splitlines()}
    original = evaluator.get_mbpp_plus
    problems = original()
    dataset_hash = evaluator.get_mbpp_plus_hash()
    # Preserve the standard cached reference results and tests. Only select the
    # already-generated problems, without filling missing samples with failures.
    truth = evaluator.get_groundtruth(problems, dataset_hash, evaluator.MBPP_OUTPUT_NOT_NONE_TASKS)
    evaluator.get_mbpp_plus = lambda **kwargs: {key: value for key, value in problems.items() if key in ids}
    evaluator.get_groundtruth = lambda *args: truth
    (root / "partial-mbpp-manifest.json").write_text(json.dumps({
        "source": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "selected": len(ids), "full_dataset": len(problems), "selection": "archived interrupted generation; nonrandom",
        "task_ids": sorted(ids), "dataset_hash": dataset_hash,
    }, indent=2))
    evaluator.evaluate("mbpp", samples=str(samples), parallel=2)
