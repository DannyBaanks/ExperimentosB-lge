# EXPERIMENT REPORT: Malbolge XOR-2048 Reproduction and Constraint Fixture

## Executive Summary
- **Objetivo:** Reproducir independientemente la ejecución y verificación de un programa en Malbolge clásico de tamaño inferior a 2048 bytes que calcula `y = x XOR 0x51` para cualquier byte de entrada $x \in [0, 255]$, documentar sus invariantes de ejecución (pasos exactos, legalidad de loader, fijación de mutaciones) y extraer el fixture de restricciones transferible para solvers.
- **Resultado:** **`[DEMONSTRATED]`**
  - **Legalidad de Loader:** 2,028 bytes legibles en ASCII [33..126], 0 errores de opcodes o caracteres prohibidos.
  - **Paridad de Oráculo (256/256):** El programa `gpt-6-astra.mal` emite exactamente $x \oplus 0x51$ y finaliza (`v`) para todos y cada uno de los 256 inputs posibles ($x \in 0..255$).
  - **Invariante de Pasos:** Exactamente **1,148 instrucciones ejecutadas** en todos y cada uno de los 256 casos (desviación estándar = 0).
  - **Fixture de Restricciones:** Tabla de datos solapada de 772 bytes en offset 124..896, 5 celdas mutables reescritas en 8 pasadas (`masks = [3, 20, 21, 18, 19, 24, 16, 7]`), profundidad de router 4.
  - **Evaluadores Independientes:** Paridad idéntica verificada entre el intérprete en C optimizado y la máquina virtual nativa en Python.

---

## Metodología y Entorno
- **Plataforma:** Ubuntu 24.04 LTS (x86_64), Python 3.12, GCC 13.3.
- **Semántica:** Malbolge Clásico (Ben Olmstead, 1998) con rotación ternaria de memoria (`xlat2`), pre-llenado loco `crazy_op` de 59,049 celdas, desofuscación `xlat1[(mem[c]-33+c)%94]`.
- **Artefactos Evaluados:**
  - `gpt-6-astra.mal` (2,028 bytes, SHA-256: `cb28ec05a4d9d8780273ed79eb49a6be4b9fcd7427e68578e5758f860a4a4015`).
  - Evaluador de referencia compilado en C (`c_evaluator.c`).
  - Evaluador de referencia en Python (`PythonClassicVM` en `reproduce_xor2048.py`).

---

## Resultados Empíricos

| Métrica | Valor Teórico / Esperado | Valor Medido | Estado |
|---|---|---|---|
| Tamaño del código fuente | $\le 2048$ bytes | 2,028 bytes | **PASS** |
| Errores de loader | 0 | 0 | **PASS** |
| Casos de prueba evaluados | 256 ($x \in 0..255$) | 256 | **PASS** |
| Casos que coinciden con $x \oplus 0x51$ | 256 | 256 (100.0%) | **PASS** |
| Cantidad de bytes emitidos por corrida | Exactamente 1 | 1 | **PASS** |
| Causa de terminación | Opcode `v` (HALT) | Opcode `v` (100%) | **PASS** |
| Pasos de ejecución por corrida | 1,148 | 1,148 | **PASS** |
| Tamaño de tabla solapada | 772 bytes | 772 bytes | **PASS** |
| Rendimiento de evaluación en C | $> 1,000$ casos/s | 22,232.7 casos/s | **PASS** |

---

## Falsificación y Controles
1. **Control de corrupción de loader:** Inyección de byte inválido (ej. espacio o carácter fuera del rango 33..126 dentro del bloque denso) falla inmediatamente el validador estático con error explícito.
2. **Control de oráculo:** Validación contra un oráculo falso ($x \oplus 0x50$) rechaza la ejecución sin falsos positivos.

---

## Veredicto
`[DEMONSTRATED]`: Reproducción independiente demostrada con 256/256 aciertos exactos a 1,148 pasos constantes, con fixture de restricciones extraído y verificado.
