#!/usr/bin/env python3
"""
Unit and integration tests for Abstract-Interpretation A* Search.
"""

import os
import json
import pytest
from pathlib import Path

from abstract_astar_search import (
    crazy,
    ConcreteVM,
    SoundAbstractDomain,
    exhaustive_search,
    abstract_astar_search,
    run_experiment,
)

def test_crazy_table():
    # 10 trits of 1 gives 29524
    assert crazy(0, 0) == 29524
    assert crazy(29524, 29524) == 0
    assert crazy(0, 2) == 29525

def test_concrete_vm_execution():
    vm = ConcreteVM("(=<`", mem_len=50)
    out = vm.run(max_steps=20)
    assert isinstance(out, list)
    assert vm.steps > 0

def test_sound_domain_evaluation():
    ub, reason = SoundAbstractDomain.evaluate_prefix("", 114)
    assert ub == 0.5
    assert reason is None

    # Test prefix that emits byte 0 != 114 within prefix boundary
    ub_pruned, reason_pruned = SoundAbstractDomain.evaluate_prefix("=((`", 114)
    assert ub_pruned == -1.0
    assert "provably_wrong_output_byte" in reason_pruned

def test_exhaustive_oracle_consistency():
    alphabet = ["(", "=", "<"]
    res = exhaustive_search(alphabet, max_len=3, target_byte=0)
    assert res["nodes_evaluated"] == 27
    assert isinstance(res["hits"], list)

def test_abstract_astar_sound_parity():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    max_len = 3
    target = 114
    exh = exhaustive_search(alphabet, max_len, target)
    ast = abstract_astar_search(alphabet, max_len, target)
    assert exh["hits"] == ast["hits"]
    assert len(set(exh["hits"]) - set(ast["hits"])) == 0
    assert len(set(ast["hits"]) - set(exh["hits"])) == 0

def test_full_experiment_run(tmp_path):
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["result_parity"] is True
    assert report["gates"]["zero_false_prunes"] is True
    assert report["gates"]["positive_pruning_ratio"] is True
    assert report["metrics"]["false_prunes_count"] == 0
    assert report["metrics"]["hits_parity"] is True
