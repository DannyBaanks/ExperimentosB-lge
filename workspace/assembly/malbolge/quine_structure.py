"""quine_structure.py -- anatomía estructural de la quine de Lutter.

Ejecuta la quine con el intérprete clásico corregido (mismo on_step hook
observacional, semántica intacta) y mide:

  - histograma de C (celdas ejecutadas / nunca ejecutadas)
  - opcodes por región: bootstrap [0,100], código (101..29515], datos (29516..59031], fill (59032..59048]
  - jumps (op 4) y DLOADs (op 40), saltos hacia adelante/atrás
  - OUTs: pasos, caracteres, período del loop de impresión
  - fases: init → loop → fin (primer/último OUT)
  - ruido: NOPs, ILLEGALs, PC dentro de la sección de datos

Uso:
  python quine_structure.py [archivo.malbolge]

Salidas:
  - Resumen por stdout
  - quine_structure_<archivo>.json (histogramas, sin traza completa)
"""
from __future__ import annotations

import array
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
MEM_SIZE = 3 ** 10
BOOTSTRAP_END = 100
CODE_END = 29515
DATA_START = 29516
FILL_START = 59032

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


def main() -> int:
    src_name = sys.argv[1] if len(sys.argv) > 1 else "quine_lutter.malbolge"
    src_path = Path(__file__).parent / src_name
    if not src_path.exists():
        src_path = Path(src_name)
    if not src_path.exists():
        print(f"no se encontró el archivo: {src_name}", file=sys.stderr)
        return 2

    source = src_path.read_text(encoding="utf-8")

    cs = array.array("H")
    ops = array.array("B")
    out_steps = array.array("I")
    out_a = array.array("I")
    jmp_steps = array.array("I")
    n_steps = 0

    def hook(step, a, c, d, op, cell):
        nonlocal n_steps
        cs.append(c)
        ops.append(op)
        if op == 5:
            out_steps.append(step)
            out_a.append(a)
        elif op == 4:
            jmp_steps.append(step)

    text, steps, status = mi.run(source, max_steps=MAX_STEPS, stdin_data="", on_step=hook)
    n_steps = steps

    counts = [0] * MEM_SIZE
    for c in cs:
        counts[c] += 1

    never = [c for c, n in enumerate(counts) if n == 0]
    regs = {"bootstrap": (0, 100), "code": (101, 29515), "data": (29516, 59031), "fill": (59032, 59048)}

    op_hist = {}
    reg_hist = {}
    reg_steps = {}
    for reg, (lo, hi) in regs.items():
        op_hist[reg] = {}
        reg_steps[reg] = 0
    total_hist = {}
    for op, c in zip(ops, cs):
        total_hist[op] = total_hist.get(op, 0) + 1
        for reg, (lo, hi) in regs.items():
            if lo <= c <= hi:
                reg_steps[reg] += 1
                op_hist[reg][op] = op_hist[reg].get(op, 0) + 1
                break

    valid_ops = {4, 5, 23, 39, 40, 62, 68, 81}
    illegal = sum(n for op, n in total_hist.items() if op not in valid_ops)

    fwd = back = 0
    for i, step in enumerate(jmp_steps):
        if i + 1 >= len(cs):
            break
        cur = cs[step - 1]
        nxt = cs[step]
        if nxt > cur:
            fwd += 1
        else:
            back += 1

    first_out = out_steps[0] if out_steps else None
    last_out = out_steps[-1] if out_steps else None
    outs = len(out_steps)
    chars = [a % 256 for a in out_a]

    periods = {}
    for i in range(1, len(out_steps)):
        p = out_steps[i] - out_steps[i - 1]
        periods[p] = periods.get(p, 0) + 1
    top_periods = sorted(periods.items(), key=lambda kv: -kv[1])[:5]

    data_pc = sum(1 for op, c in zip(ops, cs) if c >= DATA_START)

    top_cells = sorted(((counts[c], c) for c in range(MEM_SIZE)), reverse=True)[:10]

    out_positions = {}
    for step, c in zip(out_steps, [cs[s - 1] for s in out_steps]):
        out_positions[c] = out_positions.get(c, 0) + 1

    print("QUINE STRUCTURE")
    print(f"source: {src_path.name}")
    print(f"run: {status} steps={steps:,} output={len(text):,} bytes")
    print(f"saltos: {len(jmp_steps):,} (fwd={fwd:,} back={back:,})")
    print(f"OUTs: {outs:,} (primer step={first_out:,} último={last_out:,})")
    print(f"períodos entre OUTs (top): {top_periods}")
    print(f"celdas nunca ejecutadas: {len(never):,} de {MEM_SIZE:,}")
    print(f"pasos en sección de datos (C>={DATA_START}): {data_pc:,} ({100.0*data_pc/n_steps:.2f}%)")
    print("--- pasos por región ---")
    for reg, (lo, hi) in regs.items():
        n = reg_steps[reg]
        print(f"  {reg:10s} [{lo:5d},{hi:5d}]: {n:12,} pasos ({100.0*n/n_steps:.2f}%)")
    print("--- opcodes totales ---")
    for op, n in sorted(total_hist.items()):
        print(f"  {OP_NAMES.get(op, 'ILLEGAL'):8s} (op {op:3d}): {n:12,} ({100.0*n/n_steps:.2f}%)")
    print(f"  ILLEGAL (fuera de tabla): {illegal:,}")
    print("--- top 10 celdas más visitadas ---")
    for n, c in top_cells:
        print(f"  c={c:5d}: {n:12,} pasos")
    print("--- OUTs por posición de C ---")
    for c, n in sorted(out_positions.items()):
        print(f"  c={c:5d}: {n:7,} OUTs")

    payload = {
        "version": "1",
        "source": src_path.name,
        "interpreter": "malbolge_interpreter.py (clasico corregido, on_step hook)",
        "run": {"status": status, "steps": n_steps, "output_len": len(text)},
        "regions": {reg: {"lo": lo, "hi": hi, "steps": reg_steps[reg], "opcodes": {str(k): v for k, v in op_hist[reg].items()}} for reg, (lo, hi) in regs.items()},
        "opcodes_total": {str(k): v for k, v in total_hist.items()},
        "illegal_ops": illegal,
        "jumps": {"total": len(jmp_steps), "forward": fwd, "backward": back},
        "outs": {"count": outs, "first_step": first_out, "last_step": last_out, "periods_top": dict(top_periods)},
        "never_executed_cells": len(never),
        "data_section_pc_steps": data_pc,
        "top_cells": [{"cell": c, "visits": n} for n, c in top_cells],
        "out_positions": {str(k): v for k, v in out_positions.items()},
    }
    out_json = src_path.with_name(f"quine_structure_{src_path.stem}.json")
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"json: {out_json.name} ({out_json.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())