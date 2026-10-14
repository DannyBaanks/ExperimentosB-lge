# COMPOSE_PROVENANCE — 02: Symbolic Family Search

- **Date:** 2026-10-02
- **Category:** Malbolge Research Shortlists
- **Title:** Symbolic Family Search
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/02 — Compose — Symbolic Family Search.docx`
- **Source SHA-256:** `beda8643978bd822d2edf6757035ebd3d2883eeacccc6421253c40a8a7db6fe8`
- **Academic Citation:** Wu et al. "Hierarchical Symbolic Families for Program Synthesis (Prism sGraph)." arXiv:2604.15272.

## Falsifiable Claim & Hypothesis
Grouping candidate Malbolge programs into hierarchical symbolic families $F = (c_0, \dots, c_{k-1}, *, \dots)$ allows batch-evaluating and pruning infeasible candidate equivalence classes at Level 1, significantly reducing concrete VM executions in Level 2 while preserving 100% solution parity compared to exhaustive enumeration.

Falsification conditions:
1. Missing any exhaustive solution or introducing spurious hits.
2. Zero reduction in concrete VM executions compared to exhaustive search.
3. Family expansion does not conserve candidate space ($|\text{surviving}| + |\text{pruned}| \ne |\Sigma|^L$).
4. Inability to generate deterministic machine-readable rejection reasons for pruned families.

## Experimental Parameters
- Alphabet $\Sigma = \{ '(', '=', '<', '`', ':', '9' \}$ ($|\Sigma| = 6$)
- Target program length: 4 (Candidate space: $6^4 = 1,296$)
- Target output byte: 114 (ASCII `'r'`)
