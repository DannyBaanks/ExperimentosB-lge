# EXPERIMENT REPORT: Observable VM Conformance Matrix

- **Provenance:** `OPENAI_Composes_2026-10-09 / Malbolge Research Shortlists / 2026-10-09 / 07 — Compose — Observable VM Conformance Matrix.docx`
- **Source Compose SHA-256:** `1ec487eee0536a8bbf836ca184263fc53442b2d11747425bcf75b268bfde5473`
- **External Literature Reference:** Morse and Kozsik, *Emulation-Completeness of Programming Languages*, arXiv:2604.11021 (PLDI 2026)
- **Execution Date:** 2026-10-13
- **Environment:** Ubuntu 24.04 LTS / Python 3.12.3 / GCC 13.3.0
- **Status / Verdict:** `[DEMONSTRATED]`

---

## 1. Executive Summary

Testing esoteric language interpreters solely by standard stdout output (Weak Emulation) fails to detect subtle divergence in execution semantics (step scheduling, register progression, memory fill, and self-encryption).

This experiment implemented a multi-tier observable conformance matrix evaluating:
1. **Tier 1 (Weak / Output-Only):** Emitted stdout sequence equality ($O_1 \equiv O_2$).
2. **Tier 2 (Medium / Trajectory Bounds):** Step count and termination status equality ($\text{steps}_1 \equiv \text{steps}_2$ and $\text{status}_1 \equiv \text{status}_2$).
3. **Tier 3 (Strong / Full Observable Machine State):** Cycle-by-cycle register progression $(a, c, d)$ and final memory image digest equality.

### Key Findings
1. **Python vs Native C VM Parity:** The canonical Python interpreter (`workspace/assembly/malbolge/malbolge_interpreter.py`) and the native C VM (`tracer_discriminator` / Ben Olmstead reference) achieve full **Tier 3 Strong Conformance** on canonical classic workloads.
2. **Discriminative Power of Tier 3:** A subtly divergent VM emitting identical textual output passes Tier 1, but is immediately flagged and rejected by Tier 2 and Tier 3, proving that output-only smoke tests are insufficient to establish engine equivalence.

---

## 2. Claims & Falsification Matrix

| Claim ID | Formal Claim | Target Threshold | Observed Result | Status |
|---|---|---|---|---|
| **C1** | Python VM and Native C VM pass Tier 1, Tier 2, and Tier 3 | Tier 3 = True | Tier 3 = True on canonical workloads | **DEMONSTRATED** |
| **C2** | Tier 3 rejects implementations that pass Tier 1 but diverge internally | Tier 1 = True, Tier 3 = False | Divergent mock successfully flagged and rejected | **DEMONSTRATED** |

---

## 3. Artifacts
- Source Provenance: `COMPOSE_PROVENANCE.md`
- Conformance Engine: `conformance_matrix.py`
- Test Suite: `test_conformance_matrix.py` (3/3 passed)
- Results: `results.json`
- Human Guide: `GUIA.md`
- Hash Manifest: `hashes.json`
