#!/usr/bin/env python3
"""
Unit and integration tests for Prior-Guided Bounded Search.
"""

import os
import json
import pytest
from pathlib import Path

from prior_guided_search import (
    crazy,
    ConcreteVM,
    ProductionPriorScorer,
    run_bounded_search,
    run_experiment,
)

def test_production_prior_scorer():
    score_favored = ProductionPriorScorer.score("(=<`")
    score_unfavored = ProductionPriorScorer.score("9999")
    assert score_favored > score_unfavored

def test_search_completeness_and_space_invariance():
    candidates = ["(=<`", "9999", "(=`:", "::::"]
    res = run_bounded_search(candidates, target_byte=57)
    assert res["evaluations"] == 4
    assert "cumulative_hits" in res

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["completeness_only_ordering_changed"] is True
    assert report["gates"]["exact_solution_parity"] is True
    assert report["gates"]["faster_first_hit"] is True
    assert report["gates"]["higher_early_budget_coverage"] is True
    assert report["metrics"]["completeness_proven"] is True
    assert report["metrics"]["zero_candidates_excluded"] is True
    assert report["metrics"]["first_hit_speedup"] > 1.0
