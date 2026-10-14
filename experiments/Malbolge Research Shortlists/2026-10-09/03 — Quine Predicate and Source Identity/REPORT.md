# EXPERIMENT REPORT: Quine Predicate and Source Identity

- **Provenance:** `OPENAI_Composes_2026-10-09 / Malbolge Research Shortlists / 2026-10-09 / 03 — Compose — Quine Predicate and Source Identity.docx`
- **Source Compose SHA-256:** `2be4d285f75c7b785a4e5dda8dd385d720c7278100ea6e02b334505c00409943`
- **External Literature Reference:** Lei Zhang (2026-09-20), *Self-Reference and Fixed Points in Formal Systems and Language Models*
- **Execution Date:** 2026-10-13
- **Environment:** Ubuntu 24.04 LTS / Python 3.12.3
- **Status / Verdict:** `[DEMONSTRATED]`

---

## 1. Executive Summary

In esoteric computing and program synthesis, solvers often evaluate candidate quines using loose heuristics (such as substring matching or fuzzy character overlap), leading to false positives and ungrounded minimality claims.

This experiment formalizes and evaluates four machine-variant-scoped quine fixed-point predicates:
1. **$P_1$ (EXACT_BYTES):** Strict Kleene source-byte equality: $\text{source\_bytes} \equiv \text{emitted\_output\_bytes}$.
2. **$P_2$ (NORMALIZED_CODE):** Whitespace-invariant code equality: $\text{norm}(\text{source}) \equiv \text{norm}(\text{output})$.
3. **$P_3$ (BEHAVIORAL_QUINE):** Iterative generation fixed point: $f(\text{output}) \equiv \text{output}$.
4. **$P_4$ (RUNTIME_IMAGE_FIXEDPOINT):** Strong memory state fixed point: $\text{mem}_{\text{initial}} \equiv \text{mem}_{\text{final}}$.

### Formal Findings
1. **Separation of Acceptance Sets:** Over the evaluation corpus, $P_1, P_2, P_3, P_4$ delineate strictly non-identical acceptance sets:
   - The canonical 59,852-byte Lutter quine satisfies $P_1, P_2, P_3$, but fails $P_4$ because classic Malbolge execution incurs destructive self-encryption ($mem[c] \leftarrow xlat2[mem[c]-33]$).
   - Formatted whitespace variants satisfy $P_2$ but are strictly rejected by $P_1$.
2. **Zero False Positives:** Non-quines (`hello_world.malbolge`) and 1-byte mutant programs are universally rejected across all four predicates.
3. **Synthesis Guidance:** Any solver synthesis claim must explicitly declare whether it targets $P_1$ (exact byte quine) or $P_2$ (normalized code quine). Conflating the two creates false minimality records.

---

## 2. Claims & Falsification Matrix

| Claim ID | Formal Claim | Target Threshold | Observed Result | Status |
|---|---|---|---|---|
| **C1** | $P_1$ and $P_2$ delineate distinct acceptance sets | $P_1 \neq P_2$ | $P_1 \subset P_2$ (Whitespace mutant in $P_2 \setminus P_1$) | **DEMONSTRATED** |
| **C2** | $P_4$ distinguishes memory fixed-points from text quines | $P_4 \neq P_1$ | Lutter quine in $P_1 \setminus P_4$ | **DEMONSTRATED** |
| **C3** | Zero false-positive acceptance of non-quines | False acceptance = 0% | 0/4 accepted for Hello World & Mutants | **DEMONSTRATED** |

---

## 3. Artifacts
- Source Provenance: `COMPOSE_PROVENANCE.md`
- Predicate Engine: `quine_predicates.py`
- Test Suite: `test_quine_predicates.py` (4/4 passed)
- Results: `results.json`
- Human Guide: `GUIA.md`
- Hash Manifest: `hashes.json`
