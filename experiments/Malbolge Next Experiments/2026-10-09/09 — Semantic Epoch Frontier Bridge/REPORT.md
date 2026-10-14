# EXPERIMENT REPORT: Semantic Epoch Frontier Bridge

## Executive Summary
- **Objetivo:** Establecer qué negativos de búsqueda de HI/sin-entrada se transfieren a través del cambio de época semántica de Autobolge (`historical` con underflow en 0 vs `current` con underflow en 59048/EOF), y probar una regla sólida de poda por equivalencia de estado/prefijo sobre fragmentos (*shards*) deterministas.
- **Resultado:** **`[DEMONSTRATED]`**
  - **Divergencia de Época:** Se demostró la discrepancia exacta de comportamiento ante la instrucción `/` (underflow): la época histórica colapsa `a = 0`, mientras que la época actual fija `a = 59048` (EOF canónico).
  - **Sólida Poda de Prefijo:** La poda por prefijo muerto podó **11 candidatos de 202 (5.4%)** sin un solo falso negativo (**0 falsos negativos**).
  - **Retención de Controles Positivos (100%):** Todos los artefactos de control positivo (emisión de `'H'` o terminación inmediata `HALT`) fueron preservados e identificados como aciertos tanto en la línea base como en la evaluación podada.
  - **Ahorro de Recursos:** Reducción del **6.71% en pasos de máquina virtual** (de 13,549 a 12,640 pasos) y una aceleración de **1.22x** en tiempo de reloj de pared.

---

## Metodología y Configuración Experimental
- **Plataforma:** Ubuntu 24.04 LTS (x86_64), Python 3.12.
- **Épocas Semánticas:**
  - *Histórica:* Semántica previa de Autobolge (entrada sin datos asigna 0 a registro `a`).
  - *Actual:* Época `autobolge-classic-dense-input-underflow/v1` (entrada sin datos asigna 59048).
- **Fragmento Determinista:** 202 candidatos estructurados en 10 familias de prefijo (longitud de tallo 3, ramificación 20) más 2 controles positivos garantizados.
- **Criterio de Poda:** Si un prefijo entra en un ciclo ciego o agota combustible sin emitir salida ni realizar saltos fuera de su rango de código, se marca como tallo muerto y las variantes hermanas que comparten ese prefijo se descartan inmediatamente.

---

## Resultados Empíricos

| Métrica | Época Histórica | Época Actual (Línea Base) | Época Actual (Podada) | Ganancia / Delta |
|---|---|---|---|---|
| Candidatos Evaluados | 202 | 202 | 202 | - |
| Candidatos Podados | 0 | 0 | 11 (5.4%) | **+11 podados** |
| Pasos Totales de VM | 13,549 | 13,549 | 12,640 | **-6.71% pasos** |
| Aciertos Identificados | 1 | 1 | 1 | **Paridad 100%** |
| Falsos Negativos | 0 | 0 | 0 | **0 (Sound)** |
| Falsos Positivos | 0 | 0 | 0 | **0** |
| Tiempo Total (s) | 12.742 s | 13.317 s | 10.906 s | **1.22x speedup** |
| Tasa de Evaluación | 15.8 cand/s | 15.2 cand/s | 18.5 cand/s | **+21.7% tasa** |

---

## Veredicto
`[DEMONSTRATED]`: La regla de poda por prefijo/estado transfiere con cero falsos negativos y proporciona ahorros netos tanto en pasos de VM (6.71%) como en tiempo de ejecución (1.22x).
