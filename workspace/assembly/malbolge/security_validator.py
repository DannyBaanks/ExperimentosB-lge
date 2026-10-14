"""security_validator.py - bootstrap_integrity sobre el contrato observable."""

from pathlib import Path

REQUIRED_CAPABILITY_FIELDS = ["Identity", "Version", "Status", "Layer", "Category"]


def bootstrap_integrity(contract_path: str, required: list[str]) -> str:
    p = Path(contract_path)
    if not p.is_file():
        return "ERROR"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "ERROR"
    for field in required:
        if field not in text:
            return "FAIL"
    return "PASS"


def _repo_root(root: str) -> str:
    cur = Path(root)
    for _ in range(20):
        if (cur / "bridge_core" / "capabilities").is_dir():
            return str(cur)
        if cur.parent == cur:
            break
        cur = cur.parent
    return root


def resolve_contract_path(root: str, capability: str) -> str:
    short = capability[4:] if capability.startswith("cap.") else capability
    base = _repo_root(root)
    for d in (short, capability):
        path = f"{base}/bridge_core/capabilities/{d}/{short}.iesy"
        if Path(path).is_file():
            return path
    return ""
