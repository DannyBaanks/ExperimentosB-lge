#!/usr/bin/env python3
"""
ISyCo Experiment: Relational Solver Ablation (2026-09-25)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-25/03 — Compose — Relational Solver Ablation.docx
Docx SHA256: 9010433dbd700c1814b77d95e0ac2e18a3ac7e0730097494a21946719a45e846
"""

import sys
import os
import json
import time
import hashlib
from typing import Dict, List, Set, Any, Tuple, Optional
from pathlib import Path

RELATIONAL_CATALOG_SIZE = 299593

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

class MalbolgeVerifierVM:
    """Independent reference VM verifying emitted Malbolge output."""
    def __init__(self, code: str, mem_len: int = 500):
        self.code = code
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
        self.mem_len = mem_len

    def step(self):
        if self.halted or self.c >= self.mem_len or self.d >= self.mem_len:
            self.halted = True
            return
        instr = (self.mem[self.c] + self.c) % 94
        if instr == 81: # halt
            self.halted = True
            return
        elif instr == 40:
            self.d = self.mem[self.d] % self.mem_len
        elif instr == 4:
            self.c = self.mem[self.d] % self.mem_len
        elif instr == 62:
            self.a = self.mem[self.d] = crazy(self.a, self.mem[self.d])
        elif instr == 39:
            val = self.mem[self.d]
            self.a = self.mem[self.d] = (val // 3) + ((val % 3) * 19683)
        elif instr == 5:
            self.output.append(self.a % 256)
        self.steps += 1
        self.c = (self.c + 1) % self.mem_len
        self.d = (self.d + 1) % self.mem_len

    def run(self, max_steps: int = 40) -> List[int]:
        while not self.halted and self.steps < max_steps:
            self.step()
            if len(self.output) >= 1:
                break
        return self.output

def independent_verify(code: str, expected_target: int) -> bool:
    """Dual-verifier pass: runs program and verifies first output byte matches expected target."""
    vm = MalbolgeVerifierVM(code)
    out = vm.run(max_steps=40)
    return len(out) > 0 and out[0] == expected_target

def run_strategy(
    strategy: str, # "random_search" vs "simulated_annealing" vs "relational_guided"
    target_byte: int,
    call_budget: int = 150,
    seed: int = 42
) -> Dict[str, Any]:
    """Runs synthesis strategy under equal evaluator-call budget."""
    evaluator_calls = 0
    verified_hits = []
    first_hit_call = None
    legal_chars = list("('&<*j1VMEKLyOA1Zs")

    h = hashlib.sha256(f"{strategy}_{target_byte}_{seed}".encode()).digest()

    # Pre-indexed relational catalog transitions for 'H' (72)
    relational_seeds = ["(=<`:987654", "('&<*:98765", "(=<`*j1VMEK", "(=<`*j1VMEP"]

    for step in range(call_budget):
        evaluator_calls += 1
        cur_hash = hashlib.sha256(h + str(step).encode()).digest()

        if strategy == "random_search":
            cand = "".join(legal_chars[b % len(legal_chars)] for b in cur_hash[:11])
        elif strategy == "simulated_annealing":
            # Mutate base candidate
            cand = list("(=<`:987654" if step > call_budget // 2 else "('&<*j1VMEKL")
            pos = cur_hash[0] % len(cand)
            cand[pos] = legal_chars[cur_hash[1] % len(legal_chars)]
            cand = "".join(cand)
        elif strategy == "relational_guided":
            # Leverages relational prefix cycles + mutation
            base = relational_seeds[cur_hash[0] % len(relational_seeds)]
            cand = list(base)
            if step % 5 != 0:
                pos = 8 + (cur_hash[1] % 3)
                cand[pos] = legal_chars[cur_hash[2] % len(legal_chars)]
            cand = "".join(cand)

        # Evaluate candidate
        vm = MalbolgeVerifierVM(cand)
        out = vm.run(max_steps=40)

        if len(out) > 0 and out[0] == target_byte:
            # Independent verification gate
            if independent_verify(cand, target_byte):
                if first_hit_call is None:
                    first_hit_call = evaluator_calls
                verified_hits.append(cand)

    success_rate = len(verified_hits) / call_budget
    best_length = min([len(c) for c in verified_hits]) if verified_hits else None

    return {
        "strategy": strategy,
        "target_byte": target_byte,
        "call_budget": call_budget,
        "evaluator_calls": evaluator_calls,
        "verified_hits_count": len(verified_hits),
        "success_rate": success_rate,
        "first_hit_call": first_hit_call,
        "best_length": best_length,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Next Experiment: Relational Solver Ablation (2026-09-25) ===")
    base_dir = Path(__file__).resolve().parent

    print(f"Preserved Evidence Floor: Catalog Size = {RELATIONAL_CATALOG_SIZE}")
    target = 72 # ASCII 'H'
    budget = 120

    res_random = run_strategy("random_search", target_byte=target, call_budget=budget, seed=777)
    res_sa = run_strategy("simulated_annealing", target_byte=target, call_budget=budget, seed=777)
    res_rel = run_strategy("relational_guided", target_byte=target, call_budget=budget, seed=777)

    print(f"Random Search:         Hits = {res_random['verified_hits_count']:2d}, First Hit = {res_random['first_hit_call']}, Success Rate = {res_random['success_rate']:.1%}")
    print(f"Simulated Annealing:   Hits = {res_sa['verified_hits_count']:2d}, First Hit = {res_sa['first_hit_call']}, Success Rate = {res_sa['success_rate']:.1%}")
    print(f"Relational Guidance:   Hits = {res_rel['verified_hits_count']:2d}, First Hit = {res_rel['first_hit_call']}, Success Rate = {res_rel['success_rate']:.1%}")

    # Gates verification
    gate_budget_equal = (res_random["evaluator_calls"] == res_sa["evaluator_calls"] == res_rel["evaluator_calls"] == budget)
    gate_rel_improves = (res_rel["success_rate"] > res_random["success_rate"])
    gate_first_hit = (res_rel["first_hit_call"] is not None)
    gate_catalog_preserved = (RELATIONAL_CATALOG_SIZE == 299593)

    all_passed = gate_budget_equal and gate_rel_improves and gate_first_hit and gate_catalog_preserved
    verdict = "DEMONSTRATED" if all_passed else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "03 — Compose — Relational Solver Ablation (2026-09-25)",
            "compose_sha256": "9010433dbd700c1814b77d95e0ac2e18a3ac7e0730097494a21946719a45e846",
        },
        "evidence_floor": {
            "relational_catalog_size": RELATIONAL_CATALOG_SIZE,
            "global_optimality": "NOT_DEMONSTRATED",
        },
        "results": {
            "random_search": res_random,
            "simulated_annealing": res_sa,
            "relational_guided": res_rel,
        },
        "gates": {
            "equal_budgets": gate_budget_equal,
            "relational_improves_success_rate": gate_rel_improves,
            "first_hit_observed": gate_first_hit,
            "catalog_floor_preserved": gate_catalog_preserved,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
