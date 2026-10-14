# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-18/03 — Compose — Solver Optimizer Ablation.docx`
- **File SHA-256:** `c90cc64e1198403f5dbd947a0ba9e476bcfc6e2ee41ddf8beef5376b2de48e7e`
- **Category:** Malbolge Next Experiments (2026-09-18)
- **Title:** Solver Optimizer Ablation

## Core Objective & Specifications
Compare small fixed synthesis workloads under equal evaluator budgets across exhaustive search, simulated annealing, and semantic guidance:
1. **Preserved Evidence Floor:**
   - Solver tooling includes evaluator/exhaustive paths, simulated annealing/meta-search, Autobolge and Walbolge cross-verification (`DEMONSTRATED`).
   - Lou Scheffer-style constraint integration into a complete solver: `NOT_DEMONSTRATED`.
2. **Budget Equality:** Strict enforcement of 100 evaluator calls across all three strategies.
3. **Cross-Verification Gate:** Candidates must independently pass both Autobolge and Walbolge verification.
4. **Primary Metric Performance:** Semantic guidance achieves 16.0% success rate with first hit at call 5, outperforming exhaustive search (0.0%) and simulated annealing (0.0%).
