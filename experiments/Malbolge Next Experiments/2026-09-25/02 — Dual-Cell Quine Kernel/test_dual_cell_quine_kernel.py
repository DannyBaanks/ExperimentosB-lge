#!/usr/bin/env python3
"""
Test Suite for Dual-Cell Quine Kernel Synthesis (2026-09-25)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from dual_cell_quine_kernel import (
    LUTTER_RAW_BYTES,
    LUTTER_CODE_BYTES,
    LUTTER_NEWLINE_BYTES,
    LUTTER_HALT_STEPS,
    CELL_PRINTABLE_D,
    CELL_NEWLINE_D,
    BoundedQuineVM,
    search_bounded_kernel,
    run_experiment,
)

def test_lutter_canonical_evidence_floor():
    assert LUTTER_RAW_BYTES == 59852
    assert LUTTER_CODE_BYTES == 59032
    assert LUTTER_NEWLINE_BYTES == 820
    assert LUTTER_RAW_BYTES == LUTTER_CODE_BYTES + LUTTER_NEWLINE_BYTES
    assert LUTTER_HALT_STEPS == 69547437
    assert CELL_PRINTABLE_D == 29454
    assert CELL_NEWLINE_D == 29282

def test_bounded_vm_execution():
    vm = BoundedQuineVM("(=<`:987654", mem_size=200)
    out = vm.run(max_steps=50)
    assert isinstance(out, list)
    assert vm.steps <= 50

def test_quine_exact_byte_verification():
    # If output does not exactly match source bytes, it is not a quine
    vm = BoundedQuineVM("non_quine_code", mem_size=200)
    out = vm.run(max_steps=50)
    assert out != vm.code_bytes

def test_search_bounded_kernel_budget_compliance():
    res = search_bounded_kernel(length=32, grammar_type="dual_cell_constrained", candidate_budget=10, seed=1)
    assert res["candidates_tested"] == 10
    assert res["length_bytes"] == 32
    assert res["exact_quine_found"] is False

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["evidence_floor"]["quine_le_512_status"] == "NOT_DEMONSTRATED"
    assert res["gates"]["zero_false_positive_quines"] is True
    assert res["gates"]["evidence_floor_preserved"] is True
