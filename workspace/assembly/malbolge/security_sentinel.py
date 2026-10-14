"""security_sentinel.py - Guardian de invariantes (consenso).
Conjunto vacio NUNCA es ALLOW."""

from security_context import ExecutionContext
from security_systembilities import bootstrap_systembilities


class VerificationResult:
    def __init__(self, invariant: str, result: str) -> None:
        self.invariant = invariant
        self.result = result


class SentinelResponse:
    def __init__(self) -> None:
        self.verdict = "DENY"
        self.verification_results: list[VerificationResult] = []


class Sentinel:
    def __init__(self, systembilities) -> None:
        self.systembilities = systembilities

    def decide(self, ctx: ExecutionContext) -> SentinelResponse:
        resp = SentinelResponse()
        if not self.systembilities:
            return resp
        any_fail = False
        for invariant, verify in self.systembilities:
            ok = bool(verify(ctx))
            resp.verification_results.append(VerificationResult(invariant, "PASS" if ok else "FAIL"))
            if not ok:
                any_fail = True
        resp.verdict = "DENY" if any_fail else "ALLOW"
        return resp
