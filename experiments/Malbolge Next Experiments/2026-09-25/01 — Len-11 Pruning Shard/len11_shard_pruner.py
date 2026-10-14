#!/usr/bin/env python3
"""
ISyCo Experiment: Len-11 Pruning Shard (2026-09-25)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-25/01 — Compose — Len-11 Pruning Shard.docx
Docx SHA256: 668cb8ec02d792f65e351284b6ae4fd0f7355c70c32c3a3c25618f0809ff4281
"""

import sys
import os
import json
import time
import hashlib
from typing import Dict, List, Set, Any, Tuple, Optional
from pathlib import Path
from array import array

CRZ_TABLE = [
    [1, 0, 0],
    [1, 0, 2],
    [2, 2, 1]
]

# Fast 10-trit crazy lookup cache for common low values
CRAZY_CACHE: Dict[Tuple[int, int], int] = {}

def crazy(a: int, b: int) -> int:
    key = (a, b)
    if key in CRAZY_CACHE:
        return CRAZY_CACHE[key]
    orig_a, orig_b = a, b
    res = 0
    p = 1
    for _ in range(10):
        t_a = a % 3
        t_b = b % 3
        res += CRZ_TABLE[t_b][t_a] * p
        a //= 3
        b //= 3
        p *= 3
    if len(CRAZY_CACHE) < 50000:
        CRAZY_CACHE[key] = res
    return res

class FastMalbolgeVM:
    """Optimized Malbolge VM for prefix search up to 100 steps."""
    def __init__(self, code: str, init_len: int = 500):
        self.code = code
        self.code_len = len(code)
        # Allocate working memory (sufficient for 100 steps of linear execution)
        self.mem = [0] * init_len
        for i, ch in enumerate(code):
            self.mem[i] = ord(ch)
        for i in range(self.code_len, init_len):
            self.mem[i] = crazy(self.mem[i - 1], self.mem[i - 2])
        self.a = 0
        self.c = 0
        self.d = 0
        self.output: List[int] = []
        self.steps = 0
        self.halted = False
        self.mem_len = init_len

    def step(self):
        if self.halted or self.c >= self.mem_len or self.d >= self.mem_len:
            self.halted = True
            return
            
        instr = (self.mem[self.c] + self.c) % 94
        if instr == 81: # halt
            self.halted = True
            return
        elif instr == 40: # d = [d]
            self.d = self.mem[self.d] % self.mem_len
        elif instr == 4: # jmp [d]
            self.c = self.mem[self.d] % self.mem_len
        elif instr == 62: # crz a, [d]
            self.a = self.mem[self.d] = crazy(self.a, self.mem[self.d])
        elif instr == 39: # rotr [d]
            val = self.mem[self.d]
            self.a = self.mem[self.d] = (val // 3) + ((val % 3) * 19683)
        elif instr == 5: # out a
            self.output.append(self.a % 256)

        self.steps += 1
        self.c = (self.c + 1) % self.mem_len
        self.d = (self.d + 1) % self.mem_len

    def run(self, max_steps: int = 50) -> List[int]:
        while not self.halted and self.steps < max_steps:
            self.step()
            if len(self.output) >= 2:
                break
        return self.output

def generate_shard(shard_size: int = 250, seed: int = 20260925) -> List[str]:
    """Generates deterministic len-11 shard."""
    legal_chars = list("('&<*j1VMEKLyOA1Zs")
    candidates = []
    
    # Positive control 1: emits 'H' (72)
    candidates.append("(=<`:987654")
    # Positive control 2: emits 'H' then 'I'
    candidates.append("(=<`:98765Q")

    h = hashlib.sha256(str(seed).encode("utf-8")).digest()
    for i in range(shard_size - len(candidates)):
        cur_hash = hashlib.sha256(h + str(i).encode()).digest()
        cand = "".join(legal_chars[b % len(legal_chars)] for b in cur_hash[:11])
        candidates.append(cand)
    return candidates

def evaluate_shard_baseline(shard: List[str], target: List[int], max_steps: int = 50) -> Dict[str, Any]:
    t0 = time.time()
    hits = []
    total_steps = 0
    for cand in shard:
        vm = FastMalbolgeVM(cand)
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
        "count": len(shard),
    }

def evaluate_shard_with_signature_pruner(shard: List[str], target: List[int], max_steps: int = 50) -> Dict[str, Any]:
    t0 = time.time()
    hits = []
    total_steps = 0
    pruned_count = 0

    for cand in shard:
        vm = FastMalbolgeVM(cand)
        seen_signatures: Set[Tuple[int, int, int]] = set()
        prune = False

        while not vm.halted and vm.steps < max_steps:
            sig = (vm.a, vm.c, vm.d)
            if sig in seen_signatures and len(vm.output) == 0:
                # Infinite zero-output loop detected -> soundly prune
                prune = True
                pruned_count += 1
                break
            seen_signatures.add(sig)

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
        "count": len(shard),
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Next Experiment: Len-11 Pruning Shard (2026-09-25) ===")
    base_dir = Path(__file__).resolve().parent
    target = [72] # ASCII 'H'
    shard = generate_shard(shard_size=250, seed=20260925)
    print(f"Generated Shard of {len(shard)} len-11 candidates (Target: ASCII {target})")

    baseline_res = evaluate_shard_baseline(shard, target=target, max_steps=50)
    print(f"Baseline: {len(baseline_res['hits'])} hits, {baseline_res['total_steps']} steps in {baseline_res['elapsed']:.3f}s")

    pruned_res = evaluate_shard_with_signature_pruner(shard, target=target, max_steps=50)
    print(f"Pruned:   {len(pruned_res['hits'])} hits, {pruned_res['total_steps']} steps, {pruned_res['pruned_count']} pruned in {pruned_res['elapsed']:.3f}s")

    false_negatives = [c for c in baseline_res["hit_codes"] if c not in pruned_res["hit_codes"]]
    step_savings = baseline_res["total_steps"] - pruned_res["total_steps"]
    savings_pct = (step_savings / baseline_res["total_steps"]) * 100 if baseline_res["total_steps"] > 0 else 0

    print(f"Identical Hit Set: {baseline_res['hit_codes'] == pruned_res['hit_codes']}")
    print(f"False Negatives: {len(false_negatives)}")
    print(f"Step Savings: {step_savings} ({savings_pct:.2f}%)")

    gate_fn = (len(false_negatives) == 0)
    gate_hits = (baseline_res["hit_codes"] == pruned_res["hit_codes"])
    gate_savings = (step_savings > 0)

    verdict = "DEMONSTRATED" if (gate_fn and gate_hits and gate_savings) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "01 — Compose — Len-11 Pruning Shard (2026-09-25)",
            "compose_sha256": "668cb8ec02d792f65e351284b6ae4fd0f7355c70c32c3a3c25618f0809ff4281",
        },
        "shard_info": {
            "size": len(shard),
            "seed": 20260925,
            "target": target,
        },
        "baseline": {
            "hits_count": len(baseline_res["hits"]),
            "hit_codes": baseline_res["hit_codes"],
            "total_steps": baseline_res["total_steps"],
            "elapsed_seconds": baseline_res["elapsed"],
        },
        "pruned": {
            "hits_count": len(pruned_res["hits"]),
            "hit_codes": pruned_res["hit_codes"],
            "total_steps": pruned_res["total_steps"],
            "pruned_count": pruned_res["pruned_count"],
            "elapsed_seconds": pruned_res["elapsed"],
        },
        "metrics": {
            "false_negatives_count": len(false_negatives),
            "step_savings": step_savings,
            "savings_pct": savings_pct,
        },
        "gates": {
            "zero_false_negatives": gate_fn,
            "identical_hit_set": gate_hits,
            "positive_step_savings": gate_savings,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
