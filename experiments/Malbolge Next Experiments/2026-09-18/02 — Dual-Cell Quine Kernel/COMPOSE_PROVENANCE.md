# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-18/02 — Compose — Dual-Cell Quine Kernel.docx`
- **File SHA-256:** `09836e52b022cdf2d8ca146090d1b025653d0faf5c6d43c45788e9eb69c2b4e3`
- **Category:** Malbolge Next Experiments (2026-09-18)
- **Title:** Dual-Cell Quine Kernel

## Core Objective & Specifications
Test whether the tracer-observed dual-cell output mechanism can support a bounded self-reproducing kernel without falsely claiming a true quine <= 512 bytes:
1. **Preserved Evidence Floor:**
   - Lutter baseline: 59,852 original chars = 59,032 code + 820 newlines (`DEMONSTRATED`).
   - Halt steps: 69,547,437 steps (`DEMONSTRATED`).
   - Structural factorization: Two byte-identical regions of 29,516 bytes; A-only and B-only each halt after 4,354 steps with 0 output (`DEMONSTRATED`).
   - Tracer locations: Cell 29454 (59,032 output events), Cell 29282 (820 newline events).
   - True quine <= 512 bytes: strictly `NOT_DEMONSTRATED`.
2. **Bounded Search Scope:** Explores 32, 64, and 128 bytes with exact byte equality check.
3. **Sound Scientific Reporting:** Reports `NOT_DEMONSTRATED` when no candidate <= 512 bytes satisfies byte-exact quine definition.
