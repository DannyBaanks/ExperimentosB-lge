# Experiment Report: Dual-Cell Quine Kernel Synthesis (2026-09-25)

## Executive Summary
This experiment tests the dual-cell quine synthesis hypothesis across bounded search budgets (32, 64, and 128 bytes). It faithfully verifies that a true quine $\le 512$ bytes remains `NOT_DEMONSTRATED`, adhering strictly to the evidence floor and rejecting unverified claims while preserving Lutter baseline invariants.

## Search Trajectory Matrix
| Kernel Length | Grammar Strategy | Candidates Tested | Exact Quine Found | Self-Match Ratio |
|---|---|---|---|---|
| 32 Bytes | Dual-Cell Constrained | 80 | False | 0.0000 |
| 32 Bytes | Unconstrained Random | 80 | False | 0.0000 |
| 64 Bytes | Dual-Cell Constrained | 80 | False | 0.0000 |
| 64 Bytes | Unconstrained Random | 80 | False | 0.0000 |
| 128 Bytes | Dual-Cell Constrained | 80 | False | 0.0000 |
| 128 Bytes | Unconstrained Random | 80 | False | 0.0000 |

## Evidence Floor Preservation
- **Lutter Baseline:** 59,852 bytes (59,032 code + 820 newlines) at 69,547,437 steps (`DEMONSTRATED`).
- **Tracer Concentration:** Cell 29454 and Cell 29282 (`DEMONSTRATED`).
- **Quine $\le 512$ Bytes:** `NOT_DEMONSTRATED` (no spurious quines accepted).

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 5 passed in 0.34s (`test_dual_cell_quine_kernel.py`)
