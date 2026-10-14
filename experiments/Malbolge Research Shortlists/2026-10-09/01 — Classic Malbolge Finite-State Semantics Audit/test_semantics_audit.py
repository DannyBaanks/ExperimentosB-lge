"""
test_semantics_audit.py — Unit tests for Classic Malbolge Finite-State Semantics Audit.
"""

from audit_semantics import analyze_all_trit_pairs, find_memory_tail_period, audit_cross_vm_memory_parity
import sys
sys.path.insert(0, "/home/danny/Development/ISyCo/workspace/assembly/malbolge")
import malbolge_interpreter as mi


def test_trit_pair_orbits_completeness():
    orbits = analyze_all_trit_pairs()
    assert len(orbits) == 9, "Must cover all 9 trit-pair states"
    for o in orbits:
        assert o["transient_steps"] <= 1, "Transient must be at most 1 step"
        assert o["cycle_length"] in (3, 4), f"Cycle lengths must be 3 or 4, got {o['cycle_length']}"


def test_hello_world_tail_period():
    with open("/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge") as f:
        src = f.read()
    stripped_len = len([c for c in src if not c.isspace()])
    mem = mi.load_memory(src)
    _, period = find_memory_tail_period(mem, stripped_len)
    assert period == 6, f"Expected period 6, got {period}"


def test_quine_lutter_tail_period():
    with open("/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge") as f:
        src = f.read()
    stripped_len = len([c for c in src if not c.isspace()])
    mem = mi.load_memory(src)
    _, period = find_memory_tail_period(mem, stripped_len)
    assert period in (1, 2, 3, 6), f"Period must divide 6, got {period}"


def test_vm_memory_parity():
    res = audit_cross_vm_memory_parity("/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge")
    assert res["memory_load_parity"] is True, "Python and C VM memory loading must match byte-for-byte"
