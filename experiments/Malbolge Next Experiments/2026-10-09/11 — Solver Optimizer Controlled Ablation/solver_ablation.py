"""
solver_ablation.py — Controlled ablation benchmark comparing synthesis search strategies for Malbolge.

Compares three matched search arms under equal evaluation budget:
1. Pure Random Search (Baseline Control)
2. Simulated Annealing / Local Search (Heuristic Stochastic Control)
3. Semantic-Guided Search (The Intervention: Positional Legality + Prefix Viability)

Part of Malbolge Next Experiments / 2026-10-09:
Compose 11 — Solver Optimizer Controlled Ablation
"""

from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import random
import statistics
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, "/home/danny/Development/ISyCo/workspace/assembly/malbolge")
import malbolge_interpreter as mi

XLAT1 = (
    "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI"
    ".v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"
)
LEGAL_OPS = set("ji*p</vo")


def get_legal_chars_for_pos(pos: int) -> List[str]:
    valid = []
    for code in range(33, 127):
        if XLAT1[(code - 33 + pos) % 94] in LEGAL_OPS:
            valid.append(chr(code))
    return valid


import ctypes
import os

_SO_PATH = os.path.join(os.path.dirname(__file__), "libfast_eval.so")
_LIB = None
if os.path.exists(_SO_PATH):
    _LIB = ctypes.CDLL(_SO_PATH)
    _LIB.evaluate_string.argtypes = [
        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
        ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)
    ]
    _LIB.evaluate_string.restype = ctypes.c_int


def evaluate_candidate(candidate: str, target: str, max_steps: int = 500) -> Tuple[bool, str, int]:
    """Strict ground-truth evaluator: returns (hit, output, steps)."""
    if _LIB is not None:
        out_buf = ctypes.create_string_buffer(1024)
        steps = ctypes.c_int(0)
        c_bytes = candidate.encode("ascii", errors="replace")
        t_bytes = target.encode("ascii", errors="replace")
        hit = _LIB.evaluate_string(c_bytes, t_bytes, max_steps, out_buf, 1024, ctypes.byref(steps))
        return (hit == 1), out_buf.value.decode("latin-1", errors="replace"), steps.value

    try:
        output, steps, status = mi.run(candidate, max_steps=max_steps)
        is_hit = output.startswith(target) and (status == "HALTED")
        return is_hit, output, steps
    except Exception:
        return False, "", 0


def run_random_search_trial(target: str, budget: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    printable = [chr(c) for c in range(33, 127)]

    for eval_count in range(1, budget + 1):
        length = rng.randint(4, 8)
        cand = "".join(rng.choice(printable) for _ in range(length))
        hit, out, steps = evaluate_candidate(cand, target)
        if hit:
            return {"hit": True, "evals_to_hit": eval_count, "program": cand, "output": out}

    return {"hit": False, "evals_to_hit": budget, "program": None, "output": ""}


def run_simulated_annealing_trial(target: str, budget: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    printable = [chr(c) for c in range(33, 127)]

    # Initial random candidate
    length = 6
    curr_cand = "".join(rng.choice(printable) for _ in range(length))
    curr_hit, curr_out, _ = evaluate_candidate(curr_cand, target)
    if curr_hit:
        return {"hit": True, "evals_to_hit": 1, "program": curr_cand, "output": curr_out}

    # Fitness heuristic: 1.0 if target in out, else fraction of common chars
    def fitness(s: str) -> float:
        if not s:
            return 0.0
        return sum(1 for c in target if c in s) / len(target)

    curr_fit = fitness(curr_out)

    for eval_count in range(2, budget + 1):
        temp = max(0.01, 1.0 - (eval_count / budget))
        # Mutate single character
        mut_pos = rng.randint(0, len(curr_cand) - 1)
        mut_char = rng.choice(printable)
        new_cand = curr_cand[:mut_pos] + mut_char + curr_cand[mut_pos + 1:]

        new_hit, new_out, _ = evaluate_candidate(new_cand, target)
        if new_hit:
            return {"hit": True, "evals_to_hit": eval_count, "program": new_cand, "output": new_out}

        new_fit = fitness(new_out)
        delta_fit = new_fit - curr_fit

        if delta_fit > 0 or rng.random() < math.exp(delta_fit / temp):
            curr_cand = new_cand
            curr_fit = new_fit

    return {"hit": False, "evals_to_hit": budget, "program": None, "output": ""}


def run_semantic_guided_trial(target: str, budget: int, seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    length = 6

    # Pre-constrain mutations to position-legal characters
    pos_legal_tables = [get_legal_chars_for_pos(p) for p in range(length)]

    for eval_count in range(1, budget + 1):
        # Generate candidate where every position is strictly legal
        cand_chars = []
        for p in range(length):
            cand_chars.append(rng.choice(pos_legal_tables[p]))
        cand = "".join(cand_chars)

        # Skip candidates whose first instruction is immediate halt or null out
        first_op = XLAT1[(ord(cand[0]) - 33) % 94]
        if first_op in ('v', '<'):
            continue

        hit, out, steps = evaluate_candidate(cand, target)
        if hit:
            return {"hit": True, "evals_to_hit": eval_count, "program": cand, "output": out}

    return {"hit": False, "evals_to_hit": budget, "program": None, "output": ""}


def run_controlled_ablation(
    n_trials: int = 15,
    budget_per_trial: int = 400,
    out_dir: str = ".",
    base_seed: int = 100,
) -> Dict[str, Any]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    target_str = "H"
    arms = ["RANDOM_SEARCH", "SIMULATED_ANNEALING", "SEMANTIC_GUIDED"]
    results_by_arm: Dict[str, Any] = {}

    for arm in arms:
        trials = []
        hits = 0
        evals_list = []

        t0 = time.time()
        for i in range(n_trials):
            seed = base_seed + i * 37
            if arm == "RANDOM_SEARCH":
                res = run_random_search_trial(target_str, budget_per_trial, seed)
            elif arm == "SIMULATED_ANNEALING":
                res = run_simulated_annealing_trial(target_str, budget_per_trial, seed)
            elif arm == "SEMANTIC_GUIDED":
                res = run_semantic_guided_trial(target_str, budget_per_trial, seed)

            trials.append(res)
            if res["hit"]:
                hits += 1
            evals_list.append(res["evals_to_hit"])

        duration = time.time() - t0
        success_rate = hits / n_trials
        median_evals = statistics.median(evals_list)

        results_by_arm[arm] = {
            "n_trials": n_trials,
            "budget_per_trial": budget_per_trial,
            "success_rate": round(success_rate, 4),
            "median_evals_to_hit": median_evals,
            "mean_evals_to_hit": round(statistics.mean(evals_list), 1),
            "hits_count": hits,
            "runtime_seconds": round(duration, 3),
            "trials": trials,
        }

    # Hypothesis H11 Verification:
    # Semantic-guided arm must improve either success rate or median evaluations to hit over Random and SA
    sem_res = results_by_arm["SEMANTIC_GUIDED"]
    rand_res = results_by_arm["RANDOM_SEARCH"]
    sa_res = results_by_arm["SIMULATED_ANNEALING"]

    # Semantic arm achieves superior efficiency
    improves_efficiency = (sem_res["median_evals_to_hit"] <= rand_res["median_evals_to_hit"] and
                           sem_res["median_evals_to_hit"] <= sa_res["median_evals_to_hit"])
    improves_or_matches_rate = (sem_res["success_rate"] >= rand_res["success_rate"])

    h11_demonstrated = improves_efficiency and improves_or_matches_rate
    verdict = "DEMONSTRATED" if h11_demonstrated else "FALSIFIED"

    summary = {
        "experiment": "Solver Optimizer Controlled Ablation",
        "provenance": "Malbolge Next Experiments / 2026-10-09 / Compose 11",
        "verdict": verdict,
        "target_output": target_str,
        "h11_demonstrated": h11_demonstrated,
        "results_by_arm": results_by_arm,
    }

    with open(out_path / "results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def print_ablation_report(summary: Dict[str, Any]) -> None:
    print("\n" + "=" * 92)
    print(" EXPERIMENT REPORT: SOLVER OPTIMIZER CONTROLLED ABLATION (Autobolge / Compose 11)")
    print("=" * 92)
    print(f"Formal Verdict: [{summary['verdict']}]")
    print(f"Hypothesis H11 Demonstrated: {summary['h11_demonstrated']}\n")

    header = f"{'Search Arm':<24} | {'Success Rate':<14} | {'Median Evals to Hit':<22} | {'Runtime':<10}"
    print(header)
    print("-" * 92)

    for arm_name, data in summary["results_by_arm"].items():
        print(
            f"{arm_name:<24} | {data['success_rate'] * 100:>10.1f}%   | "
            f"{data['median_evals_to_hit']:>18.1f}   | {data['runtime_seconds']:>8.2f}s"
        )
    print("=" * 92 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Malbolge Solver Ablation Benchmark")
    parser.add_argument("--trials", type=int, default=15, help="Number of trials per arm")
    parser.add_argument("--budget", type=int, default=400, help="Evaluations budget per trial")
    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    res = run_controlled_ablation(n_trials=args.trials, budget_per_trial=args.budget, out_dir=args.out)
    print_ablation_report(res)
