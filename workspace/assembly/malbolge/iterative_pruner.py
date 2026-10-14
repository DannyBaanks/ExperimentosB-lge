"""iterative_pruner.py -- poda iterativa de redundancias en la quine.

Estrategia:
  1. Carga quine original
  2. Aplica todas las perturbaciones NOP confirmadas (sobrevivientes)
  3. Mapea ILLEGAL en la nueva versión
  4. Prueba cada ILLEGAL -> NOP
  5. Aplica las que sobreviven
  6. Repite hasta convergencia (ninguna nueva superviviente)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
VALID = {4, 5, 23, 39, 40, 62, 68, 81}


def hash_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def cell_value_at(source_text: str, cell_addr: int) -> int:
    char_count = -1
    for ch in source_text:
        if not ch.isspace():
            if char_count == cell_addr:
                return ord(ch)
        char_count += 1
    raise ValueError(f"cell {cell_addr} not found")


def patch_source(source_text: str, cell_addr: int, new_value: int) -> str:
    if not (33 <= new_value <= 126):
        raise ValueError(f"value {new_value} not printable")
    char_count = -1
    for i, ch in enumerate(source_text):
        if not ch.isspace():
            if cell_addr == char_count:
                return source_text[:i] + chr(new_value) + source_text[i + 1:]
        char_count += 1
    raise ValueError(f"cell {cell_addr} not found")


def nop_value_for_cell(c: int) -> int | None:
    v = (68 - c) % 94
    return v if 33 <= v <= 126 else None


def trace_illegals(src: str) -> tuple[set[int], dict[int, int]]:
    il_cells: set[int] = set()
    il_counts: dict[int, int] = {}

    def hook(step, a, c, d, op, cell):
        if op not in VALID:
            il_cells.add(c)
            il_counts[c] = il_counts.get(c, 0) + 1

    mi.run(src, max_steps=MAX_STEPS, stdin_data="", on_step=hook)
    return il_cells, il_counts


def test_perturbation(source: str, cell: int, new_value: int, ref_output: str, ref_hash: str, ref_steps: int) -> dict:
    """Prueba cambiar cell a new_value. Retorna dict con resultado."""
    try:
        perturbed = patch_source(source, cell, new_value)
    except ValueError:
        return {"cell": cell, "skip": "patch_failed"}
    text, steps, status = mi.run(perturbed, max_steps=MAX_STEPS, stdin_data="")
    out_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]
    match = (text == ref_output)
    return {
        "cell": cell, "replacement": new_value, "steps": steps,
        "status": status, "output_len": len(text),
        "output_hash": out_hash, "survives": match,
    }


def prune_round(source: str, ref_output: str, ref_hash: str, applied_patches: list) -> tuple[str, list]:
    """Una ronda de poda: mapea ILLEGAL, prueba NOP, retorna source actualizado y patches aplicados."""
    print(f"\n--- Ronda: mapeando ILLEGAL en versión actual ---")
    il_cells, il_counts = trace_illegals(source)
    sorted_cells = sorted(il_cells, key=lambda c: -il_counts.get(c, 0))
    print(f"  Celdas ILLEGAL únicas: {len(sorted_cells)}")

    new_patches = []
    new_source = source
    for c in sorted(il_cells, key=lambda c: -il_counts.get(c, 0)):
        if c in [p["cell"] for p in applied_patches]:
            continue  # ya parcheada
        try:
            original_value = cell_value_at(new_source, c)
        except ValueError:
            continue
        original_op = (original_value + c) % 94
        nv = nop_value_for_cell(c)
        if nv is None:
            continue
        if original_op == 68:
            continue  # ya es NOP

        print(f"  probando cell={c} v={original_value} op={original_op} -> NOP({nv})...", end=" ", flush=True)
        result = test_perturbation(new_source, c, nv, source, hash_short(ref_output), 69547437)
        if result.get("survives"):
            print("[OK] SOBREVIVE")
            new_source = patch_source(new_source, c, nv)
            applied_patches.append({"cell": c, "from": original_value, "to": nv})
            new_patches.append({"cell": c, "from": original_value, "to": nv})
        else:
            print("[FAIL] rompe")

    return new_source, new_patches


def main() -> int:
    src_name = sys.argv[1] if len(sys.argv) > 1 else "quine_lutter.malbolge"
    src_path = Path(__file__).parent / src_name
    if not src_path.exists():
        src_path = Path(src_name)
    if not src_path.exists():
        print(f"no se encontró: {src_name}", file=sys.stderr)
        return 2

    original_source = src_path.read_text(encoding="utf-8")
    ref_output = original_source
    ref_hash = hashlib.sha256(ref_output.encode("utf-8", errors="replace")).hexdigest()[:16]

    print("=== PRUNER ITERATIVO ===")
    print(f"baseline: hash={hash_short(original_source)}")

    # Patches iniciales conocidos (las 7 supervivientes del experimento anterior)
    initial_patches = [
        {"cell": 29398, "from": 123, "to": 92},   # OUT->NOP
        {"cell": 29405, "from": 116, "to": 85},   # OUT->NOP
        {"cell": 29406, "from": 115, "to": 84},   # OUT->NOP
        {"cell": 29411, "from": 110, "to": 79},   # OUT->NOP
        {"cell": 29496, "from": 119, "to": 88},   # OUT->NOP
        {"cell": 29502, "from": 113, "to": 82},   # OUT->NOP
        {"cell": 29416, "from": 123, "to": 74},   # IN->NOP
    ]

    current_source = original_source
    all_patches = []

    # Aplicar patches iniciales
    print("Aplicando 7 NOP confirmadas...")
    for p in initial_patches:
        current_source = patch_source(current_source, p["cell"], p["to"])
        all_patches.append(p)
    print(f"  Patches aplicados: {len(all_patches)}")

    # Verificar que la v1 sigue siendo quine
    text, steps, status = mi.run(current_source, max_steps=MAX_STEPS, stdin_data="")
    if text == original_source:
        print(f"  [OK] v1 valida: steps={steps:,} hash={hashlib.sha256(current_source.encode()).hexdigest()[:16]}")
    else:
        print(f"  [FAIL] v1 ROTA: steps={steps:,} output_len={len(text)}")
        return 1

    # Iteraciones de poda
    round_num = 1
    while True:
        print(f"\n=== RONDA {round_num} ===")
        new_source, new_patches = prune_round(current_source, original_source, hash_short(original_source), all_patches)
        if not new_patches:
            print(f"  Convergencia: no hay nuevas supervivientes en ronda {round_num}")
            break
        current_source = new_source
        all_patches.extend(new_patches)
        print(f"  [OK] {len(new_patches)} nuevos patches aplicados. Total: {len(all_patches)}")
        # Verificar validez
        text, steps, status = mi.run(current_source, max_steps=MAX_STEPS, stdin_data="")
        if text != original_source:
            print(f"  [FAIL] VERSION ROTA tras ronda {round_num}! Revertiendo ultimo batch...")
            # Revertir últimos patches
            for p in reversed(new_patches):
                current_source = patch_source(current_source, p["cell"], p["from"])
                all_patches.pop()
            break
        print(f"  [OK] Ronda {round_num} valida: steps={steps:,}")
        round_num += 1

    # Verificación final
    text, steps, status = mi.run(current_source, max_steps=MAX_STEPS, stdin_data="")
    final_hash = hashlib.sha256(current_source.encode()).hexdigest()[:16]
    print(f"\n=== RESULTADO FINAL ===")
    print(f"  Patches totales aplicados: {len(all_patches)}")
    print(f"  Hash final: {final_hash}")
    print(f"  Steps: {steps:,}")
    print(f"  Output len: {len(text)}")
    print(f"  Quine válida: {'SÍ' if text == original_source else 'NO'}")

    # Guardar versión final
    out_path = Path(__file__).parent / "quine_pruned.malbolge"
    out_path.write_text(current_source, encoding="utf-8")
    print(f"  Versión podada guardada en: {out_path}")

    # Resumen patches
    print("\nPatches aplicados:")
    for p in all_patches:
        print(f"  cell={p['cell']:5d}  {p['from']:3d}(op={(p['from']+p['cell'])%94:3d}) -> {p['to']:3d}(NOP)")

    return 0


if __name__ == "__main__":
    sys.exit(main())