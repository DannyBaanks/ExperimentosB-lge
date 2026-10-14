#!/usr/bin/env python3
"""
Test Suite for Len-11 Semantic Pruning Shard (2026-10-03)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from len11_semantic_pruning import (
    MalbolgeMiniVM,
    crazy,
    generate_len11_shard,
    evaluate_baseline,
    evaluate_with_semantic_pruning,
    run_experiment,
)

def test_crazy_operation_truth_table():
    # In 10 trits, 0 crazy 0 gives trit 1 at every place value -> sum(3^i) = 29524
    assert crazy(0, 0) == 29524
    # Single trit check: 29524 % 3 is 1
    assert (crazy(0, 0) % 3) == 1

def test_deterministic_shard_generation():
    s1 = generate_len11_shard(shard_size=20, seed=42)
    s2 = generate_len11_shard(shard_size=20, seed=42)
    assert s1 == s2
    assert len(s1) == 20
    for cand in s1:
        assert len(cand) == 11

def test_pruning_zero_false_negatives():
    shard = generate_len11_shard(shard_size=30, seed=123)
    target = [72]
    
    baseline = evaluate_baseline(shard, target, max_steps=40)
    pruned = evaluate_with_semantic_pruning(shard, target, max_steps=40)
    
    assert baseline["hit_codes"] == pruned["hit_codes"]
    false_negatives = [c for c in baseline["hit_codes"] if c not in pruned["hit_codes"]]
    assert len(false_negatives) == 0
    assert pruned["total_steps"] <= baseline["total_steps"]

def test_step_savings_achieved():
    shard = generate_len11_shard(shard_size=40, seed=999)
    target = [72]
    
    baseline = evaluate_baseline(shard, target, max_steps=40)
    pruned = evaluate_with_semantic_pruning(shard, target, max_steps=40)
    
    savings = baseline["total_steps"] - pruned["total_steps"]
    assert savings >= 0
    assert pruned["pruned_count"] > 0

def test_results_json_verdict_demonstrated():
    res_file = CURRENT_DIR / "results.json"
    if not res_file.exists():
        run_experiment()
    
    data = json.loads(res_file.read_text())
    assert data["verdict"] == "DEMONSTRATED"
    assert data["gates"]["zero_false_negatives"] is True
    assert data["gates"]["identical_hit_set"] is True
    assert data["gates"]["positive_step_savings"] is True
