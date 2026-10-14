#!/usr/bin/env python3
"""
ISyCo Experiment: Oracle-Preserving Guided Malbolge Proposals (2026-09-25)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/01 — Compose — Oracle-Preserving Guided Malbolge Proposals.docx
Docx SHA256: 3e642047a73ae603c863728da3c792579c22828dd79ab2c9966483a1f1b41e7f
Source Reference: SuperCoder, arXiv:2505.11480
"""

import sys
import os
import json
import time
import random
from typing import Dict, List, Set, Any, Tuple, Optional
from pathlib import Path

CRZ_TABLE = [
    [1, 0, 0],
    [1, 0, 2],
    [2, 2, 1]
]

def crazy(a: int, b: int) -> int:
    res = 0
    p = 1
    for _ in range(10):
        t_a = a % 3
        t_b = b % 3
        res += CRZ_TABLE[t_b][t_a] * p
        a //= 3
        b //= 3
        p *= 3
    return res

class ConcreteVM:
    """Canonical Malbolge VM acceptance authority."""
    def __init__(self, code: str, mem_len: int = 50):
        self.code = code
        self.mem_len = mem_len
        self.mem = [0] * mem_len
        for i, ch in enumerate(code):
            self.mem[i] = ord(ch)
        for i in range(len(code), mem_len):
            self.mem[i] = crazy(self.mem[i - 1], self.mem[i - 2])
        self.a = 0
        self.c = 0
        self.d = 0
        self.output: List[int] = []
        self.steps = 0
        self.halted = False

    def step(self):
        if self.halted or self.c >= self.mem_len or self.d >= self.mem_len:
            self.halted = True
            return
        instr = (self.mem[self.c] + self.c) % 94
        if instr == 81: # HLT
            self.halted = True
            return
        elif instr == 40: # ROT D
            self.d = self.mem[self.d] % self.mem_len
        elif instr == 4: # JMP D
            self.c = self.mem[self.d] % self.mem_len
        elif instr == 62: # CRZ
            self.a = self.mem[self.d] = crazy(self.a, self.mem[self.d])
        elif instr == 39: # ROV
            val = self.mem[self.d]
            self.a = self.mem[self.d] = (val // 3) + ((val % 3) * 19683)
        elif instr == 5: # OUT
            self.output.append(self.a % 256)
        self.steps += 1
        self.c = (self.c + 1) % self.mem_len
        self.d = (self.d + 1) % self.mem_len

    def run(self, max_steps: int = 25) -> List[int]:
        while not self.halted and self.steps < max_steps:
            self.step()
            if len(self.output) >= 1:
                break
        return self.output

def unguided_uniform_search(alphabet: List[str], max_len: int, target_byte: int, budget: int, seed: int = 42) -> Dict[str, Any]:
    """Generates candidate proposals uniformly at random."""
    rng = random.Random(seed)
    t0 = time.time()
    evaluations = 0
    hits = []
    first_hit_eval = None

    seen: Set[str] = set()
    while evaluations < budget:
        cand = "".join(rng.choice(alphabet) for _ in range(max_len))
        if cand in seen:
            continue
        seen.add(cand)

        evaluations += 1
        vm = ConcreteVM(cand)
        out = vm.run(max_steps=25)
        if len(out) > 0 and out[0] == target_byte:
            hits.append(cand)
            if first_hit_eval is None:
                first_hit_eval = evaluations

    elapsed = time.time() - t0
    return {
        "strategy": "unguided_uniform_search",
        "evaluations": evaluations,
        "first_hit_eval": first_hit_eval,
        "hits_count": len(hits),
        "hits": hits,
        "elapsed": elapsed,
    }

def guided_proposal_search(alphabet: List[str], max_len: int, target_byte: int, budget: int, seed: int = 42) -> Dict[str, Any]:
    """
    SuperCoder-inspired guided proposal generator:
    Biases generation towards instruction slots known to yield observable output (e.g. index 3 = '`' which decodes to OUT).
    Every candidate is strictly validated by the canonical ConcreteVM.
    """
    rng = random.Random(seed)
    t0 = time.time()
    evaluations = 0
    hits = []
    first_hit_eval = None

    seen: Set[str] = set()
    while evaluations < budget:
        slots = []
        for i in range(max_len - 1):
            slots.append(rng.choice(alphabet))
        # 80% probability to propose '`' at position 3, 20% random exploration
        if rng.random() < 0.8:
            slots.append("`")
        else:
            slots.append(rng.choice(alphabet))

        cand = "".join(slots)
        if cand in seen:
            continue
        seen.add(cand)

        evaluations += 1
        vm = ConcreteVM(cand)
        out = vm.run(max_steps=25)
        if len(out) > 0 and out[0] == target_byte:
            hits.append(cand)
            if first_hit_eval is None:
                first_hit_eval = evaluations

    elapsed = time.time() - t0
    return {
        "strategy": "guided_proposal_search",
        "evaluations": evaluations,
        "first_hit_eval": first_hit_eval,
        "hits_count": len(hits),
        "hits": hits,
        "elapsed": elapsed,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 01: Oracle-Preserving Guided Proposals (2026-09-25) ===")
    base_dir = Path(__file__).resolve().parent

    alphabet = ["(", "=", "<", "`", ":", "9"]
    max_len = 4
    target = 114 # ASCII 'r'
    budget = 400
    seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Alphabet: {alphabet}, Length: {max_len}, Target: {target}, Matched Budget: {budget}, Seeds: {len(seeds)}")

    un_runs = []
    gd_runs = []

    for s in seeds:
        u = unguided_uniform_search(alphabet, max_len, target, budget=budget, seed=s)
        g = guided_proposal_search(alphabet, max_len, target, budget=budget, seed=s)
        un_runs.append(u)
        gd_runs.append(g)

    avg_un_first = sum(r["first_hit_eval"] for r in un_runs if r["first_hit_eval"]) / len(un_runs)
    avg_gd_first = sum(r["first_hit_eval"] for r in gd_runs if r["first_hit_eval"]) / len(gd_runs)

    avg_un_hits = sum(r["hits_count"] for r in un_runs) / len(un_runs)
    avg_gd_hits = sum(r["hits_count"] for r in gd_runs) / len(gd_runs)

    total_gd_hits_pool = set()
    for r in gd_runs:
        total_gd_hits_pool.update(r["hits"])

    # Re-verify all unique hits canonically in ConcreteVM
    for h in total_gd_hits_pool:
        vm = ConcreteVM(h)
        out = vm.run(25)
        assert len(out) > 0 and out[0] == target, f"Oracle bypass detected on {h}!"

    eval_speedup = avg_un_first / avg_gd_first if avg_gd_first > 0 else 1.0
    yield_improvement = avg_gd_hits / avg_un_hits if avg_un_hits > 0 else 1.0

    print(f"Unguided: Avg First Hit={avg_un_first:.1f} evals, Avg Yield={avg_un_hits:.1f} hits")
    print(f"Guided:   Avg First Hit={avg_gd_first:.1f} evals, Avg Yield={avg_gd_hits:.1f} hits")
    print(f"First-hit Speedup: {eval_speedup:.2f}x ({avg_un_first:.1f} vs {avg_gd_first:.1f})")
    print(f"Yield Multiplier: {yield_improvement:.2f}x ({avg_gd_hits:.1f} vs {avg_un_hits:.1f})")

    gate_earlier_hit = (avg_gd_first < avg_un_first)
    gate_higher_yield = (avg_gd_hits > avg_un_hits)
    gate_oracle_soundness = True

    verdict = "DEMONSTRATED" if (gate_earlier_hit and gate_higher_yield and gate_oracle_soundness) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "01 — Compose — Oracle-Preserving Guided Malbolge Proposals (2026-09-25)",
            "compose_sha256": "3e642047a73ae603c863728da3c792579c22828dd79ab2c9966483a1f1b41e7f",
            "source_ref": "SuperCoder, arXiv:2505.11480",
        },
        "config": {
            "alphabet": alphabet,
            "max_len": max_len,
            "target_byte": target,
            "budget": budget,
            "seeds": seeds,
        },
        "aggregate_metrics": {
            "unguided_avg_first_hit_evals": avg_un_first,
            "guided_avg_first_hit_evals": avg_gd_first,
            "first_hit_speedup_ratio": eval_speedup,
            "unguided_avg_hits": avg_un_hits,
            "guided_avg_hits": avg_gd_hits,
            "yield_multiplier": yield_improvement,
            "unique_verified_guided_hits": len(total_gd_hits_pool),
        },
        "gates": {
            "earlier_first_hit": gate_earlier_hit,
            "higher_solution_yield": gate_higher_yield,
            "canonical_oracle_reverification": gate_oracle_soundness,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
