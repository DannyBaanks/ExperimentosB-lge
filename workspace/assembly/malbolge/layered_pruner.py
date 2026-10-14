"""layered_pruner.py -- poda por capas con múltiples targets de perturbación.

Estrategia:
  Para cada target en TARGETS:
    1. Escanea celdas candidatas en la versión actual
    2. Prueba perturbar cada candidata al target
    3. Aplica las que sobreviven
    6. Guarda versión y pasa al siguiente target
  Repite ciclo completo hasta convergencia global.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import malbolge_interpreter as mi

MAX_STEPS = 100_000_000
VALID = {4, 5, 23, 39, 40, 62, 68, 81}

# Targets a probar (opcode destino, nombre)
TARGETS = [
    (68, "NOP"),
    (4, "JMP"),
    (62, "CRAZY"),
    (39, "ROT"),
    (40, "DLOAD"),
    (23, "IN"),
    (5, "OUT"),
    (81, "END"),
]

# Celdas candidatas: todas las visitadas en la ejecución original
def get_executed_cells(source: str) -> dict[int, int]:
    """Retorna dict {cell: visit_count} de todas las celdas ejecutadas."""
    from collections import defaultdict
    counts = defaultdict(int)
    
    def hook(step, a, c, d, op, cell):
        counts[c] += 1
    
    import malbolge_interpreter as mi
    mi.run(source, max_steps=100_000_000, on_step=hook)
    return dict(counts)


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


def hash_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def test_perturbation(source: str, cell: int, new_value: int, ref_output: str) -> tuple[bool, str, int]:
    """Prueba perturbación. Retorna (survives, output_hash, steps)."""
    try:
        perturbed = patch_source(source, cell, new_value)
    except ValueError:
        return False, "", 0
    text, steps, status = mi.run(perturbed, max_steps=100_000_000, stdin_data="")
    match = (text == source)
    out_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]
    return match, out_hash, steps


def main():
    import sys
    from pathlib import Path
    
    src_path = Path(__file__).parent / "quine_pruned.malbolge"
    if not src_path.exists():
        src_path = Path(__file__).parent / "quine_lutter.malbolge"
    if not src_path.exists():
        print("no se encontró quine", file=sys.stderr)
        return 1
    
    original_source = src_path.read_text(encoding="utf-8")
    ref_output = original_source  # la quine original es el output de referencia
    
    current_source = src_path.read_text(encoding="utf-8")
    all_patches = []
    
    print("=== EXPLORADOR DE CAPAS ===")
    print(f"Baseline: {hashlib.sha256(open(src_path).read().encode()).hexdigest()[:16]}")
    
    # Obtener celdas ejecutadas con conteos
    print("\n[1] Mapeando celdas ejecutadas en versión actual...")
    executed = get_executed_cells(current_source)
    print(f"  Celdas ejecutadas únicas: {len(executed)}")
    
    # Ordenar por frecuencia (más visitadas primero - más impacto)
    sorted_cells = sorted(executed.keys(), key=lambda c: -executed[c])
    print(f"  Top 10 más visitadas: {[(c, executed[c]) for c in sorted_cells[:10]]}")
    
    all_patches = []
    round_num = 0
    max_rounds = 3
    
    for round_num in range(1, max_rounds + 1):
        print(f"\n=== RONDA GLOBAL {round_num} ===")
        
        # Re-escanear celdas ejecutadas en versión actual
        executed = get_executed_cells(current_source)
        sorted_cells = sorted(executed.keys(), key=lambda c: -executed[c])
        print(f"  Celdas ejecutadas: {len(executed)}")
        
        # Probar cada target
        for target_op, target_name in TARGETS:
            print(f"\n  --- Target: {target_name} (op {target_op}) ---")
            
            applied_this_target = 0
            for cell in sorted_cells:
                if cell in [p["cell"] for p in all_patches]:
                    continue
                
                try:
                    orig_val = cell_value_at(current_source, cell)
                except ValueError:
                    continue
                
                orig_op = (orig_val + cell) % 94
                if orig_op == target_op:
                    continue  # ya es ese target
                
                # Calcular valor que produce el target_op en esta celda
                new_val = (target_op - cell) % 94
                if not (33 <= new_val <= 126):
                    continue
                
                if new_val == orig_val:
                    continue
                
                # Test rápido
                match, out_hash, steps = test_perturbation(current_source, cell, new_val, current_source)
                if match:
                    # Aplicar
                    current_source = patch_source(current_source, cell, new_val)
                    all_patches.append({
                        "cell": cell,
                        "from": cell_value_at(current_source, cell),  # valor ANTES del patch
                        "to": new_val,
                        "target": target_name,
                        "visits": get_executed_cells(current_source).get(cell, 0)
                    })
                    print(f"  [OK] cell={cell} {target_name}({target_op}) applied")
                    applied_this_layer = True
                else:
                    pass  # falló
            
            if applied_this_layer:
                print(f"  [{target_name}] aplicados en esta capa")
    
    # Guardar versión final
    final_hash = hashlib.sha256(current_source.encode()).hexdigest()[:16]
    print(f"\n=== FINAL ===")
    print(f"Patches totales: {len(all_patches)}")
    for p in all_patches:
        print(f"  cell={p['cell']:5d} {p['target']}  {p['from']:3d} -> {p['to']:3d}")
    
    out_path = Path(__file__).parent / "quine_layered.malbolge"
    out_path.write_text(current_source, encoding="utf-8")
    print(f"Versión final guardada: quine_layered.malbolge")

if __name__ == "__main__":
    sys.exit(main())