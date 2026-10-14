# GUIA DE OPERACIÓN MANUAL: Rebanado de Equivalencia por Byte de Salida

> **Regla de oro:** No compares el estado global de 59,049 celdas para verificar la salida de un programa en Malbolge; la auto-modificación cifra celdas no ejecutadas o intermedias que no afectan el byte emitido. Utiliza rebanado dinámico hacia atrás (*backward slicing*) desde la instrucción `<`.

---

## 1. Propósito
Esta guía permite ejecutar el experimento comparativo entre la verificación diferencial de traza completa y el rebanado dinámico causal hacia atrás sobre candidatos sintéticos de Malbolge clásico.

---

## 2. Requisitos Previos
- Linux (Ubuntu 24.04 o compatible).
- Python 3.12+ con `pytest`.

---

## 3. Comandos de Ejecución

### A. Ejecutar el Experimento Principal
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/04 — Output-Byte Equivalence Slicing/output_slicing.py"
```

**Salida real observada:**
```
=== Output-Byte Equivalence Slicing Experiment ===
Baseline source: hello_world.malbolge (89 bytes, SHA-256: c8a95363dbe2e997...)
Candidate corpus size: 6
Baseline executed steps: 48, outputs emitted: [72, 101, 108, 108, 111]
Backward slice for output[0]: 3 / 49 steps (6.1% of trace)

--- Verification Comparison Matrix ---
[base_identity] Oracle: True | Whole: True (240 ops) | Slice: True (11 ops) | Speedup: 21.82x
[inert_cell_mod] Oracle: True | Whole: False (30 ops) | Slice: True (11 ops) | Speedup: 2.73x
[inert_tail_mod] Oracle: True | Whole: True (240 ops) | Slice: True (11 ops) | Speedup: 21.82x
[active_op_corrupt_entry] Oracle: False | Whole: False (5 ops) | Slice: False (1 ops) | Speedup: 5.0x
[corrupt_output_to_halt] Oracle: False | Whole: False (16 ops) | Slice: False (1 ops) | Speedup: 16.0x
[arithmetic_cell_mod] Oracle: True | Whole: False (30 ops) | Slice: True (11 ops) | Speedup: 2.73x

Saved results to .../results.json
```

### B. Ejecutar la Suite de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/04 — Output-Byte Equivalence Slicing/test_output_slicing.py" -v
```

**Salida real observada:**
```
test_trace_generation_and_slice PASSED [ 25%]
test_soundness_identity PASSED [ 50%]
test_counterexample_recall PASSED [ 75%]
test_inert_mutation_precision PASSED [100%]
============================== 4 passed in 0.45s ===============================
```

---

## 4. Interpretación de Resultados
1. **`Backward slice for output[0]: 3 / 49 steps (6.1% of trace)`**: Únicamente 3 instrucciones de la traza influyen causalmente en el primer carácter emitido (`'H'`). El resto de instrucciones realizan inicializaciones o cálculos que no afectan este byte.
2. **`[inert_cell_mod] Whole: False | Slice: True`**: La traza completa reporta falsamente divergencia (`False`) debido a cambios en celdas de memoria que nunca se leen. El rebanado causal reconoce correctamente que el comportamiento observable es idéntico (`True`).
3. **`Speedup: 2.73x - 21.82x`**: Reducción drástica en el número de operaciones de comparación necesarias para certificar equivalencia o rechazar mutantes inválidos.

---

## 5. Trampas y Resolución de Problemas
- **Trampa de dependencias de control en saltos `'i'`:** Si una instrucción modifica el registro `c` vía salto (`'i'`), el rebanado debe rastrear la instrucción que modificó la celda leída por dicho salto; omitir esto produciría un rebanado inválido.
