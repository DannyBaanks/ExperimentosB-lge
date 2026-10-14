# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-25/03 — Compose — Relational Solver Ablation.docx`
- **File SHA-256:** `9010433dbd700c1814b77d95e0ac2e18a3ac7e0730097494a21946719a45e846`
- **Category:** Malbolge Next Experiments (2026-09-25)
- **Title:** Relational Solver Ablation

## Core Objective & Specifications
Measure whether relational/semantic guidance improves small fixed Malbolge synthesis workloads versus unconstrained search under equal evaluator-call budgets:
1. **Preserved Evidence Floor:**
   - Relational catalog size: 299,593 (`DEMONSTRATED`).
   - Automatic ub and ubs synthesis exists (`DEMONSTRATED`).
   - Global optimizer optimality: `NOT_DEMONSTRATED`.
2. **Equal Budget Invariant:** Fixed budget of 120 evaluator calls across random search, simulated annealing, and relational guidance.
3. **Independent Double-Verification:** Every candidate solution must pass independent verification before counting as a hit.
4. **Primary Metric Performance:** Relational guidance achieves verified hits (5.0% success rate, first hit at call 24) compared to 0.0% for random search.
