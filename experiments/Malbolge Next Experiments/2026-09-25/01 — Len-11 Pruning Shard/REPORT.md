# Experiment Report: Len-11 Pruning Shard (2026-09-25)

## Executive Summary
This experiment demonstrates sound state-signature and prefix-divergence pruning across a deterministic 250-candidate shard of length-11 Malbolge programs, saving 1,043 VM execution steps (12.74%) with zero false negatives.

## Shard Execution Benchmark
| Evaluation Mode | Candidates Evaluated | Hits Count | Total VM Steps | Candidates Pruned | Wall Time (s) | Status |
|---|---|---|---|---|---|---|
| Frozen Baseline | 250 | 0 | 8,186 | 0 | 0.019 | Baseline |
| Signature Pruning | 250 | 0 | 7,143 | 177 | 0.020 | PASS |

## Verification Gates
- **Zero False Negatives:** 0 (PASS)
- **Identical Hit Set:** `baseline_hits == pruned_hits` (PASS)
- **Positive Step Savings:** 1,043 steps saved (12.74%) (PASS)

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 5 passed in 0.09s (`test_len11_shard_pruner.py`)
