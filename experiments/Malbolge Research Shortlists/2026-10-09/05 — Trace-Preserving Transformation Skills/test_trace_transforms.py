import pytest
from pathlib import Path
from trace_transforms import (
    MalbolgeVM,
    PassInertCellCanonicalization,
    PassConstantCrazyFolding,
    PassSelfModifyingPrecomputation,
    PassUnsoundControl,
    verify_transformation_soundness,
    crazy_op,
)

BASE_DIR = Path(__file__).resolve().parent
HELLO_FILE = Path("workspace/assembly/malbolge/hello_world.malbolge").resolve()

def test_baseline_execution():
    code = HELLO_FILE.read_bytes()
    vm = MalbolgeVM(code)
    res = vm.run(max_steps=100)
    assert res["halted"] is True
    assert res["steps"] == 48
    assert res["output"][:5] == [ord('H'), ord('e'), ord('l'), ord('l'), ord('o')]

def test_pass1_inert_cell_canonicalization_soundness():
    code = HELLO_FILE.read_bytes()
    vm = MalbolgeVM(code)
    base_res = vm.run(max_steps=100)
    p1_vm = PassInertCellCanonicalization.apply(vm, base_res["visited_cells"])
    p1_res = p1_vm.run(max_steps=100)
    assert verify_transformation_soundness(base_res, p1_res) is True
    assert base_res["output"] == p1_res["output"]

def test_pass2_constant_crazy_folding_reduction():
    ops = ['p', 'p', '*', 'j']
    orig, opt = PassConstantCrazyFolding.simplify_constraints(ops)
    assert opt < orig
    assert orig == 50 + 50 + 5 + 5
    assert opt == 1 + 1 + 5 + 5

def test_pass3_self_modifying_precomputation_reduction():
    orig, opt = PassSelfModifyingPrecomputation.fold_encryptions(48)
    assert opt < orig
    assert opt == 48
    assert orig == 144

def test_falsification_unsound_control_rejection():
    code = HELLO_FILE.read_bytes()
    vm = MalbolgeVM(code)
    base_res = vm.run(max_steps=100)
    invalid_vm = PassUnsoundControl.apply(vm)
    invalid_res = invalid_vm.run(max_steps=100)
    # Must fail soundness verification!
    assert verify_transformation_soundness(base_res, invalid_res) is False
