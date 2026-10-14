# EXPERIMENT REPORT: Offline Presynthesis Oracle

- **Provenance:** `OPENAI_Composes_2026-10-09 / Malbolge Research Shortlists / 2026-10-09 / 06 — Compose — Offline Presynthesis Oracle.docx`
- **Source Compose SHA-256:** `f690a25b66252547f44d6e3e44d25531b60628611b8359b44af2428e34c86be8`
- **External Literature Reference:** Dong et al., *Presynthesis / Foresighter*, PLDI 2026 (`https://arxiv.org/abs/2604.13290` / `https://doi.org/10.1145/3808288`)
- **Execution Date:** 2026-10-13
- **Environment:** Ubuntu 24.04 LTS / Python 3.12.3
- **Status / Verdict:** `[DEMONSTRATED]`

---

## 1. Executive Summary

Exhaustive search synthesizers in Malbolge suffer from combinatorial explosion because every candidate program requires spinning up the VM and filling 59,049 memory cells with the crazy operation recurrence.

This experiment evaluated an **Offline Abstract Presynthesis Oracle** that precomputes position-dependent instruction viability tables ($L=3$) and early dead-end semantics (halting at step 1 or null-byte outputs) before VM execution:
- Over a combinatorial subspace of 216 prefix candidates, the oracle successfully **pruned 214 candidates (99.07% reduction)**.
- Full VM evaluations were reduced from **216 down to only 2**.
- **Soundness was strictly preserved:** Exactly 0 false negatives were observed (every viable candidate accepted by the exhaustive search was retained by the oracle).
- Achieved an amortized end-to-end **speedup factor of 134.61x**.

---

## 2. Claims & Falsification Matrix

| Claim ID | Formal Claim | Target Threshold | Observed Result | Status |
|---|---|---|---|---|
| **C1** | Soundness: Zero false negatives against exhaustive oracle | False Negatives $= 0$ | 0 false negatives (100% sound) | **DEMONSTRATED** |
| **C2** | Subspace pruning rate | Pruning Rate $> 50\%$ | 99.07% pruned (214/216) | **DEMONSTRATED** |
| **C3** | Search acceleration | Speedup $> 1.0\text{x}$ | **134.61x** speedup | **DEMONSTRATED** |

---

## 3. Artifacts
- Source Provenance: `COMPOSE_PROVENANCE.md`
- Oracle Engine: `presynthesis_oracle.py`
- Test Suite: `test_presynthesis_oracle.py` (3/3 passed)
- Results: `results.json`
- Human Guide: `GUIA.md`
- Hash Manifest: `hashes.json`
