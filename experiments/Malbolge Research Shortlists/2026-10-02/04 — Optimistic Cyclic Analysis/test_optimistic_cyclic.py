#!/usr/bin/env python3
"""
Unit and integration tests for Optimistic Cyclic Analysis.
"""

import os
import json
import pytest
from pathlib import Path

from optimistic_cyclic_analysis import (
    crazy,
    CyclicIRNode,
    CyclicIRGraph,
    ConcreteExecutionOracle,
    NaiveOptimisticAnalysis,
    SoundCyclicAbstractInterpretation,
    run_experiment,
)

def test_cyclic_graph_construction():
    nodes = [
        CyclicIRNode(node_id=0, op="ROT_D", target=1, mem_val=1),
        CyclicIRNode(node_id=1, op="CRZ", target=2, mem_val=10),
        CyclicIRNode(node_id=2, op="JMP", target=0, mem_val=0),
    ]
    graph = CyclicIRGraph("Test_Graph", nodes)
    assert len(graph.nodes) == 3
    assert graph.entry_id == 0

def test_concrete_execution_oracle():
    nodes = [
        CyclicIRNode(node_id=0, op="ROT_D", target=1, mem_val=1),
        CyclicIRNode(node_id=1, op="CRZ", target=2, mem_val=10),
        CyclicIRNode(node_id=2, op="JMP", target=0, mem_val=0),
    ]
    graph = CyclicIRGraph("Test_Graph", nodes)
    trace = ConcreteExecutionOracle.execute_trace(graph, initial_a=0, max_cycles=2)
    assert len(trace) > 0
    # Initial step has a=0, subsequent steps demonstrate mutation
    assert trace[0]["a"] == 0
    assert any(t["a"] == 29524 for t in trace)

def test_sound_fixed_point_convergence():
    nodes = [
        CyclicIRNode(node_id=0, op="ROT_D", target=1, mem_val=1),
        CyclicIRNode(node_id=1, op="CRZ", target=2, mem_val=10),
        CyclicIRNode(node_id=2, op="JMP", target=0, mem_val=0),
    ]
    graph = CyclicIRGraph("Test_Graph", nodes)
    res = SoundCyclicAbstractInterpretation.compute_fixed_point(graph, initial_a=0)
    assert res["iterations_to_convergence"] < 20
    assert 0 in res["all_reachable_a"]
    assert 29524 in res["all_reachable_a"]

def test_unsoundness_counterexample_and_parity():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["unsoundness_counterexample_exposed"] is True
    assert report["gates"]["sound_analysis_oracle_agreement"] is True
    assert report["gates"]["fixed_point_convergence"] is True
    assert report["counterexample_witness"]["naive_optimistic_claim"] is True
    assert report["counterexample_witness"]["concrete_oracle_actual"] is False
