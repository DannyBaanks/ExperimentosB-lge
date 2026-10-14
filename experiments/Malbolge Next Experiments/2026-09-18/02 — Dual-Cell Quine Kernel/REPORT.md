# Experiment Report: Dual-Cell Quine Kernel Synthesis (2026-09-18)

## Executive Summary
This experiment tests the dual-cell quine synthesis hypothesis across bounded search budgets (32, 64, and 128 bytes). It faithfully verifies that a true quine $\le 512$ bytes remains `NOT_DEMONSTRATED`, adhering strictly to the evidence floor and rejecting unverified claims while preserving Lutter baseline invariants.

## Canonical Evidence Floor Preserved
- **Lutter Chars:** 59,852 (59,032 code + 820 newlines) at 69,547,437 steps (`DEMONSTRATED`).
- **Factorization:** Two 29,516-byte regions; isolated A and B regions halt after 4,354 steps with 0 output (`DEMONSTRATED`).
- **Tracer Concentration:** Cell 29454 (code) and Cell 29282 (newlines) (`DEMONSTRATED`).
- **Quine $\le 512$ Bytes Status:** `NOT_DEMONSTRATED` (no false positive quines accepted).

## Bounded Synthesis Search Matrix
| Kernel Length | Grammar Strategy | Candidates Tested | Exact Quine Found | Max Prefix Match |
|---|---|---|---|---|
| 32 Bytes | Dual-Cell Constrained | 60 | False | 0 |
| 32 Bytes | Random Control | 60 | False | 0 |
| 64 Bytes | Dual-Cell Constrained | 60 | False | 0 |
| 64 Bytes | Random Control | 60 | False | 0 |
| 128 Bytes | Dual-Cell Constrained | 60 | False | 0 |
| 128 Bytes | Random Control | 60 | False | 0 |

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 4 passed in 0.22s (`test_dual_cell_synthesis.py`)
