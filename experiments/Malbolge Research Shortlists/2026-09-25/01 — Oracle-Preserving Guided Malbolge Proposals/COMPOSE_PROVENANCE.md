# COMPOSE_PROVENANCE — 01: Oracle-Preserving Guided Malbolge Proposals

- **Date:** 2026-09-25
- **Category:** Malbolge Research Shortlists
- **Title:** Oracle-Preserving Guided Malbolge Proposals
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/01 — Compose — Oracle-Preserving Guided Malbolge Proposals.docx`
- **Source SHA-256:** `3e642047a73ae603c863728da3c792579c22828dd79ab2c9966483a1f1b41e7f`
- **Academic Citation:** SuperCoder. "Learned Candidate Proposals for Synthesis." arXiv:2505.11480.

## Falsifiable Claim & Hypothesis
Under an identical concrete VM evaluation budget, learned/guided candidate proposals that bias exploration towards active instruction slots (e.g. decoded OUT operations) discover valid target solutions sooner (fewer evaluations to first hit) and with higher yield than uniform random search, while preserving 100% deterministic correctness through canonical VM re-verification.

Falsification conditions:
1. Guided proposals require more or equal evaluations to reach the first valid hit across trials.
2. Guided proposals achieve equal or lower total solution yield under matched budget.
3. Any candidate proposed as a solution fails re-verification on the canonical Malbolge VM.

## Experimental Parameters
- Alphabet $\Sigma = \{ '(', '=', '<', '`', ':', '9' \}$ ($|\Sigma| = 6$)
- Candidate length: 4
- Target output byte: 114 (ASCII `'r'`)
- Evaluation budget: 400 concrete VM evaluations per trial
- Trials: 10 independent random seeds
