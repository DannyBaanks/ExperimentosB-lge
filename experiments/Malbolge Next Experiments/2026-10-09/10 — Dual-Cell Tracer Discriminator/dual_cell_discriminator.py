"""
dual_cell_discriminator.py — Orchestrator for Malbolge Dual-Cell Tracer Discrimination.

Evaluates Hypothesis H10:
Perturbing the two observed output-associated data cells (d=29454 for 59,032 chars,
d=29282 for 820 newlines) produces a distinctive, reproducible divergence against
predeclared matched controls (immediate neighbors and inert data plane cells).
"""

from __future__ import annotations
import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_QUINE_PATH = "/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge"
BINARY_PATH = str(BASE_DIR / "tracer_discriminator")


def run_single_probe(src_file: str, out_json: str, cell: int, delta: int) -> Dict[str, Any]:
    cmd = [BINARY_PATH, src_file, out_json, str(cell), str(delta)]
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    duration = time.time() - t0

    with open(out_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["execution_time_seconds"] = round(duration, 4)
    return data


def run_full_matrix(
    quine_path: str = DEFAULT_QUINE_PATH,
    out_dir: str = ".",
) -> Dict[str, Any]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Baseline Run
    baseline_json = str(out_path / "baseline.json")
    print("Executing Canonical Baseline...")
    baseline = run_single_probe(quine_path, baseline_json, -1, 0)
    baseline_hash = baseline["output_sha256"]

    # Verify Baseline Invariants
    assert baseline["steps"] == 69547437, f"Expected 69547437 steps, got {baseline['steps']}"
    assert baseline["total_out"] == 59852, f"Expected 59852 outputs, got {baseline['total_out']}"
    assert baseline["char_out"] == 59032, f"Expected 59032 chars, got {baseline['char_out']}"
    assert baseline["newline_out"] == 820, f"Expected 820 newlines, got {baseline['newline_out']}"
    assert baseline["d_29454_out_count"] == 59032, f"Expected 59032 at d=29454, got {baseline['d_29454_out_count']}"
    assert baseline["d_29282_out_count"] == 820, f"Expected 820 at d=29282, got {baseline['d_29282_out_count']}"
    print(f"  -> Baseline Verified! Total: {baseline['total_out']} outs, 69.5M steps in {baseline['execution_time_seconds']}s")

    # 2. Perturbation Matrix
    target_cells = [
        {"cell": 29454, "role": "TARGET_CHAR_STREAM", "desc": "Associated with 59,032 code outputs"},
        {"cell": 29282, "role": "TARGET_NEWLINE_STREAM", "desc": "Associated with 820 newline outputs"},
    ]

    matched_controls = [
        {"cell": 29453, "role": "CONTROL_NEIGHBOR", "desc": "Immediate predecessor of cell 29454"},
        {"cell": 29455, "role": "CONTROL_NEIGHBOR", "desc": "Immediate successor of cell 29454"},
        {"cell": 29281, "role": "CONTROL_NEIGHBOR", "desc": "Immediate predecessor of cell 29282"},
        {"cell": 29283, "role": "CONTROL_NEIGHBOR", "desc": "Immediate successor of cell 29282"},
        {"cell": 30000, "role": "CONTROL_SEGMENT", "desc": "Distant data segment cell"},
        {"cell": 35000, "role": "CONTROL_SEGMENT", "desc": "Distant data segment cell"},
        {"cell": 40000, "role": "CONTROL_SEGMENT", "desc": "Distant data segment cell"},
    ]

    all_specs = target_cells + matched_controls
    deltas = [+1, -1]
    matrix_records: List[Dict[str, Any]] = []

    print("\nExecuting Perturbation Matrix across Target and Matched Control Cells...")
    for spec in all_specs:
        cell = spec["cell"]
        role = spec["role"]
        desc = spec["desc"]

        for delta in deltas:
            tmp_json = str(out_path / f"probe_c{cell}_d{delta:+d}.json")
            data = run_single_probe(quine_path, tmp_json, cell, delta)
            Path(tmp_json).unlink(missing_ok=True)  # Clean up temp file

            # Determine outcome classification
            is_identical_quine = (data["output_sha256"] == baseline_hash and data["steps"] == baseline["steps"])
            if is_identical_quine:
                outcome_class = "INERT_SURVIVED"
            elif data["total_out"] == 0:
                outcome_class = "EARLY_ABORT_ZERO_OUTPUT"
            elif data["total_out"] < baseline["total_out"]:
                outcome_class = "PARTIAL_OUTPUT_CORRUPTED"
            else:
                outcome_class = "DIVERGENT_STREAM"

            rec = {
                "cell": cell,
                "role": role,
                "description": desc,
                "delta": delta,
                "steps": data["steps"],
                "halted": data["halted"],
                "total_out": data["total_out"],
                "char_out": data["char_out"],
                "newline_out": data["newline_out"],
                "output_sha256": data["output_sha256"],
                "identical_to_baseline": is_identical_quine,
                "outcome_class": outcome_class,
                "exec_time_seconds": data["execution_time_seconds"],
            }
            matrix_records.append(rec)
            print(f"  Cell {cell:5d} ({role:<22}) delta={delta:+2d} -> {outcome_class:<25} (Outs: {data['total_out']:5d}, Steps: {data['steps']:10d})")

    # 3. Analyze Discrimination
    # Check that both target cells produce non-inert distinct effects
    targets_results = [r for r in matrix_records if "TARGET" in r["role"]]
    controls_results = [r for r in matrix_records if "CONTROL" in r["role"]]

    target_inert_count = sum(1 for r in targets_results if r["identical_to_baseline"])
    control_inert_count = sum(1 for r in controls_results if r["identical_to_baseline"])

    # Targets are 100% causal and never inert
    targets_all_divergent = (target_inert_count == 0)
    # Inert control cells exist and survive without altering the output
    inert_controls_exist = (control_inert_count > 0)

    verdict = "DEMONSTRATED" if (targets_all_divergent and inert_controls_exist) else "NOT_DEMONSTRATED"

    summary = {
        "experiment": "Malbolge Next Experiments / 2026-10-09 / Compose 10: Dual-Cell Tracer Discriminator",
        "provenance_compose_sha256": "22e93e8e414ab55bf842fe6485b80ba5282f041c986b3427cb35b7cadcfd6af2",
        "canonical_quine_sha256": "dca8476f8b70c8462c32f661f63c5f8b1ad6c33946b3c7a9a35186c824117d98",
        "baseline": baseline,
        "verdict": verdict,
        "hypothesis_h10_demonstrated": targets_all_divergent,
        "targets_divergence_rate": 1.0 - (target_inert_count / len(targets_results)),
        "controls_inert_rate": control_inert_count / len(controls_results),
        "perturbation_matrix": matrix_records,
    }

    with open(out_path / "results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def print_summary_table(summary: Dict[str, Any]) -> None:
    print("\n" + "=" * 96)
    print(" EXPERIMENT REPORT: DUAL-CELL TRACER DISCRIMINATOR (Lutter Quine 59,852 Bytes)")
    print("=" * 96)
    print(f"Formal Verdict: [{summary['verdict']}]")
    print(f"Hypothesis H10 Demonstrated: {summary['hypothesis_h10_demonstrated']}\n")

    header = f"{'Cell':<6} | {'Role':<23} | {'Delta':<6} | {'Steps':<10} | {'Total Out':<10} | {'Outcome Class':<26}"
    print(header)
    print("-" * 96)

    for r in summary["perturbation_matrix"]:
        print(
            f"{r['cell']:<6} | {r['role']:<23} | {r['delta']:<6} | "
            f"{r['steps']:<10d} | {r['total_out']:<10d} | {r['outcome_class']:<26}"
        )
    print("=" * 96 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Dual-Cell Tracer Discriminator Experiment")
    parser.add_argument("--src", type=str, default=DEFAULT_QUINE_PATH, help="Path to quine_lutter.malbolge")
    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    summary = run_full_matrix(quine_path=args.src, out_dir=args.out)
    print_summary_table(summary)
