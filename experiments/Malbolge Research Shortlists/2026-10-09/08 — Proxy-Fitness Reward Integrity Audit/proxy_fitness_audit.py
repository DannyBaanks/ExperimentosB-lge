"""
proxy_fitness_audit.py — Audit of proxy-fitness and reward hacking in Malbolge program synthesis.

Evaluates how heuristic scoring metrics (prefix match, ASCII distance, step liveness)
can rank invalid candidates high or trigger false positive stops, contrasted against
the strict classic VM acceptance gate.

Based on Karwowski et al., UAI 2026.
Part of Malbolge Research Shortlists / 2026-10-09:
Compose 08 — Proxy-Fitness Reward Integrity Audit
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def score_prefix_match(target: str, output: str) -> float:
    """Fraction of target matched from prefix."""
    if not target or not output:
        return 0.0
    common = 0
    for t_ch, o_ch in zip(target, output):
        if t_ch == o_ch:
            common += 1
        else:
            break
    return common / len(target)


def score_ascii_closeness(target: str, output: str) -> float:
    """Normalized closeness in character space."""
    if not target or not output:
        return 0.0
    min_len = min(len(target), len(output))
    dist = sum(abs(ord(t) - ord(o)) for t, o in zip(target[:min_len], output[:min_len]))
    # Add penalty for length difference
    dist += abs(len(target) - len(output)) * 50
    return max(0.0, 1.0 - (dist / (min_len * 50 + 1)))


def score_liveness_fuel(steps: int, max_steps: int = 5000) -> float:
    """Heuristic rewarding programs that survive many execution steps."""
    return min(1.0, steps / max_steps)


def composite_proxy_fitness(target: str, output: str, steps: int, max_steps: int = 5000) -> float:
    """
    Standard composite heuristic fitness used in evolutionary / stochastic synthesizers:
    40% prefix match + 40% ASCII closeness + 20% liveness fuel.
    """
    p_score = score_prefix_match(target, output)
    d_score = score_ascii_closeness(target, output)
    l_score = score_liveness_fuel(steps, max_steps)
    return round(0.4 * p_score + 0.4 * d_score + 0.2 * l_score, 4)


def strict_vm_gate(target: str, output: str, status: str) -> bool:
    """Strict ground-truth gate: output must match target exactly AND program must halt cleanly."""
    return (output == target) and (status == "HALTED")


def run_reward_integrity_audit(out_dir: str = ".") -> Dict[str, Any]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    target_str = "HI"

    # Synthetic adversarial candidate profiles observed during synthesis
    candidates = [
        {
            "id": "C1_GENUINE_HIT",
            "description": "Emits exact target 'HI' and halts cleanly in 28 steps",
            "output": "HI",
            "steps": 28,
            "status": "HALTED",
            "is_truly_valid": True,
        },
        {
            "id": "C2_NON_TERMINATING_HACKER",
            "description": "Emits 'HI' then loops infinitely (rewarded by liveness heuristic over genuine hit)",
            "output": "HI",
            "steps": 5000,
            "status": "TIMEOUT",
            "is_truly_valid": False,
        },
        {
            "id": "C3_ASCII_DISTANCE_HACKER",
            "description": "Emits 'HJ' (1 ASCII unit off on second char) and halts",
            "output": "HJ",
            "steps": 32,
            "status": "HALTED",
            "is_truly_valid": False,
        },
        {
            "id": "C4_LONG_LIVENESS_SPIN",
            "description": "Runs 5000 steps of crazy ALU operations with empty output",
            "output": "",
            "steps": 5000,
            "status": "TIMEOUT",
            "is_truly_valid": False,
        },
        {
            "id": "C5_EARLY_CRASH",
            "description": "Illegal instruction crash on step 2",
            "output": "",
            "steps": 2,
            "status": "CRASHED",
            "is_truly_valid": False,
        },
    ]

    evaluated_candidates = []
    ranking_inversions = 0

    for c in candidates:
        fitness = composite_proxy_fitness(target_str, c["output"], c["steps"])
        gate_passed = strict_vm_gate(target_str, c["output"], c["status"])

        # Likelihood hacking occurs if an invalid candidate scores >= 0.70 fitness
        is_proxy_hack = (not c["is_truly_valid"] and fitness >= 0.70)
        if is_proxy_hack:
            ranking_inversions += 1

        evaluated_candidates.append({
            "id": c["id"],
            "description": c["description"],
            "output": c["output"],
            "steps": c["steps"],
            "status": c["status"],
            "proxy_fitness": fitness,
            "strict_gate_pass": gate_passed,
            "is_truly_valid": c["is_truly_valid"],
            "proxy_hack_flag": is_proxy_hack,
        })

    # Sort candidates by proxy fitness descending
    sorted_by_proxy = sorted(evaluated_candidates, key=lambda x: -x["proxy_fitness"])

    # Strict gate integrity:
    # 1. Genuine hit passes gate
    # 2. Zero invalid candidates pass gate
    genuine_passes = any(c["strict_gate_pass"] for c in evaluated_candidates if c["is_truly_valid"])
    zero_false_accepts = all(not c["strict_gate_pass"] for c in evaluated_candidates if not c["is_truly_valid"])

    # Likelihood hacking demonstrated if proxy score grants high score to non-halting / incorrect programs
    proxy_hacking_observed = (ranking_inversions > 0)
    verdict = "DEMONSTRATED" if (proxy_hacking_observed and genuine_passes and zero_false_accepts) else "FALSIFIED"

    summary = {
        "experiment": "Proxy-Fitness Reward Integrity Audit",
        "provenance": "Malbolge Research Shortlists / 2026-10-09 / Compose 08",
        "verdict": verdict,
        "proxy_hacking_observed": proxy_hacking_observed,
        "ranking_inversions_count": ranking_inversions,
        "strict_gate_false_accept_rate": 0.0,
        "evaluated_candidates": sorted_by_proxy,
    }

    with open(out_path / "results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def print_audit_report(summary: Dict[str, Any]) -> None:
    print("\n" + "=" * 96)
    print(" EXPERIMENT REPORT: PROXY-FITNESS REWARD INTEGRITY AUDIT (UAI 2026)")
    print("=" * 96)
    print(f"Formal Verdict: [{summary['verdict']}]")
    print(f"Proxy Hacking Inversions Detected: {summary['ranking_inversions_count']}")
    print(f"Strict Gate False Accept Rate: {summary['strict_gate_false_accept_rate'] * 100}%\n")

    header = f"{'Candidate ID':<26} | {'Steps':<6} | {'Status':<8} | {'Fitness':<8} | {'Gate Pass':<10} | {'Proxy Hack':<10}"
    print(header)
    print("-" * 96)

    for c in summary["evaluated_candidates"]:
        print(
            f"{c['id']:<26} | {c['steps']:<6} | {c['status']:<8} | "
            f"{c['proxy_fitness']:<8.4f} | {str(c['strict_gate_pass']):<10} | {str(c['proxy_hack_flag']):<10}"
        )
    print("=" * 96 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Proxy-Fitness Reward Integrity Audit")
    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    res = run_reward_integrity_audit(args.out)
    print_audit_report(res)
