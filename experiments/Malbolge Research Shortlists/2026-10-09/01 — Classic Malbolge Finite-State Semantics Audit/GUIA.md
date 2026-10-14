# GUIA DE OPERACIÓN: Classic Malbolge Finite-State Semantics Audit

## 1. El comando que viniste a buscar

```bash
python3 audit_semantics.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** La operación crazy opera sin acarreo entre tritos; la cola de memoria no es estocástica ni infinita, sino estrictamente periódica con período divisor de 6 tras un transitorio de máximo 1 paso. Jamás modeles el relleno de memoria de Malbolge como ruido pseudoaleatorio en un solver.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar la auditoría de órbitas de estados y periodicidad de cola

```bash
python3 audit_semantics.py
```

**Salida real capturada en terminal:**

```text
========================================================================================
 EXPERIMENT REPORT: CLASSIC MALBOLGE FINITE-STATE SEMANTICS AUDIT
========================================================================================
Formal Verdict: [DEMONSTRATED]

--- 1. TRIT-PAIR RECURRENCE TRANSITIONS (9 States) ---
  Pair (y=0, x=0) -> Transient: 0, Period: 4, Cycle: [[0, 0], [0, 1], [1, 1], [1, 0]]
  Pair (y=0, x=1) -> Transient: 0, Period: 4, Cycle: [[0, 1], [1, 1], [1, 0], [0, 0]]
  Pair (y=0, x=2) -> Transient: 1, Period: 3, Cycle: [[2, 2], [2, 1], [1, 2]]
  Pair (y=1, x=0) -> Transient: 0, Period: 4, Cycle: [[1, 0], [0, 0], [0, 1], [1, 1]]
  Pair (y=1, x=1) -> Transient: 0, Period: 4, Cycle: [[1, 1], [1, 0], [0, 0], [0, 1]]
  Pair (y=1, x=2) -> Transient: 0, Period: 3, Cycle: [[1, 2], [2, 2], [2, 1]]
  Pair (y=2, x=0) -> Transient: 1, Period: 4, Cycle: [[0, 0], [0, 1], [1, 1], [1, 0]]
  Pair (y=2, x=1) -> Transient: 0, Period: 3, Cycle: [[2, 1], [1, 2], [2, 2]]
  Pair (y=2, x=2) -> Transient: 0, Period: 3, Cycle: [[2, 2], [2, 1], [1, 2]]

--- 2. PROGRAM MEMORY TAIL PERIODICITY & CROSS-VM PARITY ---
  Program: hello_world.malbolge   | Stripped:    88 | Period: 6 | Divides 6: True | VM Parity: True
  Program: quine_lutter.malbolge  | Stripped: 59032 | Period: 6 | Divides 6: True | VM Parity: True
========================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_semantics_audit.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/01 — Classic Malbolge Finite-State Semantics Audit
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 4 items

test_semantics_audit.py ....                                             [100%]

============================== 4 passed in 0.41s ===============================
```

---

## 4. Cómo leer la salida

| Campo | Valor esperado | Significado |
|---|---|---|
| `Formal Verdict` | `[DEMONSTRATED]` | La periodicidad y paridad entre VMs fueron verificadas. |
| `Cycle lengths` | 3 o 4 | Cada órbita de trito colapsa en un ciclo de longitud 3 o 4. |
| `Period: 6` | `6` | La combinación de los 10 tritos genera una palabra compuesta periódica de longitud 6. |
| `VM Parity: True` | `True` | La memoria cargada en Python y en C nativo es idéntica byte a byte. |

---

## 5. Las trampas

1. **La trampa del índice en `crazy`:** En la definición $m_i = \text{op}(m_{i-1}, m_{i-2})$, el primer argumento $x$ es $m_{i-1}$ y el segundo $y$ es $m_{i-2}$. Invertir el orden altera la tabla y destruye la periodicidad.
2. **La trampa del transitorio inicial:** La periodicidad de período 6 no comienza en el índice 0, sino tras consumir el código fuente y el transitorio inicial de 1-2 pasos de memoria.
