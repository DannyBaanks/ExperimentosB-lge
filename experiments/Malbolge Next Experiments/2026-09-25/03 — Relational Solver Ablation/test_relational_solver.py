#!/usr/bin/env python3
"""
Test Suite for Relational Solver Ablation (2026-09-25)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from relational_solver_ablation import (
    RELATIONAL_CATALOG_SIZE,
    MalbolgeVerifierVM,
    independent_verify,
    run_strategy,
    run_experiment,
)

def test_evidence_floor_constants():
    assert RELATIONAL_CATALOG_SIZE == 299593

def test_independent_verifier_validates_target():
    # True emitting code (outputs 25)
    assert independent_verify("(=<`:987654", expected_target=25) is True
    # Non emitting / wrong code
    assert independent_verify("('&<*j1VMEKL", expected_target=25) is False

def test_equal_evaluator_budgets():
    budget = 40
    r_rnd = run_strategy("random_search", target_byte=72, call_budget=budget, seed=1)
    r_sa = run_strategy("simulated_annealing", target_byte=72, call_budget=budget, seed=1)
    r_rel = run_strategy("relational_guided", target_byte=72, call_budget=budget, seed=1)

    assert r_rnd["evaluator_calls"] == budget
    assert r_sa["evaluator_calls"] == budget
    assert r_rel["evaluator_calls"] == budget

def test_relational_strategy_improves_success_rate():
    budget = 100
    r_rnd = run_strategy("random_search", target_byte=72, call_budget=budget, seed=42)
    r_rel = run_strategy("relational_guided", target_byte=72, call_budget=budget, seed=42)

    assert r_rel["success_rate"] >= r_rnd["success_rate"]
    assert r_rel["verified_hits_count"] > 0

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["gates"]["equal_budgets"] is True
    assert res["gates"]["relational_improves_success_rate"] is True
    assert res["gates"]["first_hit_observed"] is True
    assert res["gates"]["catalog_floor_preserved"] is True
