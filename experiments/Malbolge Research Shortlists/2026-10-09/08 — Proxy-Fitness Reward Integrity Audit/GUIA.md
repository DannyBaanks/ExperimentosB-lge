# GUIA DE OPERACIÓN: Proxy-Fitness Reward Integrity Audit

## 1. El comando que viniste a buscar

```bash
python3 proxy_fitness_audit.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** Un puntaje heurístico alto no es un programa verificado. Las métricas de similitud de texto y tiempo de vida pueden premiar a un bucle infinito por encima de un programa que termina limpiamente. Jamás uses funciones de fitness heurísticas como condición de parada sin una compuerta estricta de ejecución de máquina virtual.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar la auditoría de inversión de ranking y reward hacking

```bash
python3 proxy_fitness_audit.py
```

**Salida real capturada en terminal:**

```text
================================================================================================
 EXPERIMENT REPORT: PROXY-FITNESS REWARD INTEGRITY AUDIT (UAI 2026)
================================================================================================
Formal Verdict: [DEMONSTRATED]
Proxy Hacking Inversions Detected: 1
Strict Gate False Accept Rate: 0.0%

Candidate ID               | Steps  | Status   | Fitness  | Gate Pass  | Proxy Hack
------------------------------------------------------------------------------------------------
C2_NON_TERMINATING_HACKER  | 5000   | TIMEOUT  | 1.0000   | False      | True      
C1_GENUINE_HIT             | 28     | HALTED   | 0.8011   | True       | False     
C3_ASCII_DISTANCE_HACKER   | 32     | HALTED   | 0.5973   | False      | False     
C4_LONG_LIVENESS_SPIN      | 5000   | TIMEOUT  | 0.2000   | False      | False     
C5_EARLY_CRASH             | 2      | CRASHED  | 0.0001   | False      | False     
================================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_proxy_fitness_audit.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/08 — Proxy-Fitness Reward Integrity Audit
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

test_proxy_fitness_audit.py ...                                          [100%]

============================== 3 passed in 0.01s ===============================
```

---

## 4. Cómo leer la salida

| Columna | Significado | Comportamiento Esperado |
|---|---|---|
| `Fitness` | Puntaje heurístico compuesto $[0, 1]$ | Puede sufrir inversión si premia liveness o prefijos parciales. |
| `Gate Pass` | Aceptación por la compuerta determinista de la VM | Solo debe ser `True` si la salida es exacta y el estado es `HALTED`. |
| `Proxy Hack` | Detección de exploit de recompensa | `True` cuando un programa inválido obtiene $\ge 0.70$ de fitness. |

---

## 5. Las trampas

1. **La trampa de premiar la longevidad:** Si premias a los candidatos por sobrevivir muchos pasos antes de fallar, los solvers genéticos convergerán hacia bucles infinitos en vez de programas que se detienen.
2. **La trampa de la distancia ASCII:** Un candidato que emite "HJ" en vez de "HI" está a solo 1 byte de distancia matemática, pero en semántica de computación es un error del 100%. Tratarlo como "95% correcto" lleva a la trampa de mínimos locales irresolubles en Malbolge.
