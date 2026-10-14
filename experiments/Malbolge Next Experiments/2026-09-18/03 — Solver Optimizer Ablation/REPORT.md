# Experiment Report: Solver / Optimizer Ablation (2026-09-18)

## Executive Summary
This experiment performs a controlled ablation comparing exhaustive search, simulated annealing, and semantic guidance under equal evaluator budgets (100 calls) for target byte emission in Malbolge. Candidates are verified against both Autobolge and Walbolge engines. Semantic guidance demonstrates a 16.0% success rate with its first hit at call 5, whereas exhaustive search and simulated annealing achieve 0.0% hits.

## Solver Strategy Ablation Matrix
| Strategy | Evaluator Budget | Evaluator Calls Made | Verified Hits | First Hit Call | Success Rate |
|---|---|---|---|---|---|
| Exhaustive Control | 100 | 100 | 0 | None | 0.0% |
| Simulated Annealing | 100 | 100 | 0 | None | 0.0% |
| Semantic Guidance | 100 | 100 | 16 | 5 | 16.0% |

## Verification Invariants
- **Evidence Floor Preserved:** Lou Scheffer constraint integration remains `NOT_DEMONSTRATED`.
- **Equal Budgets:** Exactly 100 calls across all strategies.
- **Cross-Verification Enforced:** 100% of claimed hits independently verified.

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 4 passed in 0.31s (`test_solver_optimizer_ablation.py`)
