#!/usr/bin/env python3
"""
Unit and integration tests for Symbolic Family Search.
"""

import os
import json
import pytest
from pathlib import Path

from symbolic_family_search import (
    crazy,
    ConcreteVM,
    SymbolicFamily,
    exhaustive_search,
    two_level_symbolic_family_search,
    run_experiment,
)

def test_symbolic_family_schema():
    alphabet = ["(", "=", "<"]
    fam = SymbolicFamily("(", max_len=3, alphabet=alphabet)
    assert fam.depth == 1
    assert fam.cardinality == 3 ** 2 # 9
    assert not fam.is_leaf()

    children = fam.expand()
    assert len(children) == 3
    assert children[0].prefix == "(("
    assert children[0].cardinality == 3 ** 1

def test_family_filter_soundness():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    # Prefix "=((" emits 0 != 114
    fam = SymbolicFamily("=((`", max_len=4, alphabet=alphabet)
    viable, reason = fam.evaluate_filter(114)
    assert viable is False
    assert "family_emits_wrong_byte" in reason

def test_family_search_solution_parity():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    max_len = 3
    target = 114
    exh = exhaustive_search(alphabet, max_len, target)
    fam = two_level_symbolic_family_search(alphabet, max_len, target)
    assert exh["hits"] == fam["hits"]
    assert len(set(exh["hits"]) - set(fam["hits"])) == 0

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["result_parity"] is True
    assert report["gates"]["zero_false_prunes"] is True
    assert report["gates"]["positive_eval_reduction"] is True
    assert report["gates"]["deterministic_expansion_conservation"] is True
    assert report["metrics"]["hits_parity"] is True
    assert report["metrics"]["concrete_executions_saved"] > 0
