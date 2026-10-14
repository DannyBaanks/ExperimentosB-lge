"""
presynthesis_oracle.py — Precomputed abstract transition oracle for Malbolge program synthesis.

Based on Dong et al., PLDI 2026 (Presynthesis / Foresighter).
Evaluates whether precomputing abstract prefix viability filters amortizes search cost
and guarantees zero false negatives against exact exhaustive VM verification.

Part of Malbolge Research Shortlists / 2026-10-09:
Compose 06 — Offline Presynthesis Oracle
"""

from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Set, Tuple

sys.path.insert(0, "/home/danny/Development/ISyCo/workspace/assembly/malbolge")
import malbolge_interpreter as mi

XLAT1 = (
    "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI"
    ".v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"
)
LEGAL_CHARS = set("ji*p</vo")


class PresynthesisOracle:
    """Precomputed abstract filter for valid and viable Malbolge prefixes."""

    def __init__(self, prefix_len: int = 3):
        self.prefix_len = prefix_len
        self._valid_char_cache: Dict[int, Set[str]] = {}
        self._build_syntax_table()

    def _build_syntax_table(self):
        """Precompute legal ASCII characters for positions 0..prefix_len-1."""
        for pos in range(self.prefix_len + 1):
            valid_set = set()
            for code in range(33, 127):
                ch = chr(code)
                instr = XLAT1[(code - 33 + pos) % 94]
                if instr in LEGAL_CHARS:
                    valid_set.add(ch)
            self._valid_char_cache[pos] = valid_set

    def is_syntax_viable(self, prefix: str) -> bool:
        """Check if all characters in prefix satisfy the position-dependent instruction set."""
        for pos, ch in enumerate(prefix[:self.prefix_len]):
            if ch not in self._valid_char_cache.get(pos, set()):
                return False
        return True

    def is_semantics_viable(self, prefix: str, target: str) -> bool:
        """
        Check abstract execution viability:
        - Must be syntax viable.
        - Cannot start with 'v' (halts immediately at step 1 with 0 outputs).
        - If first op is '<', emits \\x00, non-viable for printable ASCII targets.
        """
        if not self.is_syntax_viable(prefix):
            return False
        if not prefix:
            return True

        # Check first instruction
        first_op = XLAT1[(ord(prefix[0]) - 33) % 94]
        if first_op == 'v':
            # Halts at step 1 without emitting target
            return False
        if first_op == '<' and target and target[0] != '\x00':
            # Emits 0 byte initially (accumulator is 0)
            return False

        return True


def run_exhaustive_vm_search(
    candidates: List[str],
    target: str,
) -> Tuple[List[str], int, float]:
    """Exhaustively execute every candidate through the real Malbolge VM."""
    t0 = time.time()
    accepted = []
    vm_evaluations = 0

    for cand in candidates:
        vm_evaluations += 1
        output, steps, status = mi.run(cand, max_steps=500)
        if output.startswith(target) and status == "HALTED":
            accepted.append(cand)

    duration = time.time() - t0
    return accepted, vm_evaluations, duration


def run_presynthesis_guided_search(
    candidates: List[str],
    target: str,
    oracle: PresynthesisOracle,
) -> Tuple[List[str], int, float]:
    """Search using offline prefilter before running the real Malbolge VM."""
    t0 = time.time()
    accepted = []
    vm_evaluations = 0

    for cand in candidates:
        # Precomputed filter check
        if not oracle.is_semantics_viable(cand, target):
            continue

        # Only run VM on candidates that pass abstract viability
        vm_evaluations += 1
        output, steps, status = mi.run(cand, max_steps=500)
        if output.startswith(target) and status == "HALTED":
            accepted.append(cand)

    duration = time.time() - t0
    return accepted, vm_evaluations, duration


def run_presynthesis_benchmark(out_dir: str = ".") -> Dict[str, Any]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    target_str = "H"
    oracle = PresynthesisOracle(prefix_len=3)

    # Generate combinatorial test pool of candidate strings of length 3 (6^3 = 216 candidates)
    chars = "bCBA@?>=<;:9876543210/.-,+*)('&%$#\"!~}|{zyxwvutsrqponmlkjihgfedcba"[:6]
    candidate_pool = ["".join(p) for p in itertools.product(chars, repeat=3)]
    total_candidates = len(candidate_pool)

    # 1. Exhaustive baseline search
    ex_accepted, ex_evals, ex_time = run_exhaustive_vm_search(candidate_pool, target_str)

    # 2. Presynthesis-guided search
    ps_accepted, ps_evals, ps_time = run_presynthesis_guided_search(candidate_pool, target_str, oracle)

    # Verification:
    # Soundness: Zero False Negatives (every candidate accepted by exhaustive must be in presynthesis)
    false_negatives = set(ex_accepted) - set(ps_accepted)
    soundness_holds = (len(false_negatives) == 0)

    # Pruning efficiency:
    pruned_count = total_candidates - ps_evals
    prune_rate = pruned_count / total_candidates
    speedup = ex_time / ps_time if ps_time > 0 else 1.0

    verdict = "DEMONSTRATED" if (soundness_holds and prune_rate > 0.50) else "FALSIFIED"

    summary = {
        "experiment": "Offline Presynthesis Oracle",
        "provenance": "Malbolge Research Shortlists / 2026-10-09 / Compose 06",
        "verdict": verdict,
        "total_candidates": total_candidates,
        "soundness_verified": soundness_holds,
        "false_negatives_count": len(false_negatives),
        "exhaustive": {
            "accepted_count": len(ex_accepted),
            "vm_evaluations": ex_evals,
            "runtime_seconds": round(ex_time, 4),
        },
        "presynthesis": {
            "accepted_count": len(ps_accepted),
            "vm_evaluations": ps_evals,
            "pruned_candidates": pruned_count,
            "pruning_rate_pct": round(prune_rate * 100, 2),
            "runtime_seconds": round(ps_time, 4),
            "speedup_factor": round(speedup, 2),
        },
    }

    with open(out_path / "results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def print_presynthesis_report(summary: Dict[str, Any]) -> None:
    print("\n" + "=" * 92)
    print(" EXPERIMENT REPORT: OFFLINE PRESYNTHESIS ORACLE (PLDI 2026)")
    print("=" * 92)
    print(f"Formal Verdict: [{summary['verdict']}]")
    print(f"Soundness (Zero False Negatives): {summary['soundness_verified']}")
    print(f"Candidates Pruned: {summary['presynthesis']['pruned_candidates']} / {summary['total_candidates']} ({summary['presynthesis']['pruning_rate_pct']}%)")
    print(f"VM Calls Reduced: {summary['exhaustive']['vm_evaluations']} -> {summary['presynthesis']['vm_evaluations']}")
    print(f"Speedup Factor: {summary['presynthesis']['speedup_factor']}x\n")
    print("=" * 92 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Offline Presynthesis Oracle Benchmark")
    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    res = run_presynthesis_benchmark(args.out)
    print_presynthesis_report(res)
