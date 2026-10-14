"""
test_solver_ablation.py — Unit tests for Solver Optimizer Controlled Ablation.
"""

from solver_ablation import (
    get_legal_chars_for_pos,
    evaluate_candidate,
    run_controlled_ablation,
)


def test_position_legal_characters():
    pos0_chars = get_legal_chars_for_pos(0)
    assert len(pos0_chars) > 0
    # Every char must map to a legal opcode in XLAT1
    from solver_ablation import XLAT1, LEGAL_OPS
    for ch in pos0_chars:
        assert XLAT1[(ord(ch) - 33) % 94] in LEGAL_OPS


def test_evaluator_validates_hello_world():
    # Hello world source prints "Hello, world."
    with open("/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge") as f:
        src = f.read()
    hit, out, steps = evaluate_candidate(src, target="Hello")
    assert hit is True
    assert steps > 0


def test_controlled_ablation_demonstrates_h11(tmp_path):
    res = run_controlled_ablation(n_trials=5, budget_per_trial=100, out_dir=str(tmp_path), base_seed=42)
    assert res["verdict"] == "DEMONSTRATED"
    assert res["h11_demonstrated"] is True
