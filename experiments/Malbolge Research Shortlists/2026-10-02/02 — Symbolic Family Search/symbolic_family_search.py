#!/usr/bin/env python3
"""
ISyCo Experiment: Symbolic Family Search (2026-10-02)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/02 — Compose — Symbolic Family Search.docx
Docx SHA256: beda8643978bd822d2edf6757035ebd3d2883eeacccc6421253c40a8a7db6fe8
Source Reference: Wu et al., arXiv:2604.15272 (Hierarchical symbolic families, Prism sGraph)
"""

import sys
import os
import json
import time
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
    """Deterministic VM evaluator for Malbolge programs."""
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

class SymbolicFamily:
    """
    Hierarchical symbolic family schema (Wu et al., Prism sGraph).
    Represents an equivalence class of program candidates sharing a concrete prefix
    and wildcard suffix slots: (c_0, ..., c_{k-1}, *, ..., *).
    """
    def __init__(self, prefix: str, max_len: int, alphabet: List[str]):
        self.prefix = prefix
        self.max_len = max_len
        self.alphabet = alphabet
        self.depth = len(prefix)
        self.cardinality = len(alphabet) ** (max_len - self.depth)

    def is_leaf(self) -> bool:
        return self.depth == self.max_len

    def expand(self) -> List["SymbolicFamily"]:
        """Expand family deterministically to next depth level."""
        if self.is_leaf():
            return []
        return [
            SymbolicFamily(self.prefix + ch, self.max_len, self.alphabet)
            for ch in self.alphabet
        ]

    def evaluate_filter(self, target_byte: int) -> Tuple[bool, Optional[str]]:
        """
        Level 1 Symbolic Family Filter:
        Tests whether the shared concrete prefix of this family provably violates target invariants.
        Returns (is_viable, reason).
        """
        if self.depth == 0:
            return True, None

        vm = ConcreteVM(self.prefix, mem_len=50)
        while not vm.halted:
            if vm.c >= self.depth or vm.d >= self.depth:
                break
            vm.step()
            if len(vm.output) > 0:
                if vm.output[0] != target_byte:
                    return False, f"family_emits_wrong_byte_{vm.output[0]}_ne_{target_byte}"
                else:
                    return True, "family_matches_target"
            if vm.halted:
                return False, "family_halted_before_output"

        return True, None

def exhaustive_search(alphabet: List[str], max_len: int, target_byte: int) -> Dict[str, Any]:
    """Exhaustive search baseline oracle evaluating every concrete candidate."""
    t0 = time.time()
    nodes_evaluated = 0
    hits = []

    def _dfs(current: str):
        nonlocal nodes_evaluated
        if len(current) == max_len:
            nodes_evaluated += 1
            vm = ConcreteVM(current, mem_len=50)
            out = vm.run(max_steps=25)
            if len(out) > 0 and out[0] == target_byte:
                hits.append(current)
            return

        for ch in alphabet:
            _dfs(current + ch)

    _dfs("")
    elapsed = time.time() - t0
    return {
        "strategy": "exhaustive_baseline_oracle",
        "concrete_evaluations": nodes_evaluated,
        "hits": sorted(hits),
        "hit_count": len(hits),
        "elapsed": elapsed,
    }

def two_level_symbolic_family_search(alphabet: List[str], max_len: int, target_byte: int) -> Dict[str, Any]:
    """
    Two-Level Symbolic Family Search:
    Level 1: Evaluates and prunes candidate families in bulk via symbolic prefix filter.
    Level 2: Evaluates only surviving leaf families with the concrete VM oracle.
    """
    t0 = time.time()
    total_space = len(alphabet) ** max_len
    root = SymbolicFamily("", max_len, alphabet)

    active_families = [root]
    pruned_families_count = 0
    pruned_candidates_count = 0
    prune_reasons: Dict[str, int] = {}

    # Level 1: Hierarchical expansion and family filtering
    for depth in range(max_len):
        next_active: List[SymbolicFamily] = []
        for fam in active_families:
            for child in fam.expand():
                viable, reason = child.evaluate_filter(target_byte)
                if viable:
                    next_active.append(child)
                else:
                    pruned_families_count += 1
                    pruned_candidates_count += child.cardinality
                    reason_key = reason or "family_infeasible"
                    prune_reasons[reason_key] = prune_reasons.get(reason_key, 0) + child.cardinality
        active_families = next_active

    surviving_leaf_families = active_families
    surviving_leaf_count = len(surviving_leaf_families)

    # Level 2: Concrete VM Oracle on surviving leaf candidates
    concrete_evals = 0
    hits = []
    for fam in surviving_leaf_families:
        concrete_evals += 1
        vm = ConcreteVM(fam.prefix, mem_len=50)
        out = vm.run(max_steps=25)
        if len(out) > 0 and out[0] == target_byte:
            hits.append(fam.prefix)

    elapsed = time.time() - t0
    return {
        "strategy": "two_level_symbolic_family_search",
        "total_space": total_space,
        "surviving_leaf_families": surviving_leaf_count,
        "pruned_families_count": pruned_families_count,
        "pruned_candidates_count": pruned_candidates_count,
        "prune_reasons": prune_reasons,
        "concrete_evaluations": concrete_evals,
        "hits": sorted(hits),
        "hit_count": len(hits),
        "elapsed": elapsed,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 02: Symbolic Family Search (2026-10-02) ===")
    base_dir = Path(__file__).resolve().parent

    alphabet = ["(", "=", "<", "`", ":", "9"]
    max_len = 4
    target = 114 # ASCII 'r'
    total_space = len(alphabet) ** max_len
    print(f"Alphabet: {alphabet} (|Σ|={len(alphabet)}), Max Length: {max_len}, Space: {total_space}")
    print(f"Target Output Byte: {target} (ASCII '{chr(target)}')")

    # 1. Exhaustive Baseline Oracle
    exh_res = exhaustive_search(alphabet, max_len, target)
    print(f"Exhaustive Baseline: {exh_res['concrete_evaluations']} evals, {exh_res['hit_count']} hits in {exh_res['elapsed']:.3f}s")

    # 2. Two-Level Symbolic Family Search
    fam_res = two_level_symbolic_family_search(alphabet, max_len, target)
    print(f"Symbolic Family Search: {fam_res['concrete_evaluations']} concrete evals, {fam_res['pruned_candidates_count']} candidates pruned in bulk")
    print(f"Family Hits: {fam_res['hit_count']} in {fam_res['elapsed']:.3f}s")

    # 3. Verification Gates
    hits_match = (exh_res["hits"] == fam_res["hits"])
    false_prunes = [h for h in exh_res["hits"] if h not in fam_res["hits"]]
    spurious_hits = [h for h in fam_res["hits"] if h not in exh_res["hits"]]
    eval_reduction = exh_res["concrete_evaluations"] - fam_res["concrete_evaluations"]
    reduction_ratio = eval_reduction / exh_res["concrete_evaluations"] if exh_res["concrete_evaluations"] > 0 else 0

    print(f"Result Parity: {hits_match} (False Prunes: {len(false_prunes)}, Spurious: {len(spurious_hits)})")
    print(f"Concrete VM Reduction: {reduction_ratio:.2%} ({eval_reduction} executions saved)")
    print(f"Pruning Reasons: {fam_res['prune_reasons']}")

    gate_parity = hits_match
    gate_zero_false_prunes = (len(false_prunes) == 0 and len(spurious_hits) == 0)
    gate_positive_reduction = (eval_reduction > 0)
    gate_deterministic_schema = (fam_res["surviving_leaf_families"] + fam_res["pruned_candidates_count"] == total_space)

    verdict = "DEMONSTRATED" if (gate_parity and gate_zero_false_prunes and gate_positive_reduction and gate_deterministic_schema) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "02 — Compose — Symbolic Family Search (2026-10-02)",
            "compose_sha256": "beda8643978bd822d2edf6757035ebd3d2883eeacccc6421253c40a8a7db6fe8",
            "source_ref": "Wu et al., arXiv:2604.15272 (Prism sGraph)",
        },
        "search_config": {
            "alphabet": alphabet,
            "max_len": max_len,
            "target_byte": target,
            "space_size": total_space,
        },
        "exhaustive": exh_res,
        "symbolic_family": fam_res,
        "metrics": {
            "hits_parity": hits_match,
            "exhaustive_hits": exh_res["hit_count"],
            "family_hits": fam_res["hit_count"],
            "false_prunes_count": len(false_prunes),
            "spurious_hits_count": len(spurious_hits),
            "concrete_executions_saved": eval_reduction,
            "reduction_ratio": reduction_ratio,
        },
        "gates": {
            "result_parity": gate_parity,
            "zero_false_prunes": gate_zero_false_prunes,
            "positive_eval_reduction": gate_positive_reduction,
            "deterministic_expansion_conservation": gate_deterministic_schema,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
