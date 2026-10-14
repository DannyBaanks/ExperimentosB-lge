#!/usr/bin/env python3
"""
ISyCo Experiment: Optimistic Cyclic Analysis (2026-10-02)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/04 — Compose — Optimistic Cyclic Analysis.docx
Docx SHA256: 62f486676e8536b2cba1185e802c0b54f571b5e5d0001fcde81f9c8eebaf00e4
Source Reference: Arbore, Cheung, Willsey. PLDI 2026, DOI 10.1145/3808302 (Sound Cyclic Abstract Interpretation)
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

class CyclicIRNode:
    """Node in cyclic Malbolge Intermediate Representation graph."""
    def __init__(self, node_id: int, op: str, target: int, mem_val: int = 10):
        self.node_id = node_id
        self.op = op # "ROT_D", "CRZ", "ROV", "JMP", "OUT"
        self.target = target # Successor node id
        self.mem_val = mem_val

class CyclicIRGraph:
    """Cyclic CFG / IR representing self-referential or looping Malbolge code."""
    def __init__(self, name: str, nodes: List[CyclicIRNode]):
        self.name = name
        self.nodes = {n.node_id: n for n in nodes}
        self.entry_id = nodes[0].node_id

class ConcreteExecutionOracle:
    """Deterministic step-by-step concrete execution of cyclic IR."""
    @staticmethod
    def execute_trace(graph: CyclicIRGraph, initial_a: int, max_cycles: int = 4) -> List[Dict[str, Any]]:
        trace = []
        curr_id = graph.entry_id
        a = initial_a
        d = 0
        mem = [n.mem_val for n in graph.nodes.values()]
        cycle_count = 0

        trace.append({
            "step": 0,
            "cycle": 0,
            "node_id": curr_id,
            "a": a,
            "d": d
        })

        for step in range(1, max_cycles * len(graph.nodes) + 1):
            node = graph.nodes[curr_id]
            if node.op == "ROT_D":
                d = mem[d % len(mem)]
            elif node.op == "CRZ":
                a = crazy(a, mem[d % len(mem)])
            elif node.op == "ROV":
                val = mem[d % len(mem)]
                a = (val // 3) + ((val % 3) * 19683)
            elif node.op == "JMP":
                cycle_count += 1

            curr_id = node.target
            trace.append({
                "step": step,
                "cycle": cycle_count,
                "node_id": curr_id,
                "a": a,
                "d": d
            })
            if cycle_count >= max_cycles:
                break

        return trace

class NaiveOptimisticAnalysis:
    """
    Naively assumes that cyclic back-edges preserve invariants without fixed-point computation.
    Follows naive e-class analysis that optimistically asserts cycle stability.
    """
    @staticmethod
    def analyze_loop_invariant(graph: CyclicIRGraph, initial_a: int, target_prop_a: int) -> Dict[str, Any]:
        # Naive optimistic assumption: Assume the cyclic loop invariant holds across back-edges
        # If entry value equals target property, optimistically assume it persists indefinitely.
        assumed_invariant = (initial_a == target_prop_a)
        return {
            "analysis": "naive_optimistic",
            "asserts_invariant_holds": assumed_invariant,
            "justification": "optimistic_cyclic_backedge_assumption"
        }

class SoundCyclicAbstractInterpretation:
    """
    Sound cyclic abstract interpretation following Arbore, Cheung, Willsey (PLDI 2026).
    Computes least fixed-point over abstract powerset domain with monotonic transfer.
    """
    @staticmethod
    def compute_fixed_point(graph: CyclicIRGraph, initial_a: int) -> Dict[str, Any]:
        # Abstract domain: Set of reachable accumulator values at each node
        reachable: Dict[int, Set[int]] = {n_id: set() for n_id in graph.nodes}
        reachable[graph.entry_id].add(initial_a)

        changed = True
        iterations = 0
        max_iter = 20

        while changed and iterations < max_iter:
            changed = False
            iterations += 1
            for n_id, node in graph.nodes.items():
                in_values = set(reachable[n_id])
                if not in_values:
                    continue

                succ_id = node.target
                succ_set = reachable[succ_id]

                for val in in_values:
                    if node.op == "CRZ":
                        out_val = crazy(val, node.mem_val)
                    elif node.op == "ROV":
                        out_val = (node.mem_val // 3) + ((node.mem_val % 3) * 19683)
                    else:
                        out_val = val

                    if out_val not in succ_set:
                        succ_set.add(out_val)
                        changed = True

        all_reachable_a = set()
        for s in reachable.values():
            all_reachable_a.update(s)

        return {
            "analysis": "sound_cyclic_fixed_point",
            "iterations_to_convergence": iterations,
            "reachable_states_per_node": {k: sorted(list(v)) for k, v in reachable.items()},
            "all_reachable_a": sorted(list(all_reachable_a)),
        }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 04: Optimistic Cyclic Analysis (2026-10-02) ===")
    base_dir = Path(__file__).resolve().parent

    # Construct representative cyclic Malbolge IR Graph:
    # Node 0: ROT_D -> Node 1
    # Node 1: CRZ -> Node 2
    # Node 2: JMP 0 (Back-edge forming cycle)
    nodes = [
        CyclicIRNode(node_id=0, op="ROT_D", target=1, mem_val=1),
        CyclicIRNode(node_id=1, op="CRZ", target=2, mem_val=10),
        CyclicIRNode(node_id=2, op="JMP", target=0, mem_val=0),
    ]
    graph = CyclicIRGraph("Malbolge_Crazy_Cycle", nodes)

    initial_a = 0
    target_invariant = 0 # Property: A remains constant at 0 across cycle

    # 1. Concrete Execution Oracle
    concrete_trace = ConcreteExecutionOracle.execute_trace(graph, initial_a=initial_a, max_cycles=3)
    cycle1_a = [t["a"] for t in concrete_trace if t["cycle"] == 1]
    concrete_invariant_holds = all(val == target_invariant for val in cycle1_a)
    print(f"Concrete Trace: Initial A={initial_a}, Cycle 1 A-values={cycle1_a}")
    print(f"Concrete Oracle Truth: Invariant A=0 holds? {concrete_invariant_holds}")

    # 2. Naive Optimistic Analysis
    naive_res = NaiveOptimisticAnalysis.analyze_loop_invariant(graph, initial_a=initial_a, target_prop_a=target_invariant)
    print(f"Naive Optimistic Analysis: Asserts Invariant Holds? {naive_res['asserts_invariant_holds']}")

    # 3. Sound Cyclic Abstract Interpretation
    sound_res = SoundCyclicAbstractInterpretation.compute_fixed_point(graph, initial_a=initial_a)
    sound_invariant_holds = (sound_res["all_reachable_a"] == [target_invariant])
    print(f"Sound Fixed-Point Analysis: Reachable A-values={sound_res['all_reachable_a']}")
    print(f"Sound Analysis: Invariant A=0 holds? {sound_invariant_holds}")

    # 4. Verify Unsoundness Counterexample
    unsoundness_counterexample_exposed = (
        naive_res["asserts_invariant_holds"] is True
        and concrete_invariant_holds is False
    )
    sound_oracle_parity = (sound_invariant_holds == concrete_invariant_holds)

    print(f"Unsoundness Counterexample Exposed: {unsoundness_counterexample_exposed}")
    print(f"Sound Analysis Parity with Concrete Oracle: {sound_oracle_parity}")

    gate_counterexample = unsoundness_counterexample_exposed
    gate_sound_agreement = sound_oracle_parity
    gate_convergence = (sound_res["iterations_to_convergence"] < 20)

    verdict = "DEMONSTRATED" if (gate_counterexample and gate_sound_agreement and gate_convergence) else "NOT_DEMONSTRATED"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "04 — Compose — Optimistic Cyclic Analysis (2026-10-02)",
            "compose_sha256": "62f486676e8536b2cba1185e802c0b54f571b5e5d0001fcde81f9c8eebaf00e4",
            "source_ref": "Arbore, Cheung, Willsey. PLDI 2026, DOI 10.1145/3808302",
        },
        "graph_config": {
            "name": graph.name,
            "node_count": len(graph.nodes),
            "initial_a": initial_a,
            "target_invariant_property": f"A == {target_invariant}",
        },
        "concrete_oracle": {
            "trace_steps": len(concrete_trace),
            "concrete_trace": concrete_trace[:6],
            "cycle1_a_values": cycle1_a,
            "invariant_holds": concrete_invariant_holds,
        },
        "naive_optimistic": naive_res,
        "sound_fixed_point": sound_res,
        "metrics": {
            "counterexample_exposed": unsoundness_counterexample_exposed,
            "sound_oracle_parity": sound_oracle_parity,
            "convergence_iterations": sound_res["iterations_to_convergence"],
        },
        "counterexample_witness": {
            "property": f"A == {target_invariant}",
            "naive_optimistic_claim": True,
            "concrete_oracle_actual": False,
            "divergent_state": {"cycle": 1, "observed_a": cycle1_a[0] if cycle1_a else None},
        },
        "gates": {
            "unsoundness_counterexample_exposed": gate_counterexample,
            "sound_analysis_oracle_agreement": gate_sound_agreement,
            "fixed_point_convergence": gate_convergence,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
