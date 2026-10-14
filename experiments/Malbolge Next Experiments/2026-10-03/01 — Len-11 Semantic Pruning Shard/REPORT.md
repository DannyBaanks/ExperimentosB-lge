# Experiment Report: Len-11 Semantic Pruning Shard

## Executive Summary
This experiment verifies semantic and prefix-state pruning on a deterministic shard of len-11 Malbolge candidate programs, achieving an 11.20% reduction in VM execution steps with strictly zero false negatives relative to the frozen baseline.

## Shard Execution Benchmark
| Evaluation Mode | Candidates Evaluated | Hits Count | Total VM Steps | Candidates Pruned | Wall Time (s) | Status |
|---|---|---|---|---|---|---|
| Frozen Baseline | 300 | 0 | 9,722 | 0 | 14.854 | Baseline |
| Semantic Pruning | 300 | 0 | 8,633 | 206 | 15.084 | PASS |

## Soundness and Verification Gates
- **Identical Hit Set:** `baseline_hits == pruned_hits` (PASS)
- **False Negatives:** Exactly 0 (PASS)
- **Step Savings:** 1,089 steps saved (11.20% reduction) (PASS)

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 5 passed in 7.21s (`test_len11_pruning.py`)
