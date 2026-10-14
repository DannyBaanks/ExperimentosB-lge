# REPORT — 02: Prior-Guided Bounded Search (2026-09-25)

## Executive Summary
This experiment implements and tests Prior-Guided Bounded Search for Malbolge program synthesis, based on Brevis (arXiv:2608.02162). The core requirement is that search completeness must be mathematically preserved: only the evaluation ordering of candidates may change, with zero candidate exclusion.

We compared uniform lexicographical search against production-prior-guided search across the complete, finite space of 1,296 candidates of length 4. The prior-guided ordering reached the first valid target hit in 3 evaluations (compared to 16 evaluations for uniform search, a 5.33x speedup). Furthermore, by the 25% evaluation checkpoint (324 candidates evaluated), prior-guided search discovered 50 solutions compared to only 14 for uniform search (a 3.57x coverage increase). The candidate sets and final solution hits were 100% identical.

## Quantitative Comparison

| Metric | Uniform Lexicographical Ordering | Prior-Guided Ordering (Brevis) | Delta / Speedup |
|---|---|---|---|
| Total Space Evaluated | 1,296 candidates | 1,296 candidates | Identical space (100% completeness) |
| Evaluations to First Hit | 16 evals | 3 evals | **5.33x speedup** |
| Solutions at 10% Budget (129 evals) | 3 hits | 30 hits | **10.0x yield** |
| Solutions at 25% Budget (324 evals) | 14 hits | 50 hits | **3.57x yield** |
| Solutions at 50% Budget (648 evals) | 35 hits | 59 hits | **1.69x yield** |
| Final Total Solutions Found | 80 hits | 80 hits | **100% Exact Parity** |
| Execution Time (s) | 0.063 s | 0.065 s | Identical execution scale |

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Completeness Preserved | `candidates_uniform == candidates_prior` | 1296 == 1296 | **PASS** |
| Solution Set Parity | `hits_uniform == hits_prior` | 80 == 80 | **PASS** |
| Faster First Hit | `prior_first < uniform_first` | 3 < 16 (5.33x) | **PASS** |
| Early Budget Advantage | `hits_prior_25% > hits_uniform_25%` | 50 > 14 | **PASS** |

**Final Verdict:** `DEMONSTRATED`
