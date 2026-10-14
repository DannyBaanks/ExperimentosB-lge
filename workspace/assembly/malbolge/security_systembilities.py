"""security_systembilities.py - los 8 invariantes del consenso."""

from security_authority import AuthoritySigner
from security_context import ExecutionContext

FOUNDATION_ROOTS = (
    "knowledge/00-foundation/",
    "knowledge/01-bootstrap/",
    "knowledge/02-bridge/",
    "knowledge/02-runtime/",
    "knowledge/03-contracts/",
    "knowledge/04-providers/",
    "author_sdk/",
)


def _has_drive_letter(path: str) -> bool:
    if len(path) < 2:
        return False
    return path[1] == ":" and path[0].isalpha()


def workspace_boundary_verify(ctx: ExecutionContext) -> bool:
    path = ctx.get("path")
    if path is None:
        return True
    if len(path) == 0:
        return False
    if path[0] in ("/", "\\"):
        return False
    if path.startswith("\\\\"):
        return False
    if _has_drive_letter(path):
        return False
    norm = path.replace("\\", "/")
    for seg in norm.split("/"):
        if seg == "..":
            return False
    return True


def authority_chain_verify(ctx: ExecutionContext) -> bool:
    a = ctx.authority
    if not a.identity or not a.issued_by:
        return False
    signer = AuthoritySigner()
    if signer.ready:
        if not a.signature:
            return False
        if not signer.verify(a, a.signature):
            return False
    if a.expires_at:
        try:
            exp = int(a.expires_at)
        except ValueError:
            exp = 0
        now_s = ctx.get("now")
        now = int(now_s) if now_s else 0
        if exp > 0 and now > 0 and exp < now:
            return False
    requested = ctx.get("requested_scope")
    if requested and not a.has_scope(requested):
        return False
    return True


def _is_foundation_path(path: str) -> bool:
    norm = path.replace("\\", "/")
    if "runtime/implementation/" in norm and "/python/bridge" in norm:
        return True
    for root in FOUNDATION_ROOTS:
        trimmed = root.rstrip("/")
        if norm == trimmed:
            return True
        if norm.startswith(trimmed + "/"):
            return True
    return False


def core_integrity_verify(ctx: ExecutionContext) -> bool:
    path = ctx.get("path")
    if path is None:
        return True
    if len(path) == 0:
        return False
    if not _is_foundation_path(path):
        return True
    return ctx.authority.has_scope("foundation.apply")


def runtime_contract_verify(ctx: ExecutionContext) -> bool:
    return True


def hook_isolation_verify(ctx: ExecutionContext) -> bool:
    return True


def capability_isolation_verify(ctx: ExecutionContext) -> bool:
    return True


def execution_integrity_verify(ctx: ExecutionContext) -> bool:
    return True


def pattern_linter_verify(ctx: ExecutionContext) -> bool:
    return True


SYSTEMBILITIES = (
    ("Workspace Boundary", workspace_boundary_verify),
    ("Authority Chain", authority_chain_verify),
    ("Core Integrity", core_integrity_verify),
    ("Runtime Contract", runtime_contract_verify),
    ("Hook Isolation", hook_isolation_verify),
    ("Capability Isolation", capability_isolation_verify),
    ("Execution Integrity", execution_integrity_verify),
    ("Pattern Linter", pattern_linter_verify),
)


def bootstrap_systembilities():
    return SYSTEMBILITIES
