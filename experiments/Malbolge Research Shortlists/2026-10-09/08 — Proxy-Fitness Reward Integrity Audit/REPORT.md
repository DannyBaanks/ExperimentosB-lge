# EXPERIMENT REPORT: Proxy-Fitness Reward Integrity Audit

- **Provenance:** `OPENAI_Composes_2026-10-09 / Malbolge Research Shortlists / 2026-10-09 / 08 — Compose — Proxy-Fitness Reward Integrity Audit.docx`
- **Source Compose SHA-256:** `7859f226c19990144366794e8754f981d237afe5b82f7045311efad9ab986436`
- **External Literature Reference:** Karwowski et al., *Likelihood hacking in probabilistic program synthesis*, UAI 2026 (Aug 17–21), PMLR 337
- **Execution Date:** 2026-10-13
- **Environment:** Ubuntu 24.04 LTS / Python 3.12.3
- **Status / Verdict:** `[DEMONSTRATED]`

---

## 1. Executive Summary

In automated program synthesis and evolutionary search for esoteric languages, candidate generators frequently rely on heuristic proxy rewards (such as output prefix match, ASCII edit distance, and fuel/step consumption) to guide exploration.

This experiment audited the integrity of proxy rewards against strict ground-truth VM gates, demonstrating the phenomenon of **likelihood/reward hacking**:
- A non-terminating candidate (`C2_NON_TERMINATING_HACKER`) that emits target bytes but spins into an infinite loop scores **1.0000 fitness**, outranking the genuine 28-step terminating hit (`C1_GENUINE_HIT`, score **0.8011**).
- When guided solely by proxy metrics, synthesizers will favor non-terminating or approximate mutants over real programs.
- The strict ground-truth gate (`strict_vm_gate`) achieves a **0.0% false acceptance rate**, soundly rejecting all hacked candidates while accepting only verified terminating programs.

---

## 2. Claims & Falsification Matrix

| Claim ID | Formal Claim | Target Threshold | Observed Result | Status |
|---|---|---|---|---|
| **C1** | Ranking inversion via reward hacking occurs under standard proxy heuristics | Inversions $\ge 1$ | 1 inversion (`C2` scored 1.0 vs `C1` 0.8011) | **DEMONSTRATED** |
| **C2** | Strict classic VM gate prevents false positive acceptance | False Accept Rate $= 0.0\%$ | 0.0% false accepts (0/4 invalid accepted) | **DEMONSTRATED** |
| **C3** | Genuine hits pass strict verification | Genuine Hit Pass $= 100\%$ | `C1` passed | **DEMONSTRATED** |

---

## 3. Artifacts
- Source Provenance: `COMPOSE_PROVENANCE.md`
- Audit Script: `proxy_fitness_audit.py`
- Test Suite: `test_proxy_fitness_audit.py` (3/3 passed)
- Results: `results.json`
- Human Guide: `GUIA.md`
- Hash Manifest: `hashes.json`
