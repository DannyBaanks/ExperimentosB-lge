# REPORT — 04: Optimistic Cyclic Analysis (2026-10-02)

## Executive Summary
This experiment investigates the soundness of cyclic abstract interpretation over self-referential Malbolge IR graphs, reproducing the theoretical insights of Arbore, Cheung & Willsey (PLDI 2026, DOI 10.1145/3808302). Naive optimistic analyses in e-graph / cyclic IR settings often make optimistic assumptions on back-edges, falsely concluding that program variables remain invariant across cycles.

We constructed a minimal cyclic Malbolge kernel (`ROT_D` -> `CRZ` -> `JMP`) and evaluated the loop invariant property $P(A) \equiv (A = 0)$. The naive optimistic analysis asserted that the invariant held. Concrete step-by-step execution demonstrated that the crazy operation mutates $A \to 29524$ on cycle 1, producing an incontrovertible unsoundness counterexample. A least fixed-point sound cyclic abstract interpretation reached convergence in 3 iterations, computing the true reachable set $\{0, 29524\}$ and achieving $100\%$ parity with the concrete oracle.

## Quantitative Comparison

| Analysis Strategy | Claimed Invariant ($A=0$) | Concrete Oracle Truth | Verdict |
|---|---|---|---|
| **Naive Optimistic Analysis** | **True** (Asserts Invariant) | **False** ($A$ mutates to $29524$) | **UNSOUND (Counterexample Exposed)** |
| **Sound Fixed-Point Analysis** | **False** (Reachable set $\{0, 29524\}$) | **False** (Agrees with concrete oracle) | **SOUND (100% Parity)** |

### Unsoundness Counterexample Witness
- **Property Claimed:** $A = 0$ is a loop invariant across cyclic transitions.
- **Naive Optimistic Analysis:** Optimistically assumes back-edge preservation $\implies$ asserts `True`.
- **Concrete Execution Witness:**
  - Step 0 (Cycle 0, Entry): $A = 0$
  - Step 2 (Cycle 1, Post-CRZ): $A = 29524 \ne 0$
  - Step 3 (Cycle 1, Back-edge): $A = 29524 \ne 0$
- **Discrepancy:** The optimistic analysis falsely classified an actively mutating cycle as stationary.

## Verification Gates & Verdict

| Gate | Criterion | Measured Value | Status |
|---|---|---|---|
| Unsoundness Counterexample Exposed | `naive_claim == True` and `concrete_actual == False` | `True` vs `False` | **PASS** |
| Sound Analysis Parity | `sound_claim == concrete_actual` | `False` == `False` | **PASS** |
| Fixed-Point Convergence | `iterations < 20` | 3 iterations | **PASS** |

**Final Verdict:** `DEMONSTRATED`
