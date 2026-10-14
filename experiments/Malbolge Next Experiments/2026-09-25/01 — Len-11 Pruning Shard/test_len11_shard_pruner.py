#!/usr/bin/env python3
"""
Test Suite for Len-11 Pruning Shard (2026-09-25)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from len11_shard_pruner import (
    FastMalbolgeVM,
    crazy,
    generate_shard,
    evaluate_shard_baseline,
    evaluate_shard_with_signature_pruner,
    run_experiment,
)

def test_fast_vm_initialization_and_bounds():
    vm = FastMalbolgeVM("(=<`:987654", init_len=200)
    assert vm.mem_len == 200
    assert vm.code_len == 11
    assert vm.a == 0 and vm.c == 0 and vm.d == 0

def test_shard_reproducibility():
    s1 = generate_shard(shard_size=25, seed=42)
    s2 = generate_shard(shard_size=25, seed=42)
    assert s1 == s2
    assert len(s1) == 25
    for c in s1:
        assert len(c) == 11

def test_pruning_soundness_no_false_negatives():
    shard = generate_shard(shard_size=50, seed=100)
    target = [72]
    
    base = evaluate_shard_baseline(shard, target=target, max_steps=40)
    pruned = evaluate_shard_with_signature_pruner(shard, target=target, max_steps=40)
    
    assert base["hit_codes"] == pruned["hit_codes"]
    false_negatives = [c for c in base["hit_codes"] if c not in pruned["hit_codes"]]
    assert len(false_negatives) == 0

def test_step_savings():
    shard = generate_shard(shard_size=50, seed=100)
    target = [72]
    
    base = evaluate_shard_baseline(shard, target=target, max_steps=40)
    pruned = evaluate_shard_with_signature_pruner(shard, target=target, max_steps=40)
    
    assert pruned["total_steps"] <= base["total_steps"]
    assert pruned["pruned_count"] > 0

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["gates"]["zero_false_negatives"] is True
    assert res["gates"]["identical_hit_set"] is True
    assert res["gates"]["positive_step_savings"] is True
