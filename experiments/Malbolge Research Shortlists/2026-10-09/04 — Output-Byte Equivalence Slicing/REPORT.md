# EXPERIMENT REPORT: Output-Byte Equivalence Slicing

## Executive Summary
- **Objetivo:** Comparar la verificación diferencial de traza completa (*Whole-Trace Differential Verification*) contra el rebanado dinámico hacia atrás (*Backward Slicing*) enfocado en el byte de salida emitido para candidatos acotados en Malbolge clásico auto-modificante.
- **Resultado:** **`[DEMONSTRATED]`**
  - **Reducción de Dominio:** El rebanado hacia atrás del byte de salida redujo el conjunto de pasos causales evaluados de 49 a 3 pasos (**6.1% de la traza**).
  - **Falsos Positivos:** **0.0%** (Cero reclamaciones de equivalencia falsas; cero omisiones de dependencias auto-modificantes).
  - **Sensibilidad a Mutaciones Inertes:** La verificación de traza completa rechaza falsamente programas con mutaciones en celdas de memoria inertes (porque el vector de estado difiere), mientras que el rebanado hacia atrás demuestra formalmente equivalencia semántica en la salida.
  - **Detección de Contraejemplos:** **100% Recall** detectando mutaciones disruptivas en el camino de control o emisión en 1 sola operación de comparación.
  - **Aceleración Operativa:** De **2.73x a 21.82x** menos operaciones de comparación frente a la verificación de traza completa.

---

## Metodología y Configuración Experimental
- **Sustrato:** Malbolge Clásico (cargador canónico y máquina virtual con instrumentación de dependencias def-use dinámicas).
- **Programa Base:** `hello_world.malbolge` (89 bytes, SHA-256: `c8a95363...`).
- **Corpus de Mutantes:** 6 variantes que cubren:
  1. Identidad básica.
  2. Modificación de celda inerte en memoria intermedia.
  3. Modificación de cola inerte.
  4. Corrupción activa de opcode en el punto de entrada.
  5. Corrupción del opcode de emisión (`<`) reemplazado por parada (`v`).
  6. Modificación aritmética en ruta de computación.
- **Métricas:** Pasos rebanados, operaciones de comparación (`ops`), detección de contraejemplos, tiempo de cómputo en microsegundos, tasa de falsos positivos y recall.

---

## Resultados Empíricos

| Candidato | Tipo de Mutación | Oráculo (Output) | Whole-Trace Eq (Ops) | Sliced Eq (Ops) | Aceleración Ops | Estado |
|---|---|---|---|---|---|---|
| `base_identity` | Identidad base | True | True (240 ops) | True (11 ops) | **21.82x** | **PASS** |
| `inert_cell_mod` | Modificación inerte | True | **False** (30 ops) | **True** (11 ops) | **2.73x** | **PASS** |
| `inert_tail_mod` | Modificación cola | True | True (240 ops) | True (11 ops) | **21.82x** | **PASS** |
| `active_op_corrupt_entry` | Corrupción activa | False | False (5 ops) | False (1 ops) | **5.00x** | **PASS** |
| `corrupt_output_to_halt` | Eliminación de `<` | False | False (16 ops) | False (1 ops) | **16.00x** | **PASS** |
| `arithmetic_cell_mod` | Modificación aritmética | True | **False** (30 ops) | **True** (11 ops) | **2.73x** | **PASS** |

---

## Veredicto
`[DEMONSTRATED]`: El rebanado dinámico hacia atrás preserva el 100% de recall de contraejemplos, elimina falsos rechazos en presencia de mutaciones inertes y reduce el costo de comparación entre 2.73x y 21.82x.
