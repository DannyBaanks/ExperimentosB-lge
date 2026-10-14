"""
test_quine_predicates.py — Unit tests for Quine Acceptance Predicates and Source Identity.
"""

from quine_predicates import (
    normalize_code,
    check_exact_bytes,
    check_normalized_code,
    check_runtime_image_fixedpoint,
    run_predicate_evaluation_matrix,
)


def test_normalization_strips_whitespace():
    raw = b"abc \n\t def\r\n"
    assert normalize_code(raw) == b"abcdef"


def test_exact_bytes_discriminates_whitespace():
    src1 = b"abc"
    src2 = b"abc\n"
    assert not check_exact_bytes(src1, src2)
    assert check_normalized_code(src1, src2)


def test_runtime_image_requires_unmutated_memory():
    m1 = [1, 2, 3]
    m2 = [1, 2, 3]
    m3 = [1, 2, 4]
    assert check_runtime_image_fixedpoint(m1, m2)
    assert not check_runtime_image_fixedpoint(m1, m3)


def test_full_predicate_matrix_demonstrates_separation(tmp_path):
    res = run_predicate_evaluation_matrix(out_dir=str(tmp_path))
    assert res["verdict"] == "DEMONSTRATED"
    assert res["distinct_acceptance_sets_demonstrated"] is True
    # Verify P1 is subset of P2
    p1_set = set(res["acceptance_sets"]["P1_EXACT_BYTES"])
    p2_set = set(res["acceptance_sets"]["P2_NORMALIZED_CODE"])
    assert p1_set.issubset(p2_set)
    assert len(p2_set) > len(p1_set), "P2 must strictly accept normalized variants rejected by P1"
