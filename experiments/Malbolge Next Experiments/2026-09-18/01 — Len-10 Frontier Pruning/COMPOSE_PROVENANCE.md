# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-18/01 — Compose — Len-10 Frontier Pruning.docx`
- **File SHA-256:** `16739c9a6725878426e2d52e2d850103461d0dde3aac921ea188565bb41f2834`
- **Category:** Malbolge Next Experiments (2026-09-18)
- **Title:** Len-10 Frontier Pruning

## Core Objective & Specifications
Turn the completed negative HI frontier through length 10 into a controlled pruning experiment for length 11:
1. **Preserved Evidence Floor:**
   - Len 7: 2,097,152 candidates, 0 hits (`DEMONSTRATED`).
   - Len 8: 16,777,216 candidates, 0 hits (`DEMONSTRATED`).
   - Len 9: 134,217,728 candidates, 0 hits (`DEMONSTRATED`).
   - Len 10: 1,073,741,824 candidates, 0 hits, 10,252.8s (~2.85h) at 104,727 progs/s (`DEMONSTRATED`).
   - Len 11 exhaustive: strictly `NOT_DEMONSTRATED`.
2. **Safe State-Signature Pruning:** Evaluates len-11 shard preserving exact hit set (`false_negatives == 0`).
3. **Step Savings:** Demonstrates positive VM step reduction (8.42% reduction, 544 steps saved).
