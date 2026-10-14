"""security_authority.py - Authority + AuthoritySigner (HMAC-SHA256, stdlib)."""

import hashlib
import hmac
import os

BOOTSTRAP_IDENTITY = "system.bootstrap"
BOOTSTRAP_ISSUER = "bootstrap"


class Authority:
    __slots__ = ("identity", "issued_by", "issued_at", "expires_at", "scopes", "signature")

    def __init__(
        self,
        identity: str = BOOTSTRAP_IDENTITY,
        issued_by: str = BOOTSTRAP_ISSUER,
        issued_at: str = "",
        expires_at: str = "",
        scopes=None,
        signature: str = "",
    ):
        self.identity = identity
        self.issued_by = issued_by
        self.issued_at = issued_at
        self.expires_at = expires_at
        # scope "*" no matchea ningun scope concreto (fail-closed, como C):
        # foundation.apply requiere autoridad firmada real.
        self.scopes = ["*"] if scopes is None else scopes
        self.signature = signature

    def has_scope(self, wanted: str) -> bool:
        if not wanted:
            return False
        return wanted in self.scopes

    def canonical_payload(self) -> str:
        return "|".join([self.identity, self.issued_by, self.issued_at, self.expires_at, ",".join(self.scopes)])


class AuthoritySigner:
    def __init__(self) -> None:
        self.secret = os.environ.get("BRIDGE_AUTHORITY_SECRET", "")
        self.ready = len(self.secret) > 0

    def sign(self, auth: Authority) -> str:
        if not self.ready:
            return ""
        return hmac.new(
            self.secret.encode("utf-8"), auth.canonical_payload().encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def verify(self, auth: Authority, signature: str) -> bool:
        if not self.ready:
            return True
        if not signature:
            return False
        expected = self.sign(auth)
        if len(expected) != len(signature):
            return False
        diff = 0
        for x, y in zip(expected, signature):
            diff |= ord(x) ^ ord(y)
        return diff == 0
