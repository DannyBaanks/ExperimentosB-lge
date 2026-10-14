# GUIA DE OPERACIÓN MANUAL: Habilidades de Transformación Preservando Traza

> **Regla de oro:** Jamás apliques reescrituras de código o IR en Malbolge de forma global; las transformaciones deben estar acotadas por precondiciones formales y contar con un verificador diferencial que rechace cualquier alteración semántica en la salida o en la terminación.

---

## 1. Propósito
Esta guía permite ejecutar el banco de pruebas de transformaciones de IR para Malbolge clásico, evaluando 3 pases sólidos (normalización inerte, plegado constante de crazy-op y precomputación de cifrado) junto con un control deliberadamente inválido.

---

## 2. Requisitos Previos
- Linux (Ubuntu 24.04 o compatible).
- Python 3.12+ con `pytest`.

---

## 3. Comandos de Ejecución

### A. Ejecutar el Experimento Principal
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/05 — Trace-Preserving Transformation Skills/trace_transforms.py"
```

**Salida real observada:**
```
=== Trace-Preserving Transformation Skills Experiment ===
Baseline: hello_world.malbolge (89 bytes)
Baseline run: steps=48, output=[72, 101, 108, 108, 111], time=0.844ms

--- Transformation Soundness & Reduction Matrix ---
Pass 1 (Inert Cell Canonicalization): Sound=True | Unused cells normalized: 3
Pass 2 (Constant Crazy Folding): Sound=True | Constraint cost: 700 -> 210 (3.33x reduction)
Pass 3 (Self-Modifying Precomputation): Sound=True | Encryption cost: 144 -> 48 (3.00x reduction)
Pass 4 (Invalid Control - Unsound Rotation): Sound=False (Must be False!)
Overall combined solver constraint reduction: 2.64x
Results saved to .../results.json
```

### B. Ejecutar la Suite de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/05 — Trace-Preserving Transformation Skills/test_trace_transforms.py" -v
```

**Salida real observada:**
```
test_baseline_execution PASSED [ 20%]
test_pass1_inert_cell_canonicalization_soundness PASSED [ 40%]
test_pass2_constant_crazy_folding_reduction PASSED [ 60%]
test_pass3_self_modifying_precomputation_reduction PASSED [ 80%]
test_falsification_unsound_control_rejection PASSED [100%]
============================== 5 passed in 0.36s ===============================
```

---

## 4. Interpretación de Resultados
1. **`Pass 1: Sound=True`**: Demuestra que canonizar celdas que caen fuera de la huella de ejecución no modifica la salida del programa.
2. **`Pass 2 (Constant Crazy Folding): 3.33x reduction`**: Al pre-evaluar operaciones locas constantes, las restricciones ternarias no lineales se convierten en igualdades directas.
3. **`Pass 4: Sound=False`**: Valida el mecanismo de defensa; un intento de eliminar instrucciones activas es identificado y abortado antes de llegar al solver.

---

## 5. Trampas y Resolución de Problemas
- **Trampa de optimización agresiva en bucles:** Si un bucle en Malbolge reutiliza celdas previamente cifradas, no se puede asumir invariancia de valor estático a lo largo de múltiples vueltas sin comprobar que $c$ o $d$ no las reescribieron.
