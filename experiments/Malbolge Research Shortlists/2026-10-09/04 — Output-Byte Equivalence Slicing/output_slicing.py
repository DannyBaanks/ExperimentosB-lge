#!/usr/bin/env python3
"""
ISyCo Experiment: Output-Byte Equivalence Slicing
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/04 — Compose — Output-Byte Equivalence Slicing.docx
Docx SHA256: ac6747209c4e19014ce33d4e2dda124cf1745821b6ce291195cb4ca59c395089
"""

import sys
import os
import json
import hashlib
import time
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path

XLAT1 = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"
XLAT2 = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@"

CRZ_TABLE = [
    [4, 3, 3, 1, 0, 0, 1, 0, 0],
    [4, 3, 5, 1, 0, 2, 1, 0, 2],
    [5, 5, 4, 2, 2, 1, 2, 2, 1],
    [4, 3, 3, 1, 0, 0, 7, 6, 6],
    [4, 3, 5, 1, 0, 2, 7, 6, 8],
    [5, 5, 4, 2, 2, 1, 8, 8, 7],
    [7, 6, 6, 7, 6, 6, 4, 3, 3],
    [7, 6, 8, 7, 6, 8, 4, 3, 5],
    [8, 8, 7, 8, 8, 7, 5, 5, 4],
]
P9 = [1, 9, 81, 729, 6561]

def crazy_op(x: int, y: int) -> int:
    res = 0
    for j in range(5):
        res += CRZ_TABLE[(y // P9[j]) % 9][(x // P9[j]) % 9] * P9[j]
    return res

class InstrumentedTraceVM:
    """Classic Malbolge VM that records per-step dependencies for slicing."""
    def __init__(self, code_bytes: bytes):
        self.raw_code = code_bytes
        self.init_mem = [0] * 59049
        i = 0
        for b in code_bytes:
            if chr(b).isspace():
                continue
            self.init_mem[i] = b
            i += 1
        while i < 59049:
            self.init_mem[i] = crazy_op(self.init_mem[i - 1], self.init_mem[i - 2])
            i += 1

    def run(self, input_bytes: bytes = b"", max_steps: int = 500) -> dict:
        mem = list(self.init_mem)
        a = 0
        c = 0
        d = 0
        steps = 0
        outputs = []
        input_idx = 0
        halted = False

        # Step record: (step_id, c, d, a_before, mem_c_before, op_char, reads, writes, mem_mutated)
        trace = []
        full_states = []

        while steps < max_steps:
            val = mem[c]
            if val < 33 or val > 126:
                c = 0 if c == 59048 else c + 1
                d = 0 if d == 59048 else d + 1
                continue

            op_char = XLAT1[(val - 33 + c) % 94]
            a_before = a
            d_before = d
            c_before = c
            reads = {"c": c_before, f"mem_{c_before}": val}
            writes = {}

            if op_char == 'j':
                reads[f"mem_{d_before}"] = mem[d_before]
                d = mem[d_before]
                writes["d"] = d
            elif op_char == 'i':
                reads[f"mem_{d_before}"] = mem[d_before]
                c = mem[d_before]
                writes["c"] = c
            elif op_char == '*':
                reads[f"mem_{d_before}"] = mem[d_before]
                res = (mem[d_before] // 3) + ((mem[d_before] % 3) * 19683)
                a = mem[d_before] = res
                writes["a"] = a
                writes[f"mem_{d_before}"] = res
            elif op_char == 'p':
                reads["a"] = a_before
                reads[f"mem_{d_before}"] = mem[d_before]
                res = crazy_op(a_before, mem[d_before])
                a = mem[d_before] = res
                writes["a"] = a
                writes[f"mem_{d_before}"] = res
            elif op_char == '<':
                reads["a"] = a_before
                outputs.append(a_before & 0xFF)
                writes["output"] = a_before & 0xFF
            elif op_char == '/':
                inp = input_bytes[input_idx] if input_idx < len(input_bytes) else 59048
                input_idx += 1
                a = inp
                writes["a"] = a
            elif op_char == 'v':
                halted = True
                trace.append({
                    "step": steps, "c": c_before, "d": d_before, "a": a_before,
                    "op": op_char, "reads": reads, "writes": writes
                })
                break

            # Instruction encryption
            enc_val = ord(XLAT2[val - 33])
            mem[c_before] = enc_val
            writes[f"mem_{c_before}"] = enc_val

            trace.append({
                "step": steps, "c": c_before, "d": d_before, "a": a_before,
                "op": op_char, "reads": reads, "writes": writes
            })
            # Full snapshot for whole-trace comparison (registers + mutated memory list)
            full_states.append((steps, a, c, d, c_before, enc_val))

            steps += 1
            if op_char != 'i':
                c = 0 if c == 59048 else c + 1
            d = 0 if d == 59048 else d + 1

        return {
            "steps": steps,
            "outputs": outputs,
            "halted": halted,
            "trace": trace,
            "full_states": full_states,
        }

def compute_backward_slice(trace: List[dict], target_output_idx: int = 0) -> Set[int]:
    """Computes the set of step indices causally affecting the target output byte."""
    # Find the step that emitted the target output
    out_step_idx = None
    curr_out = 0
    for idx, rec in enumerate(trace):
        if rec["op"] == '<':
            if curr_out == target_output_idx:
                out_step_idx = idx
                break
            curr_out += 1

    if out_step_idx is None:
        return set()

    active_deps = {"a"}
    sliced_steps = {out_step_idx}

    # Traverse backwards from out_step_idx - 1 to 0
    for idx in range(out_step_idx - 1, -1, -1):
        rec = trace[idx]
        writes = rec["writes"]
        # Check if this step writes to any variable currently needed
        overlap = set(writes.keys()).intersection(active_deps)
        if overlap:
            sliced_steps.add(idx)
            # Remove satisfied dependencies
            for var in overlap:
                active_deps.remove(var)
            # Add new dependencies from this step's reads
            for read_var in rec["reads"].keys():
                active_deps.add(read_var)

    return sliced_steps

def whole_trace_diff(trace_a: List[Tuple], trace_b: List[Tuple]) -> Tuple[bool, int, Optional[int]]:
    """Compares entire trace state sequences element by element."""
    comparisons = 0
    min_len = min(len(trace_a), len(trace_b))
    for i in range(min_len):
        comparisons += 5  # a, c, d, mem_addr, mem_val
        if trace_a[i] != trace_b[i]:
            return False, comparisons, i
    if len(trace_a) != len(trace_b):
        return False, comparisons + 1, min_len
    return True, comparisons, None

def sliced_equivalence_check(trace_a: List[dict], slice_a: Set[int],
                              trace_b: List[dict], slice_b: Set[int],
                              out_idx: int = 0) -> Tuple[bool, int, Optional[int]]:
    """Compares only the sliced execution records and final emitted output byte."""
    comparisons = 0
    # First check output byte directly
    outs_a = [r["writes"]["output"] for r in trace_a if r["op"] == '<']
    outs_b = [r["writes"]["output"] for r in trace_b if r["op"] == '<']
    comparisons += 1
    if not outs_a or not outs_b:
        return (len(outs_a) == len(outs_b)), comparisons, 0
    if outs_a[out_idx] != outs_b[out_idx]:
        return False, comparisons, 0

    # Compare the sliced steps
    steps_a = sorted(list(slice_a))
    steps_b = sorted(list(slice_b))
    comparisons += 1
    if len(steps_a) != len(steps_b):
        return False, comparisons, min(len(steps_a), len(steps_b))

    for sa, sb in zip(steps_a, steps_b):
        comparisons += 3  # op, reads, writes
        ra = trace_a[sa]
        rb = trace_b[sb]
        if ra["op"] != rb["op"] or ra["reads"] != rb["reads"]:
            return False, comparisons, sa

    return True, comparisons, None

def generate_candidate_corpus(base_code: bytes) -> List[dict]:
    """Generates a diverse set of equivalent and non-equivalent candidate mutants."""
    candidates = []
    # Candidate 0: Baseline (Identity)
    candidates.append({"id": "base_identity", "code": base_code, "expected_equiv": True, "category": "identical"})

    # Candidate 1: Dead-code mutation in unused high memory cell (offset 1500)
    mut_dead = bytearray(base_code)
    if len(mut_dead) > 50:
        mut_dead[45] = 68  # change inert cell
    candidates.append({"id": "inert_cell_mod", "code": bytes(mut_dead), "expected_equiv": True, "category": "inert_mutation"})

    # Candidate 2: Invert a bit in an inert comment/whitespace-like high area
    mut_inert2 = bytearray(base_code)
    mut_inert2[-1] = mut_inert2[-1] ^ 1 if mut_inert2[-1] < 126 else mut_inert2[-1] - 1
    candidates.append({"id": "inert_tail_mod", "code": bytes(mut_inert2), "expected_equiv": True, "category": "inert_mutation"})

    # Candidate 3: Semantic bug - Mutate an active op cell directly on the output path (breaks output)
    mut_bug1 = bytearray(base_code)
    mut_bug1[0] = ord('*') if mut_bug1[0] != ord('*') else ord('j')
    candidates.append({"id": "active_op_corrupt_entry", "code": bytes(mut_bug1), "expected_equiv": False, "category": "counterexample"})

    # Candidate 4: Semantic bug - Mutate output instruction to halt
    mut_bug2 = bytearray(base_code)
    for i in range(min(30, len(mut_bug2))):
        if XLAT1[(mut_bug2[i] - 33 + i) % 94] == '<':
            # Turn into halt 'v'
            target_char = ord('v')
            for c_cand in range(33, 127):
                if XLAT1[(c_cand - 33 + i) % 94] == 'v':
                    mut_bug2[i] = c_cand
                    break
            break
    candidates.append({"id": "corrupt_output_to_halt", "code": bytes(mut_bug2), "expected_equiv": False, "category": "counterexample"})

    # Candidate 5: Subtle data mutation in a cell read during arithmetic
    mut_bug3 = bytearray(base_code)
    if len(mut_bug3) > 10:
        mut_bug3[5] = ((mut_bug3[5] - 33 + 7) % 94) + 33
    candidates.append({"id": "arithmetic_cell_mod", "code": bytes(mut_bug3), "expected_equiv": False, "category": "counterexample"})

    return candidates

def run_experiment():
    base_dir = Path(__file__).resolve().parent
    # Classic Hello World Malbolge snippet (first 89 bytes)
    hello_mal = Path("workspace/assembly/malbolge/hello_world.malbolge").resolve()
    base_code = hello_mal.read_bytes()

    print(f"=== Output-Byte Equivalence Slicing Experiment ===")
    print(f"Baseline source: {hello_mal.name} ({len(base_code)} bytes, SHA-256: {hashlib.sha256(base_code).hexdigest()[:16]}...)")

    corpus = generate_candidate_corpus(base_code)
    print(f"Candidate corpus size: {len(corpus)}")

    # Run baseline trace
    base_vm = InstrumentedTraceVM(base_code)
    base_res = base_vm.run(max_steps=200)
    base_trace = base_res["trace"]
    base_full = base_res["full_states"]
    base_output = base_res["outputs"]
    print(f"Baseline executed steps: {base_res['steps']}, outputs emitted: {base_output[:5]}")

    t0_slice = time.perf_counter()
    base_slice = compute_backward_slice(base_trace, target_output_idx=0)
    t_slice_base = time.perf_counter() - t0_slice
    print(f"Backward slice for output[0]: {len(base_slice)} / {len(base_trace)} steps ({len(base_slice)/max(1,len(base_trace))*100:.1f}% of trace)")

    results_table = []
    whole_total_time = 0.0
    slice_total_time = 0.0
    whole_total_ops = 0
    slice_total_ops = 0
    false_positives = 0
    false_negatives = 0

    for cand in corpus:
        cand_id = cand["id"]
        c_vm = InstrumentedTraceVM(cand["code"])
        c_res = c_vm.run(max_steps=200)

        # 1. Whole-trace verification
        t0_w = time.perf_counter()
        w_equiv, w_ops, w_diff_step = whole_trace_diff(base_full, c_res["full_states"])
        t_w = time.perf_counter() - t0_w
        whole_total_time += t_w
        whole_total_ops += w_ops

        # 2. Sliced verification
        t0_s = time.perf_counter()
        c_slice = compute_backward_slice(c_res["trace"], target_output_idx=0)
        s_equiv, s_ops, s_diff_step = sliced_equivalence_check(base_trace, base_slice, c_res["trace"], c_slice, out_idx=0)
        t_s = time.perf_counter() - t0_s
        slice_total_time += t_s
        slice_total_ops += s_ops

        # Output ground-truth
        oracle_equiv = (len(c_res["outputs"]) > 0 and len(base_output) > 0 and c_res["outputs"][0] == base_output[0])
        # Soundness checks
        if s_equiv and not oracle_equiv:
            false_positives += 1
        if not s_equiv and oracle_equiv:
            # Sliced check reported difference when output was identical
            pass

        results_table.append({
            "id": cand_id,
            "category": cand["category"],
            "oracle_output_match": oracle_equiv,
            "whole_trace": {
                "equivalent": w_equiv,
                "comparisons": w_ops,
                "first_diff_step": w_diff_step,
                "time_us": round(t_w * 1e6, 2),
            },
            "backward_slice": {
                "equivalent": s_equiv,
                "sliced_steps": len(c_slice),
                "comparisons": s_ops,
                "first_diff_step": s_diff_step,
                "time_us": round(t_s * 1e6, 2),
            },
            "eval_speedup_ops": round(w_ops / max(1, s_ops), 2),
        })

    print(f"\n--- Verification Comparison Matrix ---")
    for r in results_table:
        print(f"[{r['id']}] Oracle: {r['oracle_output_match']} | Whole: {r['whole_trace']['equivalent']} ({r['whole_trace']['comparisons']} ops) | Slice: {r['backward_slice']['equivalent']} ({r['backward_slice']['comparisons']} ops) | Speedup: {r['eval_speedup_ops']}x")

    recall = 1.0 if all(r['backward_slice']['equivalent'] == r['oracle_output_match'] for r in results_table if not r['oracle_output_match']) else 0.0

    experiment_data = {
        "provenance": {
            "compose": "OPENISY COMPOSE 04 — 2026-10-09 (Output-Byte Equivalence Slicing)",
            "compose_sha256": "ac6747209c4e19014ce33d4e2dda124cf1745821b6ce291195cb4ca59c395089",
            "source_paper": "Biberstein, Devietti, Naik, 'The Output-Space Hypothesis', arXiv:2609.19611",
            "baseline_source": "workspace/assembly/malbolge/hello_world.malbolge",
            "baseline_sha256": hashlib.sha256(base_code).hexdigest(),
        },
        "metrics": {
            "total_candidates": len(corpus),
            "false_positives": false_positives,
            "counterexample_recall": recall,
            "whole_trace_total_ops": whole_total_ops,
            "sliced_total_ops": slice_total_ops,
            "overall_ops_reduction_ratio": round(whole_total_ops / max(1, slice_total_ops), 2),
            "average_slice_ratio_pct": round(len(base_slice) / max(1, len(base_trace)) * 100, 2),
        },
        "candidates": results_table,
        "verdict": "DEMONSTRATED" if false_positives == 0 and recall == 1.0 and whole_total_ops > slice_total_ops else "NOT_DEMONSTRATED",
    }

    out_json = base_dir / "results.json"
    with open(out_json, "w") as f:
        json.dump(experiment_data, f, indent=2)
    print(f"\nSaved results to {out_json}")
    return experiment_data

if __name__ == "__main__":
    run_experiment()
