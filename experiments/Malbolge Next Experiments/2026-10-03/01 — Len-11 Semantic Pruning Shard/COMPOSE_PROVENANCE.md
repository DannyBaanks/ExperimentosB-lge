# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-10-03/01 — Compose — Len-11 Semantic Pruning Shard.docx`
- **File SHA-256:** `d01340d854bb530909481fe059384e5eddd2c09917d8a391b4e5926e10616d12`
- **Category:** Malbolge Next Experiments (2026-10-03)
- **Title:** Len-11 Semantic Pruning Shard

## Core Objective & Specifications
Test whether semantic/prefix-state equivalence can prune a deterministic len-11 HI/no-input shard without losing any candidate accepted by the frozen baseline:
1. **Preserved Evidence Floor:**
   - Len-10 exhaustive search: 1,073,741,824 programs, ~2.85h, 0 hits (`DEMONSTRATED`).
   - Prior parity evidence: 417 randomized + 299,593 catalog cases, 0 mismatches (`DEMONSTRATED`).
   - Exhaustive len-11 coverage: `NOT_DEMONSTRATED`.
2. **Deterministic Shard Definition:** Seed 1103, shard size 300, targeting prefix ASCII byte 72 (`H`).
3. **Soundness Verification:** Zero false negatives (`baseline_hits == pruned_hits`).
4. **Step Savings:** Demonstrates positive VM step reduction (11.20% reduction, 1,089 steps saved).
