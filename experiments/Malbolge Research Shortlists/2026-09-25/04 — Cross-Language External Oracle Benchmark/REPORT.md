# REPORT — 04: Cross-Language External Oracle Benchmark (2026-09-25)

## Executive Summary
This experiment establishes a cross-language synthesis benchmark evaluated against a shared, language-agnostic external oracle, following Acher & Jézéquel (arXiv:2606.13763). The benchmark holds the required semantic I/O specification constant (emitting ASCII byte 114) while testing synthesis across three distinct representational tiers:
1. **Structured Register IR** (Direct opcode instructions)
2. **Linear Tape VM** (Turing-equivalent tape manipulations)
3. **Canonical Malbolge VM** (Crazy ternary operations, self-modifying code, instruction pointer indirection)

The experiment confirmed that all three synthesized artifacts independently execute and satisfy the exact same external oracle with zero cross-delegation. Synthesis cost (evaluations to satisfy the oracle) scaled monotonically with representational complexity: 1 evaluation for Structured IR, 4 evaluations for Linear Tape, and 16 evaluations for Malbolge (a 16x synthesis difficulty multiplier).

## Quantitative Cross-Language Results

| Representation Tier | Synthesized Program Artifact | Evaluations to Oracle Hit | Execution Time (s) | Shared Oracle Result |
|---|---|---|---|---|
| **Structured Register IR** | `[('LOAD_IMM', 114), ('EMIT', 0)]` | 1 eval | 0.0000 s | **PASS (114 emitted)** |
| **Linear Tape VM** | `++++...+` (114 increments + `.`) | 4 evals | 0.0000 s | **PASS (114 emitted)** |
| **Malbolge VM** | `((<``` (4-instruction kernel) | 16 evals | 0.0008 s | **PASS (114 emitted)** |

### Complexity Scaling & Security Audits
- **Cost Scaling:** $Evals_{\text{Structured}} (1) < Evals_{\text{Tape}} (4) \le Evals_{\text{Malbolge}} (16)$.
- **Synthesis Difficulty Multiplier:** Malbolge synthesis requires $16.0\times$ more evaluations than structured IR.
- **Delegation Audit:** All runtimes executed strictly inside their isolated interpreter memory spaces with zero external process spawning or forbidden host delegation.

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Shared Oracle Satisfied | All runtimes pass `ExternalSemanticOracle.verify` | 3/3 passed | **PASS** |
| Cost Monotonicity | Synthesis cost scales with exoticness | 1 < 4 <= 16 | **PASS** |
| Zero Forbidden Delegation | Clean isolated runtime execution | Verified | **PASS** |

**Final Verdict:** `DEMONSTRATED`
