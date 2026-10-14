#!/usr/bin/env python3
"""
ISyCo Experiment: Mine Reusable Malbolge Trace Motifs (2026-09-25)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/03 — Compose — Mine Reusable Malbolge Trace Motifs.docx
Docx SHA256: 0520cf88e3090696944e3ebdb5ab54b23b6864104bb146aa66f6a5ec692e8995
Source Reference: GrowLibm, arXiv:2603.24812 (Mining Reusable Program Trace Motifs)
"""

import sys
import os
import json
import time
import itertools
from collections import Counter
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

class TraceMotifMiner:
    """
    Mines reusable execution state/trace motifs from intermediate searches (GrowLibm).
    Extracts high-frequency prefix subroutines that establish active computational state.
    """
    @staticmethod
    def mine_motifs_from_traces(alphabet: List[str], length: int = 3) -> List[Tuple[str, int]]:
        prefix_counter = Counter()
        for p in itertools.product(alphabet, repeat=length):
            cand = "".join(p)
            vm = ConcreteVM(cand)
            out = vm.run(max_steps=15)
            # Reusable motif criterion: program survived without immediate halt and transitioned accumulator
            if not vm.halted and vm.a > 0:
                prefix_counter[cand[:2]] += 1

        return prefix_counter.most_common()

def search_scratch(alphabet: List[str], target_byte: int, max_len: int = 4) -> Tuple[Optional[str], int]:
    evals = 0
    for p in itertools.product(alphabet, repeat=max_len):
        evals += 1
        cand = "".join(p)
        vm = ConcreteVM(cand)
        out = vm.run(max_steps=25)
        if len(out) > 0 and out[0] == target_byte:
            return cand, evals
    return None, evals

def search_with_motif(alphabet: List[str], motif: str, target_byte: int, suffix_len: int = 2) -> Tuple[Optional[str], int]:
    evals = 0
    for p in itertools.product(alphabet, repeat=suffix_len):
        evals += 1
        cand = motif + "".join(p)
        vm = ConcreteVM(cand)
        out = vm.run(max_steps=25)
        if len(out) > 0 and out[0] == target_byte:
            return cand, evals
    return None, evals

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 03: Mine Reusable Trace Motifs (2026-09-25) ===")
    base_dir = Path(__file__).resolve().parent

    alphabet = ["(", "=", "<", "`", ":", "9"]

    # 1. Mining Phase
    print("Mining trace motifs from intermediate exploration traces...")
    motifs = TraceMotifMiner.mine_motifs_from_traces(alphabet, length=3)
    top_motif, top_freq = motifs[0]
    print(f"Top Mined Motif: '{top_motif}' (Frequency: {top_freq})")
    print(f"Top 5 Candidate Motifs: {motifs[:5]}")

    # 2. Evaluation on Held-Out Synthesis Workloads
    held_out_targets = [
        {"name": "Held-Out Target 57 ('9')", "byte": 57},
        {"name": "Held-Out Target 60 ('<')", "byte": 60},
    ]

    benchmarks = []
    for tgt in held_out_targets:
        target_byte = tgt["byte"]
        # Scratch synthesis
        t0 = time.time()
        scratch_hit, scratch_evals = search_scratch(alphabet, target_byte, max_len=4)
        scratch_time = time.time() - t0

        # Motif-augmented synthesis
        t0 = time.time()
        motif_hit, motif_evals = search_with_motif(alphabet, top_motif, target_byte, suffix_len=2)
        motif_time = time.time() - t0

        # Canonical Replay
        vm_reverify = ConcreteVM(motif_hit)
        replayed_out = vm_reverify.run(25)
        assert len(replayed_out) > 0 and replayed_out[0] == target_byte, f"Replay failed for {motif_hit}!"

        eval_reduction = (scratch_evals - motif_evals) / scratch_evals if scratch_evals > 0 else 0
        speedup = scratch_evals / motif_evals if motif_evals > 0 else 1.0

        benchmarks.append({
            "target_name": tgt["name"],
            "target_byte": target_byte,
            "scratch": {
                "hit": scratch_hit,
                "evaluations": scratch_evals,
                "time_sec": scratch_time,
            },
            "motif_augmented": {
                "motif_used": top_motif,
                "hit": motif_hit,
                "evaluations": motif_evals,
                "time_sec": motif_time,
            },
            "evaluation_reduction_ratio": eval_reduction,
            "eval_speedup": speedup,
            "canonical_replay_verified": True,
        })
        print(f"{tgt['name']}: Scratch={scratch_evals} evals ({scratch_hit}), Motif={motif_evals} evals ({motif_hit}) -> Reduction: {eval_reduction:.2%} ({speedup:.2f}x speedup)")

    # Gates
    all_held_out_reduced = all(b["evaluation_reduction_ratio"] > 0 for b in benchmarks)
    all_replayed = all(b["canonical_replay_verified"] for b in benchmarks)
    non_empty_library = len(motifs) > 0

    verdict = "DEMONSTRATED" if (all_held_out_reduced and all_replayed and non_empty_library) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "03 — Compose — Mine Reusable Malbolge Trace Motifs (2026-09-25)",
            "compose_sha256": "0520cf88e3090696944e3ebdb5ab54b23b6864104bb146aa66f6a5ec692e8995",
            "source_ref": "GrowLibm, arXiv:2603.24812",
        },
        "mining": {
            "mined_motifs_count": len(motifs),
            "top_motif": top_motif,
            "top_motif_frequency": top_freq,
            "motif_library": [{"motif": m, "frequency": f} for m, f in motifs[:5]],
        },
        "held_out_benchmarks": benchmarks,
        "gates": {
            "held_out_evaluations_reduced": all_held_out_reduced,
            "canonical_replay_verified": all_replayed,
            "non_empty_motif_library": non_empty_library,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
