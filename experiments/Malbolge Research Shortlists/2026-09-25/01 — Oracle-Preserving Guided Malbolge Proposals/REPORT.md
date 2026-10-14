# REPORT — 01: Oracle-Preserving Guided Malbolge Proposals (2026-09-25)

## Executive Summary
This experiment investigates whether learned / guided candidate proposals can improve synthesis efficiency in Malbolge without compromising deterministic correctness, following the SuperCoder paradigm (arXiv:2505.11480). Because Malbolge execution requires exact instruction decoding mod 94 to generate observable I/O, uniform random exploration wastes evaluations on dead non-operational combinations.

We evaluated guided proposal generation against unguided uniform random generation over 10 independent trials with a matched budget of 400 concrete VM evaluations per trial. Guided proposals reached the first valid target hit in an average of 5.5 evaluations (compared to 18.0 evaluations for unguided search, a 3.27x speedup) and produced an average of 54.8 verified solutions (compared to 25.2, a 2.17x yield improvement). Every proposed hit was strictly validated by the canonical concrete VM.

## Quantitative Results (Averaged over 10 Trials)

| Metric | Unguided Uniform Search | Guided Proposal Search | Delta / Multiplier |
|---|---|---|---|
| Matched VM Evaluation Budget | 400 | 400 | Identical Budget |
| Average Evals to First Hit | 18.0 evals | 5.5 evals | **3.27x faster time-to-first-hit** |
| Average Solutions Discovered | 25.2 hits | 54.8 hits | **2.17x higher solution yield** |
| Unique Verified Hits Pool | - | 77 unique programs | 100% verified by canonical VM |
| Oracle Bypass / Hallucinations | 0 | 0 | **0 (Full Soundness)** |

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Earlier First Hit | `avg_gd_first < avg_un_first` | 5.5 < 18.0 (3.27x) | **PASS** |
| Higher Solution Yield | `avg_gd_hits > avg_un_hits` | 54.8 > 25.2 (2.17x) | **PASS** |
| Canonical VM Re-verification | Every hit verified on ConcreteVM | 77/77 passed | **PASS** |

**Final Verdict:** `DEMONSTRATED`
