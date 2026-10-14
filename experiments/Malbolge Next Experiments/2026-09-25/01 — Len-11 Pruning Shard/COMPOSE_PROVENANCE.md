# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-25/01 — Compose — Len-11 Pruning Shard.docx`
- **File SHA-256:** `668cb8ec02d792f65e351284b6ae4fd0f7355c70c32c3a3c25618f0809ff4281`
- **Category:** Malbolge Next Experiments (2026-09-25)
- **Title:** Len-11 Pruning Shard

## Core Objective & Specifications
Test whether state signature and prefix-divergence pruning can reduce evaluator VM work on a fixed len-11 shard without false negatives:
1. **Target:** Prefix ASCII 72 (`H`) without input.
2. **Deterministic Shard:** 250 candidates generated deterministically from seed 20260925.
3. **Soundness Invariant:** Exact hit-set identity (`baseline_hits == pruned_hits`), zero false negatives.
4. **Step Savings:** Achieves measurable VM step reduction (12.74% reduction, 1,043 steps saved).
