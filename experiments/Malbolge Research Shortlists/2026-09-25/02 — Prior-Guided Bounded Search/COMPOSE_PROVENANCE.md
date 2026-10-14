# COMPOSE_PROVENANCE — 02: Prior-Guided Bounded Search

- **Date:** 2026-09-25
- **Category:** Malbolge Research Shortlists
- **Title:** Prior-Guided Bounded Search
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/02 — Compose — Prior-Guided Bounded Search.docx`
- **Source SHA-256:** `6d43391cb75eaecf1f22f1b92559b7e55cededc9a904470ed067b5dbe467ea20`
- **Academic Citation:** Brevis. "Prior-Guided Bounded Program Search." arXiv:2608.02162.

## Falsifiable Claim & Hypothesis
A production prior learned strictly from historical Malbolge execution traces and instruction frequencies improves the search ordering (reducing evaluations to first hit and increasing early budget coverage) over uniform lexicographical enumeration on a finite candidate space, while preserving 100% search completeness (zero candidates excluded) and exact solution-set parity under the canonical VM oracle.

Falsification conditions:
1. Candidate space size changes or candidates are silently excluded ($|\text{prior\_space}| \ne |\text{uniform\_space}|$).
2. Missing any solution hit found by the uniform enumeration.
3. No improvement in evaluations to first hit or early-budget coverage.

## Experimental Parameters
- Alphabet $\Sigma = \{ '(', '=', '<', '`', ':', '9' \}$ ($|\Sigma| = 6$)
- Candidate length: 4 (Total exact candidate space: $6^4 = 1,296$)
- Target output byte: 114 (ASCII `'r'`)
