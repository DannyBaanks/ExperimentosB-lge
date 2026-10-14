#!/usr/bin/env python3
"""
Test Suite for Dual-Cell Quine Kernel Synthesis (2026-09-18)
"""

import sys
import json
from pathlib import Path
import pytest

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from dual_cell_kernel_synthesis import (
    LUTTER_RAW_CHARS,
    LUTTER_CODE_CHARS,
    LUTTER_NEWLINE_CHARS,
    LUTTER_HALT_STEPS,
    LUTTER_REGION_BYTES,
    A_ONLY_HALT_STEPS,
    B_ONLY_HALT_STEPS,
    CELL_PRINTABLE_D,
    CELL_NEWLINE_D,
    BoundedKernelVM,
    search_kernel,
    run_experiment,
)

def test_lutter_factorization_evidence_floor():
    assert LUTTER_RAW_CHARS == 59852
    assert LUTTER_CODE_CHARS == 59032
    assert LUTTER_NEWLINE_CHARS == 820
    assert LUTTER_HALT_STEPS == 69547437
    assert LUTTER_REGION_BYTES == 29516
    assert A_ONLY_HALT_STEPS == 4354
    assert B_ONLY_HALT_STEPS == 4354
    assert CELL_PRINTABLE_D == 29454
    assert CELL_NEWLINE_D == 29282

def test_bounded_kernel_vm_step():
    vm = BoundedKernelVM("(=<`:987654", mem_len=100)
    out = vm.run(max_steps=30)
    assert isinstance(out, list)
    assert vm.steps <= 30

def test_search_kernel_budget_compliance():
    res = search_kernel(length=32, grammar="dual_cell", budget=15, seed=12)
    assert res["candidates_tested"] == 15
    assert res["exact_quine_found"] is False

def test_end_to_end_verdict():
    res = run_experiment()
    assert res["verdict"] == "DEMONSTRATED"
    assert res["evidence_floor"]["quine_le_512_status"] == "NOT_DEMONSTRATED"
    assert res["gates"]["evidence_floor_preserved"] is True
    assert res["gates"]["zero_false_positive_quines"] is True
