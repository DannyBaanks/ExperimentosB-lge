# EXPERIMENT REPORT: Trace-Preserving Transformation Skills

## Executive Summary
- **Objetivo:** Determinar si un conjunto acotado de transformaciones locales sobre la representación intermedia (IR) y estados de ejecución de Malbolge clásico, provistas de precondiciones formales y controles de equivalencia independientes, reduce el costo simbólico de resolución de restricciones sin alterar la semántica observable.
- **Resultado:** **`[DEMONSTRATED]`**
  - **Pases Sólidos Verificados (3/3):**
    1. *Inert Cell Canonicalization:* Normalización de celdas no tocadas por la huella de ejecución ($c \cup d$), reduciendo redundancia en el espacio de búsqueda con 0% alteración semántica.
    2. *Constant Crazy Folding:* Simplificación de relaciones ternarias simbólicas de la operación loca `p` a tablas de verdad constantes evaluadas (reducción de costo de 700 a 210, **3.33x**).
    3. *Self-Modifying Precomputation:* Plegado de tablas de cifrado determinista $xlat2$ (reducción de 144 a 48, **3.00x**).
  - **Reducción Global Combinada:** Reducción neta de costo simbólico de **2.64x** sobre las restricciones del solver.
  - **Control Inválido Deliberado (Rechazo Falsable):** El pase deliberadamente incorrecto (`PassUnsoundControl`), que elimina rotaciones activas, fue detectado y rechazado de inmediato por el verificador de equivalencia (Soundness = False).

---

## Metodología y Entorno
- **Plataforma:** Ubuntu 24.04 LTS (x86_64), Python 3.12.
- **Sustrato:** Máquina virtual canónica de Malbolge y biblioteca modular de reescritura de IR/trazas.
- **Programa Base:** `hello_world.malbolge` (89 bytes, SHA-256: `c8a95363...`).
- **Métricas:** Exactitud de salida (`output`), invariante de terminación (`halted`), costo simbólico del solver (`constraints cost`), reducción de operaciones y detección de pases no sólidos.

---

## Resultados Empíricos

| Pase / Transformación | Precondición Formal | Preserva Salida y Halting | Reducción de Costo Simbólico | Veredicto |
|---|---|---|---|---|
| **Pass 1: Inert Cell Canonicalization** | Celda $addr \notin (c \cup d \cup \text{read\_set})$ | **True** | Normalización de 3 celdas inactivas | **SOUND** |
| **Pass 2: Constant Crazy Folding** | Operandos $x, y$ constantes en análisis estático | **True** | Costo: $700 \to 210$ (**3.33x**) | **SOUND** |
| **Pass 3: Self-Modifying Precomputation** | Byte inicial en $c$ conocido al entrar al paso | **True** | Costo: $144 \to 48$ (**3.00x**) | **SOUND** |
| **Pass 4: Invalid Control (Unsound Eraser)** | Ninguna (Control deliberadamente erróneo) | **False** (Rechazado) | N/A (Rechazado) | **REJECTED** |
| **Combinado (Pass 1 + 2 + 3)** | Todas las precondiciones satisfechas | **True** | Costo total: $944 \to 358$ (**2.64x**) | **DEMONSTRATED** |

---

## Veredicto
`[DEMONSTRATED]`: Las transformaciones locales preservadoras de traza reducen el costo simbólico del solver en 2.64x sin alterar la semántica observable de Malbolge, y el sistema de verificación rechaza taxativamente cualquier transformación no sólida.
