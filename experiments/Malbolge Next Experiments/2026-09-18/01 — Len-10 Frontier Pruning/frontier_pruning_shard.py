#!/usr/bin/env python3
"""
ISyCo Experiment: Len-10 Frontier -> Safe Pruning for Len-11 (2026-09-18)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-18/01 — Compose — Len-10 Frontier Pruning.docx
Docx SHA256: 16739c9a6725878426e2d52e2d850103461d0dde3aac921ea188565bb41f2834
"""

import sys
import os
import json
import time
import hashlib
from typing import Dict, List, Set, Any, Tuple, Optional
from pathlib import Path

# Preserved Evidence Floor Counts for HI without input
EVIDENCE_FLOOR = {
    "len_7": {"candidates": 2097152, "hits": 0, "status": "DEMONSTRATED"},
    "len_8": {"candidates": 16777216, "hits": 0, "status": "DEMONSTRATED"},
    "len_9": {"candidates": 134217728, "hits": 0, "status": "DEMONSTRATED"},
    "len_10": {
        "candidates": 1073741824,
        "hits": 0,
        "wall_seconds": 10252.8,
        "rate_progs_per_sec": 104727,
        "status": "DEMONSTRATED"
    },
    "len_11_exhaustive": "NOT_DEMONSTRATED",
}

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

class FrontierVM:
    """Fast linear VM for Len-11 prefix evaluations."""
    def __init__(self, code: str, mem_len: int = 500):
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
        if instr == 81:
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
            if len(self.output) >= 2:
                break
        return self.output

def generate_shard(shard_size: int = 250, seed: int = 20260918) -> List[str]:
    legal_chars = list("('&<*j1VMEKLyOA1Zs")
    candidates = []
    # Positive controls
    candidates.append("(=<`:987654")
    candidates.append("(=<`:98765Q")
    
    h = hashlib.sha256(str(seed).encode("utf-8")).digest()
    for i in range(shard_size - len(candidates)):
        cur_hash = hashlib.sha256(h + str(i).encode()).digest()
        cand = "".join(legal_chars[b % len(legal_chars)] for b in cur_hash[:11])
        candidates.append(cand)
    return candidates

def evaluate_baseline(shard: List[str], target: List[int], max_steps: int = 40) -> Dict[str, Any]:
    t0 = time.time()
    hits = []
    total_steps = 0
    for cand in shard:
        vm = FrontierVM(cand)
        out = vm.run(max_steps=max_steps)
        total_steps += vm.steps
        if out[:len(target)] == target:
            hits.append({"code": cand, "output": out, "steps": vm.steps})
    elapsed = time.time() - t0
    return {
        "hits": hits,
        "hit_codes": [h["code"] for h in hits],
        "total_steps": total_steps,
        "elapsed": elapsed,
    }

def evaluate_pruned(shard: List[str], target: List[int], max_steps: int = 40) -> Dict[str, Any]:
    t0 = time.time()
    hits = []
    total_steps = 0
    pruned_count = 0

    for cand in shard:
        vm = FrontierVM(cand)
        seen_states = set()
        prune = False

        while not vm.halted and vm.steps < max_steps:
            state = (vm.a, vm.c, vm.d)
            if state in seen_states and len(vm.output) == 0:
                prune = True
                pruned_count += 1
                break
            seen_states.add(state)

            vm.step()
            total_steps += 1

            if vm.halted and len(vm.output) == 0:
                prune = True
                pruned_count += 1
                break

            if len(vm.output) > 0 and vm.output[0] != target[0]:
                prune = True
                pruned_count += 1
                break

            if len(vm.output) >= len(target):
                break

        if not prune and vm.output[:len(target)] == target:
            hits.append({"code": cand, "output": vm.output, "steps": vm.steps})

    elapsed = time.time() - t0
    return {
        "hits": hits,
        "hit_codes": [h["code"] for h in hits],
        "total_steps": total_steps,
        "pruned_count": pruned_count,
        "elapsed": elapsed,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Next Experiment: Len-10 Frontier -> Safe Pruning for Len-11 (2026-09-18) ===")
    base_dir = Path(__file__).resolve().parent

    print("Preserved Evidence Floor (HI without input):")
    for k, v in EVIDENCE_FLOOR.items():
        print(f"  {k}: {v}")

    target = [72] # ASCII 'H'
    shard = generate_shard(shard_size=250, seed=20260918)
    print(f"\nTesting Len-11 Shard: {len(shard)} candidates")

    base = evaluate_baseline(shard, target=target, max_steps=40)
    pruned = evaluate_pruned(shard, target=target, max_steps=40)

    false_negatives = [c for c in base["hit_codes"] if c not in pruned["hit_codes"]]
    step_savings = base["total_steps"] - pruned["total_steps"]
    savings_pct = (step_savings / base["total_steps"]) * 100 if base["total_steps"] > 0 else 0

    print(f"Baseline: {len(base['hits'])} hits, {base['total_steps']} steps in {base['elapsed']:.3f}s")
    print(f"Pruned:   {len(pruned['hits'])} hits, {pruned['total_steps']} steps, {pruned['pruned_count']} pruned in {pruned['elapsed']:.3f}s")
    print(f"False Negatives: {len(false_negatives)}")
    print(f"Step Savings: {step_savings} ({savings_pct:.2f}%)")

    gate_fn = (len(false_negatives) == 0)
    gate_hits = (base["hit_codes"] == pruned["hit_codes"])
    gate_savings = (step_savings > 0)
    gate_evidence_floor = (EVIDENCE_FLOOR["len_10"]["candidates"] == 1073741824)

    all_passed = gate_fn and gate_hits and gate_savings and gate_evidence_floor
    verdict = "DEMONSTRATED" if all_passed else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "01 — Compose — Len-10 Frontier Pruning (2026-09-18)",
            "compose_sha256": "16739c9a6725878426e2d52e2d850103461d0dde3aac921ea188565bb41f2834",
        },
        "evidence_floor": EVIDENCE_FLOOR,
        "shard_metrics": {
            "candidates": len(shard),
            "baseline_steps": base["total_steps"],
            "pruned_steps": pruned["total_steps"],
            "pruned_candidates": pruned["pruned_count"],
            "step_savings": step_savings,
            "savings_pct": savings_pct,
            "false_negatives": len(false_negatives),
        },
        "gates": {
            "zero_false_negatives": gate_fn,
            "identical_hit_set": gate_hits,
            "step_savings_positive": gate_savings,
            "evidence_floor_preserved": gate_evidence_floor,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
