"""bootstrap_meter.py -- instrumento de medición estructural de la quine de Lutter.

Mide eventos de frontera del bootstrap [0,100] ejecutando la quine con el
mismo intérprete clásico corregido (malbolge_interpreter.py), instrumentado
vía el hook observacional on_step (no altera la semántica del runtime).

Eventos medidos:
  bootstrap_entry            : primer tick con C en [0,100]
  bootstrap_exit             : primer tick con C >= 101 (salió físicamente)
  first_continuation         : primer tick con C >= 157 (Walbolge)
  first_jump_after_bootstrap : primer JMP con C >= 101
  halt_step                  : tick del END (opcode 81)

Uso:
  python bootstrap_meter.py [archivo.malbolge]

Salidas:
  - Resumen BOOTSTRAP METER por stdout
  - bootstrap_meter_<archivo>.json con eventos + trace ±20 por frontera
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

BOOTSTRAP_END = 100
PHYSICAL_EXIT = 101
WALBOLGE_EXIT = 157
TRACE_PAD = 20
MAX_STEPS = 100_000_000

OP_NAMES = {
    4: "JMP",
    5: "OUT",
    23: "IN",
    39: "ROT",
    40: "DLOAD",
    62: "CRAZY",
    68: "NOP",
    81: "END",
}


def op_name(op: int) -> str:
    return OP_NAMES.get(op, "ILLEGAL")


class BootstrapMeter:
    """Hook observacional: registra eventos estructurales + traces ±20."""

    def __init__(self) -> None:
        self.events: dict[str, dict] = {}
        self.traces: dict[str, list[dict]] = {}
        self._ring: list[dict] = []
        self._pending: dict[str, int] = {}

    def hook(self, step: int, a: int, c: int, d: int, op: int, cell: int) -> None:
        rec = {"step": step, "a": a, "c": c, "d": d, "op": op, "op_name": op_name(op), "cell": cell}
        self._ring.append(rec)
        if len(self._ring) > TRACE_PAD + 1:
            self._ring.pop(0)

        self._detect("bootstrap_entry", step, a, c, d, op, cell)
        self._detect("bootstrap_exit", step, a, c, d, op, cell)
        self._detect("first_continuation", step, a, c, d, op, cell)
        self._detect("first_jump_after_bootstrap", step, a, c, d, op, cell)
        self._detect("halt_step", step, a, c, d, op, cell)

        for name, remaining in list(self._pending.items()):
            if rec["step"] == self.events[name]["step"]:
                continue
            self.traces[name].append(rec)
            if remaining <= 1:
                del self._pending[name]
            else:
                self._pending[name] = remaining - 1

    def _detect(self, name: str, step: int, a: int, c: int, d: int, op: int, cell: int) -> None:
        if name in self.events:
            return
        triggered = False
        if name == "bootstrap_entry":
            triggered = 0 <= c <= BOOTSTRAP_END
        elif name == "bootstrap_exit":
            triggered = c >= PHYSICAL_EXIT
        elif name == "first_continuation":
            triggered = c >= WALBOLGE_EXIT
        elif name == "first_jump_after_bootstrap":
            triggered = op == 4 and c >= PHYSICAL_EXIT
        elif name == "halt_step":
            triggered = op == 81
        if not triggered:
            return
        rec = {"step": step, "a": a, "c": c, "d": d, "op": op, "op_name": op_name(op), "cell": cell}
        self.events[name] = rec
        self.traces[name] = list(self._ring)
        self._pending[name] = TRACE_PAD


def format_event(ev: dict) -> str:
    return (
        f"step={ev['step']} c={ev['c']} d={ev['d']} a={ev['a']} "
        f"op={ev['op']}({ev['op_name']})"
    )


def main() -> int:
    src_name = sys.argv[1] if len(sys.argv) > 1 else "quine_lutter.malbolge"
    src_path = Path(__file__).parent / src_name
    if not src_path.exists():
        src_path = Path(src_name)
    if not src_path.exists():
        print(f"no se encontró el archivo: {src_name}", file=sys.stderr)
        return 2

    source = src_path.read_text(encoding="utf-8")
    meter = BootstrapMeter()

    text, steps, status = mi.run(
        source, max_steps=MAX_STEPS, stdin_data="", on_step=meter.hook
    )

    ev = meter.events
    print("BOOTSTRAP METER")
    print(f"source: {src_path.name}")
    print(f"bootstrap: [0,{BOOTSTRAP_END}]")
    print(f"bootstrap_entry: {format_event(ev['bootstrap_entry'])}")
    print(f"bootstrap_exit: {format_event(ev['bootstrap_exit'])}")
    print(f"first_continuation (c>=157): {format_event(ev['first_continuation'])}")
    print(f"first_jump_after_bootstrap: {format_event(ev['first_jump_after_bootstrap'])}")
    print(f"halt: {ev['halt_step']['step']:,}")

    out_json = src_path.with_name(f"bootstrap_meter_{src_path.stem}.json")
    payload = {
        "version": "1",
        "source": src_path.name,
        "interpreter": "malbolge_interpreter.py (clasico corregido, on_step hook)",
        "bootstrap": [0, BOOTSTRAP_END],
        "thresholds": {
            "physical_exit_c": PHYSICAL_EXIT,
            "walbolge_exit_c": WALBOLGE_EXIT,
        },
        "run": {
            "status": status,
            "steps": steps,
            "output_len": len(text),
            "max_steps": MAX_STEPS,
        },
        "events": ev,
        "traces": meter.traces,
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"json: {out_json.name} ({out_json.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())