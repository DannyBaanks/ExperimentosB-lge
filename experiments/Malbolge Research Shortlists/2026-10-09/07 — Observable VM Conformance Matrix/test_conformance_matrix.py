"""
test_conformance_matrix.py — Unit tests for Observable VM Conformance Matrix.
"""

from conformance_matrix import (
    run_python_vm,
    run_divergent_mock_vm,
    evaluate_conformance_tiers,
    run_conformance_matrix,
)
from pathlib import Path


def test_python_vm_hello_world_execution():
    hello_src = Path("/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge").read_text()
    res = run_python_vm(hello_src)
    assert res["output"] == "Hello, world."
    assert res["status"] == "HALTED"
    assert res["steps"] == 48


def test_tier_discrimination_catches_divergence():
    hello_src = Path("/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge").read_text()
    py_res = run_python_vm(hello_src)
    div_res = run_divergent_mock_vm(hello_src)
    eval_res = evaluate_conformance_tiers(py_res, div_res)

    assert eval_res["tier1_weak_output"] is True, "Mock VM passes weak output check"
    assert eval_res["tier2_medium_trajectory"] is False, "Tier 2 must catch step divergence"
    assert eval_res["tier3_strong_machine_state"] is False, "Tier 3 must reject altered machine state"


def test_conformance_matrix_runner(tmp_path):
    res = run_conformance_matrix(str(tmp_path))
    assert res["verdict"] == "DEMONSTRATED"
    assert res["tier_discrimination_demonstrated"] is True
