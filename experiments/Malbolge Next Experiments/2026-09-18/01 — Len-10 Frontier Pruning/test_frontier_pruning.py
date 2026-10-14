#!/usr/bin/env python3
"""
Test Suite for Len-10 Frontier -> Safe Pruning for Len-11 (2026-09-18)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from frontier_pruning_shard import (
    EVIDENCE_FLOOR,
    FrontierVM,
    generate_shard,
    evaluate_baseline,
    evaluate_pruned,
    run_experiment,
)

def test_evidence_floor_constants():
    assert EVIDENCE_FLOOR["len_7"]["candidates"] == 2097152
    assert EVIDENCE_FLOOR["len_8"]["candidates"] == 16777216
    assert EVIDENCE_FLOOR["len_9"]["candidates"] == 134217728
    assert EVIDENCE_FLOOR["len_10"]["candidates"] == 1073741824
    assert EVIDENCE_FLOOR["len_10"]["wall_seconds"] == 10252.8
    assert EVIDENCE_FLOOR["len_11_exhaustive"] == "NOT_DEMONSTRATED"

def test_shard_reproducibility():
    s1 = generate_shard(shard_size=20, seed=123)
    s2 = generate_shard(shard_size=20, seed=123)
    assert s1 == s2
    assert len(s1) == 20

def test_pruning_soundness_zero_false_negatives():
    shard = generate_shard(shard_size=40, seed=555)
    target = [72]
    
    base = evaluate_baseline(shard, target=target, max_steps=35)
    pruned = evaluate_pruned(shard, target=target, max_steps=35)
    
    assert base["hit_codes"] == pruned["hit_codes"]
    false_negatives = [c for c in base["hit_codes"] if c not in pruned["hit_codes"]]
    assert len(false_negatives) == 0

def test_step_savings():
    shard = generate_shard(shard_size=40, seed=555)
    target = [72]
    
    base = evaluate_baseline(shard, target=target, max_steps=35)
    pruned = evaluate_pruned(shard, target=target, max_steps=35)
    
    savings = base["total_steps"] - pruned["total_steps"]
    assert savings >= 0

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["gates"]["zero_false_negatives"] is True
    assert res["gates"]["identical_hit_set"] is True
    assert res["gates"]["step_savings_positive"] is True
    assert res["gates"]["evidence_floor_preserved"] is True
