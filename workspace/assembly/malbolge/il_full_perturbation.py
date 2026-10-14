"""il_full_perturbation.py -- mapa completo de benevolencia de las celdas ILLEGAL.

Itera TODAS las celdas unicas donde el opcode ejecuto como ILLEGAL, perturba
cada una para forzar NOP (op 68) y reporta si la quine sobrevive.

Output:
  - Tabla por stdout con cell, value, op original, replacement, steps, hash, verdict
  - il_full_perturbation.json con resultados detallados + resumen
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
VALID = {4, 5, 23, 39, 40, 62, 68, 81}


def trace_illegals(src: str) -> tuple[set[int], dict[int, int]]:
    il_cells: set[int] = set()
    il_counts: dict[int, int] = {}

    def hook(step, a, c, d, op, cell):
        if op not in VALID:
            il_cells.add(c)
            il_counts[c] = il_counts.get(c, 0) + 1

    mi.run(src, max_steps=MAX_STEPS, stdin_data="", on_step=hook)
    return il_cells, il_counts


def cell_value_at(source_text: str, cell_addr: int) -> int:
    char_count = -1
    for ch in source_text:
        if not ch.isspace():
            char_count += 1
            if char_count == cell_addr:
                return ord(ch)
    raise ValueError(f"cell {cell_addr} not found in source (program has {char_count+1} cells)")


def patch_source(source_text: str, cell_addr: int, new_value: int) -> str:
    if not (33 <= new_value <= 126):
        raise ValueError(f"value {new_value} not printable")
    char_count = -1
    for i, ch in enumerate(source_text):
        if not ch.isspace():
            char_count += 1
            if char_count == cell_addr:
                return source_text[:i] + chr(new_value) + source_text[i + 1:]
    raise ValueError(f"cell {cell_addr} not found")


def nop_value_for_cell(c: int) -> int | None:
    v = (68 - c) % 94
    return v if 33 <= v <= 126 else None


def hash_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def main() -> int:
    src_name = sys.argv[1] if len(sys.argv) > 1 else "quine_lutter.malbolge"
    src_path = Path(__file__).parent / src_name
    if not src_path.exists():
        src_path = Path(src_name)
    if not src_path.exists():
        print(f"no se encontró: {src_name}", file=sys.stderr)
        return 2

    source = src_path.read_text(encoding="utf-8")
    ref_output = source
    ref_hash = hash_short(ref_output)
    ref_steps = 69_547_437

    print("Phase 1: trazando quine original...")
    il_cells, il_counts = trace_illegals(source)
    sorted_cells = sorted(il_cells, key=lambda c: -il_counts[c])
    print(f"  Celdas unicas con op ILLEGAL: {len(sorted_cells)}")

    print(f"\nPhase 2: perturbando {len(sorted_cells)} celdas (IL->NOP)...")
    results = []
    for i, c in enumerate(sorted_cells):
        try:
            original_value = cell_value_at(source, c)
        except ValueError:
            results.append({
                "cell": c, "skip": "not_in_source", "illegal_visits": il_counts.get(c, 0),
            })
            print(f"  [{i+1}/{len(sorted_cells)}] cell={c:5d}  SKIP (not in source, fill region)")
            continue
        original_op = (original_value + c) % 94
        nv = nop_value_for_cell(c)
        if nv is None:
            results.append({
                "cell": c, "original_value": original_value, "original_op": original_op,
                "illegal_visits": il_counts[c], "skip": "no_valid_nop",
            })
            print(f"  [{i+1:2d}/{len(sorted_cells)}] cell={c:5d} v={original_value:3d} op={original_op:3d}  SKIP (sin NOP printable)")
            continue
        perturbed = patch_source(source, c, nv)
        text, steps, status = mi.run(perturbed, max_steps=MAX_STEPS, stdin_data="")
        out_hash = hash_short(text)
        match = (text == ref_output)
        results.append({
            "cell": c, "original_value": original_value, "original_op": original_op,
            "illegal_visits": il_counts[c], "replacement_value": nv,
            "steps": steps, "status": status, "output_len": len(text),
            "output_hash": out_hash, "survives": match,
        })
        marker = "SURVIVE" if match else "ROMPE "
        print(f"  [{i+1:2d}/{len(sorted_cells)}] cell={c:5d} v={original_value:3d} op={original_op:3d} -> v={nv:3d}  "
              f"steps={steps:>11,}  hash={out_hash}  {marker}")

    survives = sum(1 for r in results if r.get("survives"))
    broken = sum(1 for r in results if "survives" in r and not r["survives"])
    skipped = sum(1 for r in results if r.get("skip"))

    print("\n========================================")
    print("MAPA DE BENEVOLENCIA DE LA QUINE")
    print(f"  Total celdas ILLEGAL:       {len(results)}")
    print(f"  TOLERABLES (sobrevive NOP): {survives}")
    print(f"  CRITICAS (rompe):           {broken}")
    print(f"  SKIP (sin NOP printable):   {skipped}")
    print(f"  baseline: steps={ref_steps:,} hash={ref_hash}")
    print("========================================")

    if survives > 0:
        print("\nCelda(s) tolerable(s):")
        for r in results:
            if r.get("survives"):
                print(f"  cell={r['cell']} visits={r['illegal_visits']:,}  v {r['original_value']} -> {r['replacement_value']}")

    out = src_path.with_name("il_full_perturbation.json")
    out.write_text(json.dumps({
        "baseline": {"steps": ref_steps, "output_hash": ref_hash, "output_len": len(ref_output)},
        "results": results,
        "summary": {"total": len(results), "survives": survives, "broken": broken, "skipped": skipped},
    }, indent=2), encoding="utf-8")
    print(f"\njson: {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())