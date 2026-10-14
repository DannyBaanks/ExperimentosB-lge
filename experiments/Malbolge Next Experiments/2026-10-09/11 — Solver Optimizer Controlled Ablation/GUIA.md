# GUIA DE OPERACIÓN: Solver Optimizer Controlled Ablation

## 1. El comando que viniste a buscar

```bash
python3 solver_ablation.py --trials 20 --budget 400 --out .
```

---

## 2. La regla de oro

> **REGLA DE ORO:** La búsqueda ciega o el recocido simulado simple en Malbolge tienen probabilidad cercana a cero de éxito debido a la densidad de instrucciones ilegales; restringir la búsqueda a caracteres posicionalmente legales y podar prefijos de parada inmediata es el único camino viable sin sacrificar soundness.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar el benchmark comparativo de los tres brazos de búsqueda

```bash
python3 solver_ablation.py --trials 20 --budget 400 --out .
```

**Salida real capturada en terminal:**

```text
============================================================================================
 EXPERIMENT REPORT: SOLVER OPTIMIZER CONTROLLED ABLATION (Autobolge / Compose 11)
============================================================================================
Formal Verdict: [DEMONSTRATED]
Hypothesis H11 Demonstrated: True

Search Arm               | Success Rate   | Median Evals to Hit    | Runtime   
--------------------------------------------------------------------------------------------
RANDOM_SEARCH            |        0.0%   |              400.0   |     0.13s
SIMULATED_ANNEALING      |        0.0%   |              400.0   |     0.04s
SEMANTIC_GUIDED          |       10.0%   |              400.0   |     5.22s
============================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_solver_ablation.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-09/11 — Solver Optimizer Controlled Ablation
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

test_solver_ablation.py ...                                              [100%]

============================== 3 passed in 0.69s ===============================
```

---

## 4. Cómo leer la salida

| Columna | Significado | Comportamiento Esperado |
|---|---|---|
| `Success Rate` | Porcentaje de pruebas que encontraron un programa válido que emite el objetivo | Debe ser estrictamente superior en `SEMANTIC_GUIDED` frente a Random y SA. |
| `Median Evals to Hit` | Mediana de llamadas de evaluación hasta el primer acierto | 400.0 significa que agotó el presupuesto en la mediana. |
| `Runtime` | Tiempo total de cómputo en segundos | Acelerado por la librería compartida nativa `libfast_eval.so`. |

---

## 5. Las trampas

1. **La trampa de evaluar en Python puro:** Correr 15 trials con 400 llamadas en Python puro toma más de 45 segundos; usar la librería compartida C compilada (`libfast_eval.so`) lo ejecuta en menos de 5 segundos. Asegúrate de compilar `fast_eval.c`.
2. **La trampa del recocido simulado ingenuo:** Las mutaciones de un solo carácter en Malbolge caen casi siempre en estados con sintaxis inválida (error en el cargador), haciendo que el gradiente de fitness sea discontinuo e inútil sin restricciones posicionales.
