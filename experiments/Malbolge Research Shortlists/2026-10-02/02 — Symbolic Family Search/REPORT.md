# REPORT — 02: Symbolic Family Search (2026-10-02)

## Executive Summary
This experiment prototypes and evaluates a two-level Symbolic Family Search synthesizer for Malbolge, inspired by Prism sGraph (Wu et al., arXiv:2604.15272). Instead of dispatching every concrete candidate program to the concrete VM, candidates are grouped into hierarchical symbolic families $F = (c_0, \dots, c_{k-1}, *, \dots)$.

In Level 1, family prefixes are evaluated abstractly. If a family provably violates target invariants (such as emitting a conflicting output byte within the concrete prefix window), the entire family of candidates is pruned in bulk. In Level 2, only surviving leaf families are evaluated by the concrete VM oracle.

The experiment verified exact solution parity ($80$ solutions found by both approaches, zero false prunes, zero spurious solutions) while reducing concrete VM evaluations by $8.10\%$ ($105$ concrete VM executions saved).

## Quantitative Results

| Metric | Exhaustive Baseline Oracle | Two-Level Symbolic Family Search | Delta / Reduction |
|---|---|---|---|
| Search Space Size | 1,296 | 1,296 | - |
| Concrete VM Evaluations | 1,296 | 1,191 | **-105 executions (-8.10%)** |
| Pruned Candidates (Bulk) | 0 | 105 | +105 pruned in Level 1 |
| Solution Hits Found | 80 | 80 | **100% exact parity** |
| False Prunes | - | 0 | **0 (Soundness preserved)** |
| Spurious Hits | - | 0 | 0 |
| Execution Time (s) | 0.059 s | 0.126 s | Family schema expansion overhead |

### Level 1 Pruned Family Reasons Breakdown
- `family_emits_wrong_byte_0_ne_114`: 100 candidates pruned in bulk
- `family_emits_wrong_byte_30_ne_114`: 5 candidates pruned in bulk
- Total candidates eliminated at Level 1: 105

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Result Parity | `exh_hits == family_hits` | 80 == 80 | **PASS** |
| Zero False Prunes | `false_prunes == 0` | 0 | **PASS** |
| Positive VM Reduction | `eval_reduction > 0` | 105 (8.10%) | **PASS** |
| Deterministic Space Conservation | `surviving + pruned == total_space` | 1191 + 105 == 1296 | **PASS** |

**Final Verdict:** `DEMONSTRATED`
