# REPORT — 01: Abstract-Interpretation A* Search (2026-10-02)

## Executive Summary
This experiment implements and tests an Abstract-Interpretation guided $A^*$ search synthesizer for Malbolge program prefixes, following Mell, Zdancewic & Bastani (arXiv:2602.14717). By evaluating partial candidate prefixes strictly within their closed memory boundaries (where instruction execution and data pointers have not yet touched the uninitialized suffix), the abstract domain proves whether a branch can legally satisfy the target output byte.

The experiment was verified against an exhaustive search oracle over a search space of $1,296$ candidates. Result parity was $100\%$ ($80$ solutions found by both algorithms, $0$ false prunes, $0$ spurious hits), with a pruning ratio of $8.10\%$.

## Quantitative Results

| Metric | Exhaustive Baseline Oracle | Sound Abstract $A^*$ Search | Delta / Ratio |
|---|---|---|---|
| Search Space Size | 1,296 | 1,296 | - |
| Evaluated Terminal Nodes | 1,296 | 1,191 | -105 nodes (-8.10%) |
| Pruned Nodes | 0 | 105 | 8.10% pruned |
| Solution Hits Found | 80 | 80 | **100% exact parity** |
| False Prunes | - | 0 | **0 (Soundness preserved)** |
| Spurious Hits | - | 0 | 0 |
| Execution Time (s) | 0.059 s | 0.117 s | Overhead for priority queue & bounds |

### Pruning Reasons Breakdown
- `provably_wrong_output_byte_0_ne_114`: 100 branches pruned
- `provably_wrong_output_byte_30_ne_114`: 5 branches pruned
- Total provably invalid branches eliminated: 105

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Result Parity | `exh_hits == astar_hits` | 80 == 80 | **PASS** |
| Zero False Prunes | `false_prunes == 0` | 0 | **PASS** |
| Positive Pruning | `pruned_nodes > 0` | 105 (8.10%) | **PASS** |
| Machine-readable reasons | Every prune has formal reason | 2 distinct reasons | **PASS** |

**Final Verdict:** `DEMONSTRATED`
