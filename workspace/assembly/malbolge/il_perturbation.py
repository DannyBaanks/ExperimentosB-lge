"""il_perturbation.py -- test: ¿son las celdas ILLEGAL ruido o parte del mecanismo?

Hipotesis: 36.97M pasos ILLEGAL (53.2% del quine). ¿Son necesarios?

Experimento:
  1. Carga y traza la quine. Encuentra celdas unicas donde op ILLEGAL ocurre.
  2. Para cada celda ILLEGAL: calcula el valor que haria op=68 (NOP).
  3. Patchea el source con ese valor, re-ejecuta la quine completa.
  4. Compara output vs source byte a byte.

Categorias:
  - SOBREVIVE: output identico al source (la celda era ruido tolerable)
  - ROMPE: output difiere (la celda era necesaria aunque ilegal)
  - SKIP: no hay valor printable (33-126) que produzca NOP en esa direccion
"""
from __future__ import annotations

import array
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
VALID = {4, 5, 23, 39, 40, 62, 68, 81}
N_TOP = 8


def trace_illegals(src: str) -> tuple[set[int], dict[int, int]]:
    cs = array.array("H")
    ops = array.array("B")
    il_cells: set[int] = set()
    il_counts: dict[int, int] = {}

    def hook(step, a, c, d, op, cell):
        cs.append(c)
        ops.append(op)
        if op not in VALID:
            il_cells.add(c)
            il_counts[c] = il_counts.get(c, 0) + 1

    mi.run(src, max_steps=MAX_STEPS, stdin_data="", on_step=hook)
    return il_cells, il_counts


def patch_source(source_text: str, cell_addr: int, new_value: int) -> str:
    if not (33 <= new_value <= 126):
        raise ValueError(f"value {new_value} not printable ASCII")
    char_count = -1
    for i, ch in enumerate(source_text):
        if not ch.isspace():
            char_count += 1
            if char_count == cell_addr:
                return source_text[:i] + chr(new_value) + source_text[i + 1:]
    raise ValueError(f"cell {cell_addr} not found in source")


def nop_value_for_cell(c: int) -> int | None:
    """Valor v tal que (v + c) % 94 == 68 (NOP), o None si no cae en printable ASCII."""
    v = (68 - c) % 94
    return v if 33 <= v <= 126 else None


def main() -> int:
    src_name = sys.argv[1] if len(sys.argv) > 1 else "quine_lutter.malbolge"
    src_path = Path(__file__).parent / src_name
    if not src_path.exists():
        src_path = Path(src_name)
    if not src_path.exists():
        print(f"no se encontró el archivo: {src_name}", file=sys.stderr)
        return 2

    source = src_path.read_text(encoding="utf-8")
    ref_output = source

    print("Phase 1: trazando la quine original...")
    il_cells, il_counts = trace_illegals(source)
    print(f"  Celdas unicas con op ILLEGAL visitadas: {len(il_cells):,}")
    sorted_cells = sorted(il_cells, key=lambda c: -il_counts[c])
    print(f"  Top {N_TOP} por visitas ILLEGAL:")
    for c in sorted_cells[:N_TOP]:
        nv = nop_value_for_cell(c)
        flag = "" if nv is not None else "  [no valid NOP]"
        print(f"    cell={c:5d}  visitas_illegal={il_counts[c]:>10,}  NOP_value={nv}{flag}")

    print(f"\nPhase 2: perturbando top {N_TOP} celdas (IL -> NOP), ejecutando quine completa...")
    results = []
    for c in sorted_cells[:N_TOP]:
        nv = nop_value_for_cell(c)
        if nv is None:
            print(f"  cell={c:5d} SKIP (no valid NOP value)")
            results.append({"cell": c, "skip": "no_valid_nop"})
            continue
        perturbed = patch_source(source, c, nv)
        text, steps, status = mi.run(perturbed, max_steps=MAX_STEPS, stdin_data="")
        match = (text == ref_output)
        print(f"  cell={c:5d} -> NOP(v={nv}): status={status} steps={steps:,} "
              f"out_len={len(text):,} match={match}")
        results.append({
            "cell": c, "visits": il_counts[c], "nop_value": nv,
            "status": status, "steps": steps, "output_len": len(text), "match": match,
        })

    print("\n--- Resumen ---")
    survived = sum(1 for r in results if r.get("match"))
    broken = sum(1 for r in results if "match" in r and not r["match"])
    skipped = sum(1 for r in results if r.get("skip"))
    print(f"  SOBREVIVE (quine identica): {survived}/{N_TOP - skipped}")
    print(f"  ROMPE (output distinto):    {broken}/{N_TOP - skipped}")
    print(f"  SKIP (sin NOP printable):   {skipped}/{N_TOP}")

    out = src_path.with_name("il_perturbation_results.json")
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"  json: {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())