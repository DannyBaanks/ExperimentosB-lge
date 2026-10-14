# Experiment Report: Len-10 Frontier -> Safe Pruning for Len-11 (2026-09-18)

## Executive Summary
This experiment establishes a controlled pruning evaluation for length-11 Malbolge search grounded in the preserved negative evidence floor through length 10. Across a 250-candidate shard, state-signature pruning saves 544 VM execution steps (8.42%) with zero false negatives.

## Preserved Exhaustive Search Evidence Floor (HI without input)
| Length | Total Programs Evaluated | Hits Count | Exhaustive Search Time | Rate (progs/s) | Status |
|---|---|---|---|---|---|
| Len 7 | 2,097,152 | 0 | - | - | DEMONSTRATED |
| Len 8 | 16,777,216 | 0 | - | - | DEMONSTRATED |
| Len 9 | 134,217,728 | 0 | - | - | DEMONSTRATED |
| Len 10 | 1,073,741,824 | 0 | 10,252.8 s (~2.85 h) | 104,727 | DEMONSTRATED |
| Len 11 (Full) | $3^{11} \times \dots$ | - | - | - | NOT_DEMONSTRATED |

## Shard Benchmark (Len-11, 250 Candidates)
- **Baseline VM Steps:** 6,458 steps
- **Pruned VM Steps:** 5,914 steps
- **Pruned Candidates:** 163
- **Step Savings:** 544 steps (8.42% reduction)
- **False Negatives:** 0 (PASS)

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 5 passed in 0.33s (`test_frontier_pruning.py`)
