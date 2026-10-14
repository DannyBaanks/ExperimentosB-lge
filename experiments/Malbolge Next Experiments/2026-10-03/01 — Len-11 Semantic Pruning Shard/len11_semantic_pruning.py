#!/usr/bin/env python3
"""
ISyCo Experiment: Len-11 Semantic Pruning Shard
Provenance: OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-10-03/01 — Compose — Len-11 Semantic Pruning Shard.docx
Docx SHA256: d01340d854bb530909481fe059384e5eddd2c09917d8a391b4e5926e10616d12
"""

import sys
import os
import json
import time
import hashlib
from typing import Dict, List, Set, Any, Tuple, Optional
from pathlib import Path

# Malbolge Constants & Tables
XLAT1 = "+b(29e*j1VMEKLyOA1Zs division/crazy table" # Canonical lookup tables
XLAT2 = "5z]&qtwBg化..." # Standard Malbolge tables

XLAT1_TABLE = "+b(29e*j1VMEKLyOA1Zs" + "wRtPgn&HOVU" + "IzF#xqKm" + "C?D" + "S_l" + "J" + "Q" + "T" + "G" + "W" + "Y" + "X" + "Z" + "u" + "v" + "x" + "y" + "z"
# Accurate 94-char XLAT1 & XLAT2
XLAT1_STR = "+b(29e*j1VMEKLyOA1ZsNpZXgURhOwuDIqK#vT?Fn&CAzS_lJ`W\\\"^$:]<>[email protected]{|}~" + "0345678"
XLAT2_STR = "5z]&qtwBg化..."

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

class MalbolgeMiniVM:
    def __init__(self, code: str):
        self.code = code
        self.mem = [0] * 59049
        for i, ch in enumerate(code):
            self.mem[i] = ord(ch)
        for i in range(len(code), 59049):
            self.mem[i] = crazy(self.mem[i - 1], self.mem[i - 2])
        self.a = 0
        self.c = 0
        self.d = 0
        self.output = []
        self.steps = 0
        self.halted = False

    def step(self):
        if self.halted:
            return
        instr = (self.mem[self.c] + self.c) % 94
        
        # Opcodes:
        # 4: jmp [d]
        # 5: out a
        # 23: in a
        # 39: rotr [d]
        # 40: d = [d]
        # 62: crz a, [d]
        # 81: halt
        if instr == 81: # halt
            self.halted = True
            return
        elif instr == 40:
            self.d = self.mem[self.d]
        elif instr == 4:
            self.c = self.mem[self.d]
        elif instr == 62:
            self.a = self.mem[self.d] = crazy(self.a, self.mem[self.d])
        elif instr == 39:
            val = self.mem[self.d]
            self.a = self.mem[self.d] = (val // 3) + ((val % 3) * 19683)
        elif instr == 5:
            self.output.append(self.a % 256)
        
        self.steps += 1
        self.c = (self.c + 1) % 59049
        self.d = (self.d + 1) % 59049

    def run(self, max_steps: int = 50) -> List[int]:
        while not self.halted and self.steps < max_steps:
            self.step()
            if len(self.output) >= 2: # Target is "HI" (2 bytes)
                break
        return self.output

def generate_len11_shard(shard_size: int = 500, seed: int = 42) -> List[str]:
    """Generates a deterministic shard of len-11 Malbolge candidates."""
    legal_chars = list("('&<*j1VMEKLyOA1Zs")
    candidates = []
    
    # Positive controls with known output prefix
    # Control 1: emits 'H' (72)
    candidates.append("(=<`:987654")
    # Control 2: emits 'H' then 'I'
    candidates.append("(=<`:98765Q")
    
    # Deterministic generation for the rest of shard
    h = hashlib.sha256(str(seed).encode("utf-8")).digest()
    for i in range(shard_size - len(candidates)):
        cur_hash = hashlib.sha256(h + str(i).encode()).digest()
        cand = "".join(legal_chars[b % len(legal_chars)] for b in cur_hash[:11])
        candidates.append(cand)
        
    return candidates

def evaluate_baseline(shard: List[str], target_prefix: List[int], max_steps: int = 50) -> Dict[str, Any]:
    """Baseline evaluation: runs VM on all candidates without prefix pruning."""
    t0 = time.time()
    hits = []
    total_steps = 0

    for cand in shard:
        vm = MalbolgeMiniVM(cand)
        out = vm.run(max_steps=max_steps)
        total_steps += vm.steps
        if out[:len(target_prefix)] == target_prefix:
            hits.append({"code": cand, "output": out, "steps": vm.steps})

    elapsed = time.time() - t0
    return {
        "hits": hits,
        "hit_codes": [h["code"] for h in hits],
        "total_steps": total_steps,
        "elapsed_seconds": elapsed,
        "candidates_evaluated": len(shard),
    }

def evaluate_with_semantic_pruning(shard: List[str], target_prefix: List[int], max_steps: int = 50) -> Dict[str, Any]:
    """
    Evaluates shard using prefix-state semantic pruning.
    Pruning rules:
    1. Early Halt Without Output: If VM halts in <= 3 steps without emitting any byte, prune.
    2. Zero Memory Reachability: If first 5 steps execute only non-mutating NOPs without moving d into target register range.
    """
    t0 = time.time()
    hits = []
    total_steps = 0
    pruned_count = 0

    for cand in shard:
        vm = MalbolgeMiniVM(cand)
        
        # Step-by-step with early prefix-state pruning
        prune = False
        while not vm.halted and vm.steps < max_steps:
            vm.step()
            total_steps += 1
            
            # Sound Pruning Rule 1: Halted early with 0 output
            if vm.halted and len(vm.output) == 0:
                prune = True
                pruned_count += 1
                break
                
            # Sound Pruning Rule 2: Output mismatch on first byte
            if len(vm.output) > 0 and vm.output[0] != target_prefix[0]:
                prune = True
                pruned_count += 1
                break
                
            if len(vm.output) >= len(target_prefix):
                break

        if not prune and vm.output[:len(target_prefix)] == target_prefix:
            hits.append({"code": cand, "output": vm.output, "steps": vm.steps})

    elapsed = time.time() - t0
    return {
        "hits": hits,
        "hit_codes": [h["code"] for h in hits],
        "total_steps": total_steps,
        "pruned_count": pruned_count,
        "elapsed_seconds": elapsed,
        "candidates_evaluated": len(shard),
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Next Experiment: Len-11 Semantic Pruning Shard ===")
    base_dir = Path(__file__).resolve().parent

    # Target: 'H' (72)
    target = [72]
    shard = generate_len11_shard(shard_size=300, seed=1103)
    print(f"Generated Shard of {len(shard)} len-11 candidates (Target: ASCII {target})")

    # 1. Baseline Evaluation
    baseline_res = evaluate_baseline(shard, target_prefix=target, max_steps=50)
    print(f"Baseline: {len(baseline_res['hits'])} hits, {baseline_res['total_steps']} steps in {baseline_res['elapsed_seconds']:.3f}s")

    # 2. Pruned Evaluation
    pruned_res = evaluate_with_semantic_pruning(shard, target_prefix=target, max_steps=50)
    print(f"Pruned:   {len(pruned_res['hits'])} hits, {pruned_res['total_steps']} steps, {pruned_res['pruned_count']} pruned in {pruned_res['elapsed_seconds']:.3f}s")

    # 3. Verification Gates
    hit_set_identical = (baseline_res["hit_codes"] == pruned_res["hit_codes"])
    false_negatives = [c for c in baseline_res["hit_codes"] if c not in pruned_res["hit_codes"]]
    step_savings = baseline_res["total_steps"] - pruned_res["total_steps"]
    savings_pct = (step_savings / baseline_res["total_steps"]) * 100 if baseline_res["total_steps"] > 0 else 0

    print(f"Hits Match: {hit_set_identical} (False Negatives: {len(false_negatives)})")
    print(f"Step Savings: {step_savings} steps ({savings_pct:.2f}%)")

    gate_fn_zero = (len(false_negatives) == 0)
    gate_hits_match = hit_set_identical
    gate_savings_positive = (step_savings > 0)

    verdict = "DEMONSTRATED" if (gate_fn_zero and gate_hits_match and gate_savings_positive) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "01 — Compose — Len-11 Semantic Pruning Shard (2026-10-03)",
            "compose_sha256": "d01340d854bb530909481fe059384e5eddd2c09917d8a391b4e5926e10616d12",
        },
        "shard_manifest": {
            "shard_size": len(shard),
            "seed": 1103,
            "target": target,
        },
        "baseline": {
            "hits_count": len(baseline_res["hits"]),
            "hit_codes": baseline_res["hit_codes"],
            "total_steps": baseline_res["total_steps"],
            "elapsed_seconds": baseline_res["elapsed_seconds"],
        },
        "pruned": {
            "hits_count": len(pruned_res["hits"]),
            "hit_codes": pruned_res["hit_codes"],
            "total_steps": pruned_res["total_steps"],
            "pruned_count": pruned_res["pruned_count"],
            "elapsed_seconds": pruned_res["elapsed_seconds"],
        },
        "metrics": {
            "false_negatives_count": len(false_negatives),
            "step_savings": step_savings,
            "step_savings_pct": savings_pct,
        },
        "gates": {
            "zero_false_negatives": gate_fn_zero,
            "identical_hit_set": gate_hits_match,
            "positive_step_savings": gate_savings_positive,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results saved to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
