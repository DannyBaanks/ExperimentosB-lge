# REPORT — 05: Neural Branch and Size-Bound Guidance (2026-09-25)

## Executive Summary
This experiment evaluates learned neural-style branch prioritization and size-bound estimation for Malbolge program synthesis, adapting neural superoptimization techniques (uniba/110288). The predictor extracts structural execution features (terminal output feasibility, active operation density, and length fit) to prioritize search queues without delegating correctness authority away from the canonical VM.

In **Conservative Priority Mode**, the predictor reorders the search queue while preserving 100% completeness (all 1,296 candidates evaluated, zero candidates dropped). This achieved a **5.33x speedup to the first valid hit** (eval 3 vs eval 16) with 80/80 solutions preserved. In **Bounded Guidance Mode**, pruning branches below a threshold eliminated 950 candidates (73.3% of the search space), finding 50 solutions in 0.018s while explicitly auditing 30 false negatives.

## Quantitative Results

| Metric | Baseline Unguided Search | Mode A: Conservative Priority | Mode B: Bounded Guidance |
|---|---|---|---|
| Total Candidates Evaluated | 1,296 | 1,296 | 346 (950 pruned) |
| Evaluations to First Hit | 16 evals | 3 evals | 3 evals |
| Time-to-First-Hit Speedup | 1.00x | **5.33x speedup** | **5.33x speedup** |
| Total Solutions Discovered | 80 hits | 80 hits | 50 hits |
| False Negatives (Lost Hits) | 0 | **0 (Full Completeness)** | 30 (Explicitly Tracked) |
| Total Execution Time (s) | 0.068 s | 0.070 s | **0.018 s (-73.5% time)** |

### Size-Bound Estimation Accuracy
- **Predicted Minimal Program Length:** 4
- **Actual Optimal Program Length:** 4
- **Accuracy:** 100% correct bound estimation.

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Faster First Hit | `prio_first < base_first` | 3 < 16 (5.33x) | **PASS** |
| Zero Loss in Conservative Mode | `prio_hits == base_hits` | 80 == 80 | **PASS** |
| Size Bound Prediction Verified | `predicted_bound == optimal_len` | 4 == 4 | **PASS** |
| False Negative Audit | Explicit accounting of pruned candidates | 30 tracked | **PASS** |

**Final Verdict:** `DEMONSTRATED`
