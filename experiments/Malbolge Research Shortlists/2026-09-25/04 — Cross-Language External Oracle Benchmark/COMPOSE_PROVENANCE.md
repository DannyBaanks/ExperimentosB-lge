# COMPOSE_PROVENANCE — 04: Cross-Language External Oracle Benchmark

- **Date:** 2026-09-25
- **Category:** Malbolge Research Shortlists
- **Title:** Cross-Language External Oracle Benchmark
- **Source Document:** `OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-09-25/04 — Compose — Cross-Language External Oracle Benchmark.docx`
- **Source SHA-256:** `1a009f707c477df2d5730ac7d7fde8e4e1ab65695f72faf6fe8b23d0192e68fc`
- **Academic Citation:** Acher & Jézéquel. "Cross-Language Program Synthesis Evaluation." arXiv:2606.13763.

## Falsifiable Claim & Hypothesis
Program synthesis difficulty (evaluations required to discover a valid program) scales monotonically with the exoticness / obfuscation level of the representation (Structured Register IR < Linear Tape VM < Malbolge Cryptographic VM) when evaluated against a strictly unified, language-agnostic external semantic oracle, with zero illegal delegation or process leakage between runtimes.

Falsification conditions:
1. The external semantic oracle differs between languages or uses language-internal flags.
2. Synthesis cost does not scale with representation complexity (Malbolge requires fewer evaluations than structured IR).
3. Any runtime delegates execution to an external process or bypasses isolated evaluation.

## Experimental Parameters
- Target semantic specification: Emit character byte 114 (ASCII `'r'`) upon execution
- Shared external oracle: `ExternalSemanticOracle.verify(output_bytes)`
- Runtimes evaluated:
  - Structured Register IR (High-Level)
  - Linear Tape VM (Intermediate Esolang)
  - Canonical Malbolge VM (Exotic Cryptographic Self-Modifying)
