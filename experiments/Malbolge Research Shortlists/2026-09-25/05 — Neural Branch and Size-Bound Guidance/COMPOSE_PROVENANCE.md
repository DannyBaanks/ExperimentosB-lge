# COMPOSE_PROVENANCE — 05: Neural Branch and Size-Bound Guidance

- **Date:** 2026-09-25
- **Category:** Malbolge Research Shortlists
- **Title:** Neural Branch and Size-Bound Guidance
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/05 — Compose — Neural Branch and Size-Bound Guidance.docx`
- **Source SHA-256:** `0395b91e6c6741d868ce9e8b270e0bd8f2afcb7af8d4fc54ad45cd9cae2a228a`
- **Academic Citation:** Neural-guided superoptimization in Ethereum, uniba/110288.

## Falsifiable Claim & Hypothesis
A lightweight learned advisory predictor can prioritize candidate branches and estimate optimal size bounds for Malbolge program synthesis, significantly reducing time and evaluations to the first valid solution under conservative priority mode while preserving 100% search completeness (zero solutions lost), with canonical acceptance authority strictly retained by the Malbolge VM.

Falsification conditions:
1. No speedup in time or evaluations to first valid hit.
2. Loss of valid solutions in conservative priority guidance mode.
3. Size bound estimator excludes the known optimal solution length.
4. Correctness becomes dependent on the neural predictor rather than the canonical VM oracle.

## Experimental Parameters
- Alphabet $\Sigma = \{ '(', '=', '<', '`', ':', '9' \}$ ($|\Sigma| = 6$)
- Candidate length: 4 (Total candidate space: $6^4 = 1,296$)
- Target output byte: 114 (ASCII `'r'`)
- Evaluated modes:
  - Mode A: Conservative Priority-Guided Mode (Zero pruning, reordering only)
  - Mode B: Bounded Guidance Mode (With explicit false negative accounting)
