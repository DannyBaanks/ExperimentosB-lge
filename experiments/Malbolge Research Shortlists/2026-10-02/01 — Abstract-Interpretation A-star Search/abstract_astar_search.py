#!/usr/bin/env python3
"""
ISyCo Experiment: Abstract-Interpretation A* Search (2026-10-02)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/01 — Compose — Abstract-Interpretation A-star Search.docx
Docx SHA256: 6e79e1c0565d0785d1a85ebf2e56f5f73872f5a19c7c15b5dd0e3a10a88dc22d
Source Reference: Mell/Zdancewic/Bastani, arXiv:2602.14717
"""

import sys
import os
import json
import time
import heapq
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
    """Deterministic VM evaluator for complete or partial Malbolge programs."""
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

class SoundAbstractDomain:
    """
    Computes sound upper bounds for partial program prefixes.
    Guarantees zero false prunes: a prefix is pruned IF AND ONLY IF every possible
    extension of that prefix is mathematically proven unable to emit the target byte
    as its first output character.
    """
    @staticmethod
    def evaluate_prefix(prefix: str, target_byte: int) -> Tuple[float, Optional[str]]:
        code_len = len(prefix)
        if code_len == 0:
            return 0.5, None

        vm = ConcreteVM(prefix, mem_len=50)
        # Step strictly while C and D are within the concrete prefix.
        # Inside this window, memory is invariant under any suffix extension.
        while not vm.halted:
            if vm.c >= code_len or vm.d >= code_len:
                break
            vm.step()
            if len(vm.output) > 0:
                if vm.output[0] != target_byte:
                    return -1.0, f"provably_wrong_output_byte_{vm.output[0]}_ne_{target_byte}"
                else:
                    return 1.0, "prefix_matches_target"
            if vm.halted:
                return -1.0, "prefix_halted_before_target_output"

        # Heuristic upper bound estimating accumulator proximity
        diff = abs((vm.a % 256) - target_byte)
        return 1.0 / (1.0 + diff), None

def exhaustive_search(alphabet: List[str], max_len: int, target_byte: int) -> Dict[str, Any]:
    """Exhaustive search oracle exploring all programs of exact length max_len."""
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
        "strategy": "exhaustive_oracle",
        "nodes_evaluated": nodes_evaluated,
        "hits": sorted(hits),
        "hit_count": len(hits),
        "elapsed": elapsed,
    }

def abstract_astar_search(alphabet: List[str], max_len: int, target_byte: int) -> Dict[str, Any]:
    """A* search with sound abstract interpretation pruning over program prefixes."""
    t0 = time.time()
    nodes_evaluated = 0
    pruned_nodes = 0
    prune_reasons: Dict[str, int] = {}
    hits = []

    # Priority queue stores (-upper_bound, depth, prefix)
    frontier: List[Tuple[float, int, str]] = [(-0.5, 0, "")]

    while frontier:
        neg_ub, depth, prefix = heapq.heappop(frontier)

        if depth == max_len:
            nodes_evaluated += 1
            vm = ConcreteVM(prefix, mem_len=50)
            out = vm.run(max_steps=25)
            if len(out) > 0 and out[0] == target_byte:
                hits.append(prefix)
            continue

        for ch in alphabet:
            cand = prefix + ch
            ub, reason = SoundAbstractDomain.evaluate_prefix(cand, target_byte)
            if ub < 0.0:
                sub_tree_size = len(alphabet) ** (max_len - depth - 1)
                pruned_nodes += sub_tree_size
                reason_key = reason or "sound_prune"
                prune_reasons[reason_key] = prune_reasons.get(reason_key, 0) + sub_tree_size
            else:
                heapq.heappush(frontier, (-ub, depth + 1, cand))

    elapsed = time.time() - t0
    return {
        "strategy": "abstract_astar",
        "nodes_evaluated": nodes_evaluated,
        "pruned_nodes": pruned_nodes,
        "prune_reasons": prune_reasons,
        "hits": sorted(hits),
        "hit_count": len(hits),
        "elapsed": elapsed,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 01: Abstract-Interpretation A* Search (2026-10-02) ===")
    base_dir = Path(__file__).resolve().parent

    alphabet = ["(", "=", "<", "`", ":", "9"]
    max_len = 4
    target = 114 # Target output byte (ASCII 'r')
    total_space = len(alphabet) ** max_len
    print(f"Alphabet: {alphabet} (|Σ|={len(alphabet)}), Max Length: {max_len}, Space: {total_space}")
    print(f"Target Output Byte: {target} (ASCII '{chr(target)}')")

    # 1. Exhaustive Baseline Oracle
    exh_res = exhaustive_search(alphabet, max_len, target)
    print(f"Exhaustive Oracle: {exh_res['nodes_evaluated']} nodes, {exh_res['hit_count']} hits in {exh_res['elapsed']:.3f}s")

    # 2. Sound Abstract A* Search
    astar_res = abstract_astar_search(alphabet, max_len, target)
    print(f"Abstract A* Search: {astar_res['nodes_evaluated']} nodes, {astar_res['pruned_nodes']} pruned, {astar_res['hit_count']} hits in {astar_res['elapsed']:.3f}s")

    # 3. Verification Gates
    hits_match = (exh_res["hits"] == astar_res["hits"])
    false_prunes = [h for h in exh_res["hits"] if h not in astar_res["hits"]]
    spurious_hits = [h for h in astar_res["hits"] if h not in exh_res["hits"]]
    pruning_ratio = astar_res["pruned_nodes"] / total_space if total_space > 0 else 0

    print(f"Result Parity: {hits_match} (False Prunes: {len(false_prunes)}, Spurious: {len(spurious_hits)})")
    print(f"Pruning Ratio: {pruning_ratio:.2%} ({astar_res['pruned_nodes']}/{total_space})")
    print(f"Pruning Reasons: {astar_res['prune_reasons']}")

    gate_parity = hits_match
    gate_zero_false_prunes = (len(false_prunes) == 0 and len(spurious_hits) == 0)
    gate_positive_prune = (astar_res["pruned_nodes"] > 0)
    gate_sound_reasons = (len(astar_res["prune_reasons"]) > 0)

    verdict = "DEMONSTRATED" if (gate_parity and gate_zero_false_prunes and gate_positive_prune and gate_sound_reasons) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "01 — Compose — Abstract-Interpretation A-star Search (2026-10-02)",
            "compose_sha256": "6e79e1c0565d0785d1a85ebf2e56f5f73872f5a19c7c15b5dd0e3a10a88dc22d",
            "source_ref": "Mell/Zdancewic/Bastani, arXiv:2602.14717",
        },
        "search_config": {
            "alphabet": alphabet,
            "max_len": max_len,
            "target_byte": target,
            "space_size": total_space,
        },
        "exhaustive": exh_res,
        "abstract_astar": astar_res,
        "metrics": {
            "hits_parity": hits_match,
            "exhaustive_hits": exh_res["hit_count"],
            "astar_hits": astar_res["hit_count"],
            "false_prunes_count": len(false_prunes),
            "spurious_hits_count": len(spurious_hits),
            "pruning_ratio": pruning_ratio,
        },
        "gates": {
            "result_parity": gate_parity,
            "zero_false_prunes": gate_zero_false_prunes,
            "positive_pruning_ratio": gate_positive_prune,
            "sound_reasons_present": gate_sound_reasons,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
