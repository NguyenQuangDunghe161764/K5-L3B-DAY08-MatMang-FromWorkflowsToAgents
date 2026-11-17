"""Run with python -m tests.ablation_ticket; official fixtures stay unchanged."""
import copy
import json
from pathlib import Path

from lab8.benchmark import run_benchmark
from lab8.config_loader import repo_path
from lab8.db import load_json, load_jsonl


def main():
    world = load_json(repo_path("data", "public_world_state.json"))
    baseline = load_jsonl(repo_path("data", "public_claims.jsonl"))
    variant = copy.deepcopy(baseline)
    claim = next(c for c in variant if c["claim_id"] == "C-002")
    assert "5 ngày" in claim["ticket"]
    claim["ticket"] = claim["ticket"].replace("5 ngày", "2 ngày")
    for name, claims in [("baseline", baseline), ("aligned_ticket", variant)]:
        report = run_benchmark(world=world, claims=claims,
                               shapes=["workflow", "single", "orchestrator", "swarm"],
                               seeds=[11, 22, 33, 44, 55])
        out = Path("reports") / f"ablation_{name}.json"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(out)
        for shape, stats in report["by_shape"].items():
            print(shape, stats["pass_rate"], stats["pass_5"], stats["cost_per_success_vnd"])


if __name__ == "__main__":
    main()
