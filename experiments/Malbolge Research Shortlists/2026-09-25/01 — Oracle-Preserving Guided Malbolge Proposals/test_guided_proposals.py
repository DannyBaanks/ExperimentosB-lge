#!/usr/bin/env python3
"""
Unit and integration tests for Oracle-Preserving Guided Malbolge Proposals.
"""

import os
import json
import pytest
from pathlib import Path

from guided_proposals import (
    crazy,
    ConcreteVM,
    unguided_uniform_search,
    guided_proposal_search,
    run_experiment,
)

def test_concrete_vm_oracle_execution():
    vm = ConcreteVM("(=<`", mem_len=50)
    out = vm.run(max_steps=20)
    assert isinstance(out, list)
    assert vm.steps > 0

def test_unguided_search_budget_enforcement():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    res = unguided_uniform_search(alphabet, max_len=4, target_byte=114, budget=50, seed=123)
    assert res["evaluations"] <= 50
    assert "hits_count" in res

def test_guided_search_oracle_soundness():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    res = guided_proposal_search(alphabet, max_len=4, target_byte=114, budget=100, seed=123)
    for h in res["hits"]:
        vm = ConcreteVM(h)
        out = vm.run(25)
        assert len(out) > 0 and out[0] == 114

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["earlier_first_hit"] is True
    assert report["gates"]["higher_solution_yield"] is True
    assert report["gates"]["canonical_oracle_reverification"] is True
    assert report["aggregate_metrics"]["first_hit_speedup_ratio"] > 1.0
    assert report["aggregate_metrics"]["yield_multiplier"] > 1.0
