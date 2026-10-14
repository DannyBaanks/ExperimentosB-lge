"""
test_proxy_fitness_audit.py — Unit tests for Proxy-Fitness Reward Integrity Audit.
"""

from proxy_fitness_audit import (
    score_prefix_match,
    score_ascii_closeness,
    composite_proxy_fitness,
    strict_vm_gate,
    run_reward_integrity_audit,
)


def test_prefix_match_scoring():
    assert score_prefix_match("HI", "HI") == 1.0
    assert score_prefix_match("HI", "H") == 0.5
    assert score_prefix_match("HI", "NO") == 0.0


def test_strict_gate_rejects_non_halting_prefix():
    # Emits 'HI' but did not halt
    assert not strict_vm_gate("HI", "HI", "TIMEOUT")
    # Emits 'H' and halted
    assert not strict_vm_gate("HI", "H", "HALTED")
    # Emits 'HI' and halted
    assert strict_vm_gate("HI", "HI", "HALTED")


def test_reward_integrity_audit_demonstrates_exploit(tmp_path):
    res = run_reward_integrity_audit(str(tmp_path))
    assert res["verdict"] == "DEMONSTRATED"
    assert res["proxy_hacking_observed"] is True
    assert res["ranking_inversions_count"] > 0
    assert res["strict_gate_false_accept_rate"] == 0.0
