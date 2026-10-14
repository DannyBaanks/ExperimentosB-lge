import pytest
from pathlib import Path
from output_slicing import (
    InstrumentedTraceVM,
    compute_backward_slice,
    whole_trace_diff,
    sliced_equivalence_check,
    generate_candidate_corpus,
)

BASE_DIR = Path(__file__).resolve().parent
HELLO_FILE = Path("workspace/assembly/malbolge/hello_world.malbolge").resolve()

def test_trace_generation_and_slice():
    code = HELLO_FILE.read_bytes()
    vm = InstrumentedTraceVM(code)
    res = vm.run(max_steps=100)
    assert res["halted"] is True
    assert len(res["outputs"]) > 0
    assert res["outputs"][0] == ord('H')

    bslice = compute_backward_slice(res["trace"], target_output_idx=0)
    assert len(bslice) > 0
    # Backward slice must be strictly smaller than the whole trace
    assert len(bslice) < len(res["trace"])

def test_soundness_identity():
    code = HELLO_FILE.read_bytes()
    vm = InstrumentedTraceVM(code)
    res = vm.run(max_steps=100)
    bslice = compute_backward_slice(res["trace"], target_output_idx=0)

    equiv, ops, diff_step = sliced_equivalence_check(res["trace"], bslice, res["trace"], bslice, out_idx=0)
    assert equiv is True
    assert diff_step is None

def test_counterexample_recall():
    code = HELLO_FILE.read_bytes()
    corpus = generate_candidate_corpus(code)
    base_vm = InstrumentedTraceVM(code)
    base_res = base_vm.run(max_steps=100)
    base_slice = compute_backward_slice(base_res["trace"], target_output_idx=0)

    # Counterexample candidate (active_op_corrupt_entry)
    cand_bad = [c for c in corpus if c["id"] == "active_op_corrupt_entry"][0]
    bad_vm = InstrumentedTraceVM(cand_bad["code"])
    bad_res = bad_vm.run(max_steps=100)
    bad_slice = compute_backward_slice(bad_res["trace"], target_output_idx=0)

    equiv, ops, diff_step = sliced_equivalence_check(base_res["trace"], base_slice, bad_res["trace"], bad_slice, out_idx=0)
    assert equiv is False
    assert (len(bad_res["outputs"]) == 0 or bad_res["outputs"][0] != base_res["outputs"][0])

def test_inert_mutation_precision():
    code = HELLO_FILE.read_bytes()
    corpus = generate_candidate_corpus(code)
    cand_inert = [c for c in corpus if c["id"] == "inert_cell_mod"][0]

    base_vm = InstrumentedTraceVM(code)
    base_res = base_vm.run(max_steps=100)
    base_slice = compute_backward_slice(base_res["trace"], target_output_idx=0)

    inert_vm = InstrumentedTraceVM(cand_inert["code"])
    inert_res = inert_vm.run(max_steps=100)
    inert_slice = compute_backward_slice(inert_res["trace"], target_output_idx=0)

    # Sliced verification correctly recognizes output equivalence
    equiv, ops, diff = sliced_equivalence_check(base_res["trace"], base_slice, inert_res["trace"], inert_slice, out_idx=0)
    assert equiv is True
    assert inert_res["outputs"][0] == base_res["outputs"][0]
