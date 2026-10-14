"""
test_dual_cell_discriminator.py — Substrate unit and invariant tests for Malbolge Dual-Cell Discriminator.

Part of Malbolge Next Experiments / 2026-10-09:
Compose 10 — Dual-Cell Tracer Discriminator
"""

import hashlib
from pathlib import Path
import pytest
from dual_cell_discriminator import run_single_probe, DEFAULT_QUINE_PATH

CANONICAL_QUINE_SHA256 = "dca8476f8b70c8462c32f661f63c5f8b1ad6c33946b3c7a9a35186c824117d98"
CANONICAL_RAW_BYTES = 59852
CANONICAL_CODE_BYTES = 59032
CANONICAL_NEWLINE_BYTES = 820
CANONICAL_HALT_STEPS = 69547437


def test_canonical_source_hash_integrity():
    """Verify that quine_lutter.malbolge matches the exact pinned hash and byte count."""
    quine_file = Path(DEFAULT_QUINE_PATH)
    assert quine_file.exists(), f"Quine source missing: {quine_file}"

    content = quine_file.read_bytes()
    assert len(content) == CANONICAL_RAW_BYTES, f"Expected {CANONICAL_RAW_BYTES} raw bytes, got {len(content)}"

    digest = hashlib.sha256(content).hexdigest()
    assert digest == CANONICAL_QUINE_SHA256, f"Hash mismatch: expected {CANONICAL_QUINE_SHA256}, got {digest}"


def test_baseline_execution_reproduction(tmp_path):
    """Verify baseline execution exact reproduction (69,547,437 steps, 59,852 bytes, HALT)."""
    out_json = str(tmp_path / "baseline_test.json")
    res = run_single_probe(DEFAULT_QUINE_PATH, out_json, -1, 0)

    assert res["steps"] == CANONICAL_HALT_STEPS
    assert res["halted"] is True
    assert res["total_out"] == CANONICAL_RAW_BYTES
    assert res["char_out"] == CANONICAL_CODE_BYTES
    assert res["newline_out"] == CANONICAL_NEWLINE_BYTES
    assert res["output_sha256"] == CANONICAL_QUINE_SHA256


def test_dual_cell_output_associations(tmp_path):
    """Verify that cell 29454 emits 59,032 chars and cell 29282 emits 820 newlines."""
    out_json = str(tmp_path / "associations_test.json")
    res = run_single_probe(DEFAULT_QUINE_PATH, out_json, -1, 0)

    assert res["d_29454_out_count"] == CANONICAL_CODE_BYTES, "Cell 29454 must account for all 59,032 code outputs"
    assert res["d_29282_out_count"] == CANONICAL_NEWLINE_BYTES, "Cell 29282 must account for all 820 newline outputs"


def test_target_cells_perturbation_causality(tmp_path):
    """Verify that target cells 29454 and 29282 are causally necessary and never inert."""
    # Target 29454 perturbed by +1 aborts early with 0 outputs
    out_29454 = str(tmp_path / "p_29454.json")
    res_29454 = run_single_probe(DEFAULT_QUINE_PATH, out_29454, 29454, 1)
    assert res_29454["total_out"] == 0
    assert res_29454["steps"] < 100000

    # Target 29282 perturbed by +1 aborts early with 0 outputs
    out_29282 = str(tmp_path / "p_29282.json")
    res_29282 = run_single_probe(DEFAULT_QUINE_PATH, out_29282, 29282, 1)
    assert res_29282["total_out"] == 0
    assert res_29282["steps"] < 100000


def test_inert_matched_controls_survival(tmp_path):
    """Verify that matched control cells 29455 and 29283 survive perturbation without altering output."""
    out_29455 = str(tmp_path / "p_29455.json")
    res_29455 = run_single_probe(DEFAULT_QUINE_PATH, out_29455, 29455, 1)
    assert res_29455["steps"] == CANONICAL_HALT_STEPS
    assert res_29455["output_sha256"] == CANONICAL_QUINE_SHA256

    out_29283 = str(tmp_path / "p_29283.json")
    res_29283 = run_single_probe(DEFAULT_QUINE_PATH, out_29283, 29283, 1)
    assert res_29283["steps"] == CANONICAL_HALT_STEPS
    assert res_29283["output_sha256"] == CANONICAL_QUINE_SHA256
