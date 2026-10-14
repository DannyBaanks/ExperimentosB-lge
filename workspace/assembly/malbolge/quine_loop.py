"""quine_loop.py -- anatomía del loop de impresión de la quine de Lutter.

Mide el intervalo entre OUTs consecutivos: qué celdas visita el PC entre
carácter y carácter, cuánto dura, cuánto ruido (NOP/ILLEGAL) hay por
carácter, y si el patrón cambia entre la pasada del código (0..29515) y
la de los datos (29516..59031).

Uso:
  python quine_loop.py [archivo.malbolge]

Salidas:
  - Resumen por stdout (primeros N intervalos + muestras del medio/final)
  - quine_loop_<archivo>.json
"""
from __future__ import annotations

import array
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
VALID = {4, 5, 23, 39, 40, 62, 68, 81}


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

    def hook(step, a, c, d, op, cell):
        cs.append(c)
        ops.append(op)
        if op == 5:
            out_steps.append(step)

    text, steps, status = mi.run(source, max_steps=MAX_STEPS, stdin_data="", on_step=hook)

    def interval_stats(lo_step, hi_step):
        lo = lo_step - 1
        hi = hi_step - 1
        cells = set(cs[lo:hi])
        ops_iv = ops[lo:hi]
        noise = sum(1 for op in ops_iv if op not in VALID)
        c0 = cs[lo]
        return {
            "span": hi_step - lo_step,
            "cells_visited": len(cells),
            "noise": noise,
            "noise_pct": 100.0 * noise / len(ops_iv),
            "min_c": min(cells),
            "max_c": max(cells),
        }

    samples = []
    first = [interval_stats(out_steps[i], out_steps[i + 1]) for i in range(10)]
    mid = interval_stats(out_steps[len(out_steps) // 2], out_steps[len(out_steps) // 2 + 1])
    last = interval_stats(out_steps[-2], out_steps[-1])
    for i, s in enumerate(first):
        samples.append({"sample": f"interval#{i}", **s})
    samples.append({"sample": "interval#medio", **mid})
    samples.append({"sample": "interval#final", **last})

    print("QUINE LOOP")
    print(f"source: {src_path.name}")
    print(f"OUTs: {len(out_steps):,}  (primer step {out_steps[0]:,}  último {out_steps[-1]:,})")
    print("--- intervalos (pasos entre OUT consecutivos) ---")
    for s in samples:
        print(
            f"  {s['sample']:16s} span={s['span']:5d} celdas={s['cells_visited']:3d} "
            f"ruido={s['noise']:4d} ({s['noise_pct']:.1f}%) c-min={s['min_c']} c-max={s['max_c']}"
        )
    print(f"--- total: pasos={steps:,} ILLEGAL={sum(1 for op in ops if op not in VALID):,} "
          f"({100.0*sum(1 for op in ops if op not in VALID)/steps:.1f}%)")

    payload = {
        "version": "1",
        "source": src_path.name,
        "run": {"status": status, "steps": steps, "output_len": len(text)},
        "outs": len(out_steps),
        "first_out_step": out_steps[0],
        "last_out_step": out_steps[-1],
        "interval_samples": samples,
    }
    out_json = src_path.with_name(f"quine_loop_{src_path.stem}.json")
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"json: {out_json.name} ({out_json.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())