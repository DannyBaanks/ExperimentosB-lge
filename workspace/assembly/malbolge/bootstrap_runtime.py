import json
import sys
import time
from pathlib import Path

from paths import find_root
from registry import REGISTRY_JSON
from sentinel import allowed
from security_authority import Authority
from security_context import ExecutionContext
from security_sentinel import Sentinel
from security_systembilities import bootstrap_systembilities
from security_validator import REQUIRED_CAPABILITY_FIELDS, bootstrap_integrity, resolve_contract_path

try:
    from malbolge_interpreter import run as malbolge_run
except ImportError:
    malbolge_run = None

_HERE = Path(__file__).resolve().parent
MALBOLGE_CORE = (_HERE / "bootstrap.malbolge").read_text(encoding="ascii")
MALBOLGE_SIGNATURE = "Hello, world."


def malbolge_gate(input_text: str) -> dict:
    """Gate obligatorio: el core esoterico (programa malbolge real) debe
    ejecutarse en el interprete canonical y HALTAR con la firma exacta.
    Sin eso el orquestador falla cerrado: el esoterico no responde."""
    if malbolge_run is None:
        return {"ok": False, "error": "interprete malbolge ausente"}
    text, steps, status = malbolge_run(MALBOLGE_CORE, max_steps=2000000, stdin_data=input_text)
    if status != "HALTED":
        return {"ok": False, "error": "status=%s" % status}
    if text != MALBOLGE_SIGNATURE:
        return {"ok": False, "error": "firma=%r" % text[:40]}
    return {"ok": True, "steps": steps, "signature": text}


def extract_str(input_text: str, key: str) -> str:
    marker = f'"{key}"'
    i = input_text.find(marker)
    if i >= 0:
        rest = input_text[i + len(marker):]
        open_q = rest.find('"')
        if open_q >= 0:
            from_ = rest[open_q + 1:]
            close = from_.find('"')
            if close >= 0:
                return from_[:close]
    return ""


def main() -> None:
    input_text = sys.stdin.read()
    op_raw = extract_str(input_text, "operation")
    capability_raw = extract_str(input_text, "capability")
    path_raw = extract_str(input_text, "path")
    op = op_raw
    capability = capability_raw or "cap.boot_wizard"

    gate = malbolge_gate(input_text)
    if not gate["ok"]:
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "FAIL", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "FAIL", "action": op,
            "message": "Core esoterico Malbolge no responde: " + gate["error"],
            "echo": {"operation": op, "capability": capability},
        }, ensure_ascii=False))
        return

    if not allowed(op):
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "DENY", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "DENY", "action": op,
            "message": "Operacion no permitida en Bootstrapability",
            "echo": {"operation": op, "capability": capability},
        }, ensure_ascii=False))
        return

    root = find_root()
    if not root:
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "FAIL", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "FAIL", "action": op,
            "message": "No se encontro .iesyroot",
            "echo": {"operation": op},
        }, ensure_ascii=False))
        return

    ctx = ExecutionContext()
    ctx.set("now", str(int(time.time())))
    if path_raw:
        ctx.set("path", path_raw)

    sentinel = Sentinel(bootstrap_systembilities())
    resp = sentinel.decide(ctx)
    verification_results = [{"invariant": r.invariant, "result": r.result} for r in resp.verification_results]

    if resp.verdict != "ALLOW":
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "DENY", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "DENY", "action": op,
            "message": "Sentinel DENY: invariante violado",
            "verification_results": verification_results,
            "echo": {"operation": op, "capability": capability},
        }, ensure_ascii=False))
        return

    contract = resolve_contract_path(root, capability)
    if not contract:
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "FAIL", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "FAIL", "action": op,
            "message": "bootstrap_integrity ERROR",
            "echo": {"operation": op, "capability": capability},
        }, ensure_ascii=False))
        return

    integrity = bootstrap_integrity(contract, REQUIRED_CAPABILITY_FIELDS)
    if integrity != "PASS":
        print(json.dumps({
            "protocol": "bridge.protocol/1", "status": "FAIL", "runtime": "Malbolge",
            "law_result": "FAIL", "integrity_status": "FAIL", "action": op,
            "message": f"bootstrap_integrity {integrity}",
            "echo": {"operation": op, "capability": capability},
        }, ensure_ascii=False))
        return

    action = "registry" if "registry" in op else "execute"
    out = {
        "protocol": "bridge.protocol/1",
        "status": "OK",
        "runtime": "Malbolge",
        "law_result": "PASS",
        "integrity_status": "RUN",
        "action": action,
        "message": "Contrato validado por MiniSentinel + Sentinel (consenso) + bootstrap_integrity (engine Malbolge via interprete canonical)",
        "address": contract,
        "required_fields": REQUIRED_CAPABILITY_FIELDS,
        "verification_results": verification_results,
        "malbolge_core": gate,
        "echo": {"operation": op, "capability": capability, "root": root},
        "registry": json.loads(REGISTRY_JSON),
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
