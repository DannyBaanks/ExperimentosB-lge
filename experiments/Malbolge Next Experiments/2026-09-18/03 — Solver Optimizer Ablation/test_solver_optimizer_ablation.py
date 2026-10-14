#!/usr/bin/env python3
"""
Test Suite for Solver / Optimizer Ablation (2026-09-18)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from solver_optimizer_ablation import (
    AutobolgeVerifier,
    WalbolgeVerifier,
    run_synthesis_ablation,
    run_experiment,
)

def test_cross_verifier_agreement():
    code = "(=<`:987654"
    vm = AutobolgeVerifier(code)
    out = vm.run(max_steps=40)
    target = out[0]
    
    # Both Autobolge and Walbolge must agree
    assert WalbolgeVerifier.cross_verify(code, target) is True
    assert WalbolgeVerifier.cross_verify(code, target + 1) is False

def test_equal_evaluator_budgets():
    budget = 50
    r_exh = run_synthesis_ablation("exhaustive_control", target_byte=25, budget=budget, seed=1)
    r_sa = run_synthesis_ablation("simulated_annealing", target_byte=25, budget=budget, seed=1)
    r_sem = run_synthesis_ablation("semantic_guided", target_byte=25, budget=budget, seed=1)

    assert r_exh["evaluator_calls"] == budget
    assert r_sa["evaluator_calls"] == budget
    assert r_sem["evaluator_calls"] == budget

def test_semantic_guidance_improvement():
    budget = 80
    r_exh = run_synthesis_ablation("exhaustive_control", target_byte=25, budget=budget, seed=99)
    r_sem = run_synthesis_ablation("semantic_guided", target_byte=25, budget=budget, seed=99)

    assert r_sem["success_rate"] > r_exh["success_rate"]
    assert r_sem["first_hit_call"] is not None
    assert r_sem["verified_hits_count"] > 0

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["gates"]["equal_budgets"] is True
    assert res["gates"]["semantic_improves_success_rate"] is True
    assert res["gates"]["first_hit_observed"] is True
    assert res["gates"]["cross_verification_enforced"] is True
