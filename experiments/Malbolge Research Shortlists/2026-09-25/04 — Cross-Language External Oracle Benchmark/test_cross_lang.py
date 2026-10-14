#!/usr/bin/env python3
"""
Unit and integration tests for Cross-Language External Oracle Benchmark.
"""

import os
import json
import pytest
from pathlib import Path

from cross_lang_oracle_benchmark import (
    crazy,
    ExternalSemanticOracle,
    StructuredRegisterVM,
    LinearTapeVM,
    MalbolgeVM,
    synthesize_structured,
    synthesize_tape,
    synthesize_malbolge,
    run_experiment,
)

def test_external_semantic_oracle():
    assert ExternalSemanticOracle.verify([114]) is True
    assert ExternalSemanticOracle.verify([114, 0, 10]) is True
    assert ExternalSemanticOracle.verify([0]) is False
    assert ExternalSemanticOracle.verify([]) is False

def test_isolated_vm_execution():
    s_prog = [("LOAD_IMM", 114), ("EMIT", 0)]
    assert ExternalSemanticOracle.verify(StructuredRegisterVM(s_prog).run()) is True

    t_prog = "+" * 114 + "."
    assert ExternalSemanticOracle.verify(LinearTapeVM(t_prog).run()) is True

    m_prog = "((<`"
    assert ExternalSemanticOracle.verify(MalbolgeVM(m_prog).run()) is True

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["shared_oracle_satisfied_by_all"] is True
    assert report["gates"]["cost_scales_with_exoticness"] is True
    assert report["gates"]["zero_forbidden_delegation"] is True
    assert len(report["representations"]) == 3
    for r in report["representations"]:
        assert r["oracle_verified"] is True
