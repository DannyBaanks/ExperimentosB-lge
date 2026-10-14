# COMPOSE_PROVENANCE — 01: Abstract-Interpretation A* Search

- **Date:** 2026-10-02
- **Category:** Malbolge Research Shortlists
- **Title:** Abstract-Interpretation A* Search
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/01 — Compose — Abstract-Interpretation A-star Search.docx`
- **Source SHA-256:** `6e79e1c0565d0785d1a85ebf2e56f5f73872f5a19c7c15b5dd0e3a10a88dc22d`
- **Academic Citation:** Mell, Zdancewic, Bastani. "A* Search over Sets of Programs with Abstract Upper Bounds and Provable Pruning." arXiv:2602.14717.

## Falsifiable Claim & Hypothesis
A sound abstract domain evaluated strictly over bounded prefix execution (where program counters $C$ and pointer $D$ do not escape the fixed prefix) can safely prune a non-trivial fraction ($>0\%$) of partial Malbolge search branches while returning 100% identical solution hits compared to exhaustive enumeration.

Falsification conditions:
1. Any false prune (an exhaustive hit pruned by the abstract domain).
2. Any missed exhaustive solution or spurious solution.
3. Zero pruning ratio (0% branches pruned).
4. Pruning decisions without deterministic machine-readable justification.

## Experimental Parameters
- Alphabet $\Sigma = \{ '(', '=', '<', '`', ':', '9' \}$ ($|\Sigma| = 6$)
- Target program length: 4 (Search space: $6^4 = 1,296$ candidates)
- Target output byte: 114 (ASCII `'r'`)
