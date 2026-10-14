# COMPOSE PROVENANCE

## Originating Compose Document
- **Source File:** `OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-09-25/02 — Compose — Dual-Cell Quine Kernel.docx`
- **File SHA-256:** `507048d511a55c14812cfeb9796268ee4339798b9ad072cf0fb72f021db4e583`
- **Category:** Malbolge Next Experiments (2026-09-25)
- **Title:** Dual-Cell Quine Kernel

## Core Objective & Specifications
Test the tracer-derived dual-cell hypothesis as a bounded synthesis framework across 32, 64, and 128 bytes without falsely claiming a true quine <= 512 bytes:
1. **Preserved Evidence Floor:**
   - Lutter baseline: 59,852 bytes = 59,032 code + 820 newlines (`DEMONSTRATED`).
   - Halt steps: 69,547,437 (`DEMONSTRATED`).
   - Tracer locations: Cell 29454 (printable code) and Cell 29282 (newlines).
   - True quine <= 512 bytes: strictly `NOT_DEMONSTRATED`.
2. **Bounded Search Scope:** Evaluates candidate kernels at 32, 64, and 128 bytes under dual-cell constrained grammar vs unconstrained random control.
3. **Byte-Exact Equality Invariant:** Output must match source byte-for-byte; zero tolerance for false positive quines.
