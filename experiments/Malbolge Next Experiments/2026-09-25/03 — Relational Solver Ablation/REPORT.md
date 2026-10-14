# Experiment Report: Relational Solver Ablation (2026-09-25)

## Executive Summary
This experiment performs a controlled ablation comparing relational guidance against unconstrained random search and simulated annealing under equal evaluator-call budgets (120 calls) for target byte emission in Malbolge. Relational guidance demonstrates a verified 5.0% success rate with its first hit at call 24, whereas unconstrained random search achieves 0.0% hits.

## Synthesis Strategy Ablation Matrix
| Strategy | Evaluator Budget | Evaluator Calls Made | Verified Hits | First Hit Call | Success Rate |
|---|---|---|---|---|---|
| Random Search | 120 | 120 | 0 | None | 0.0% |
| Simulated Annealing | 120 | 120 | 0 | None | 0.0% |
| Relational Guidance | 120 | 120 | 6 | 24 | 5.0% |

## Verification Invariants
- **Evidence Floor Preserved:** Catalog size 299,593 pinned; global optimality remains `NOT_DEMONSTRATED`.
- **Equal Budgets:** Exactly 120 calls across all arms.
- **Independent Cross-Verification:** 100% of claimed hits independently verified.

## Conformance Verdict
- **Verdict:** `DEMONSTRATED`
- **Test Suite:** 5 passed in 0.34s (`test_relational_solver.py`)
