# GUIA DE OPERACIÓN: Quine Predicate and Source Identity

## 1. El comando que viniste a buscar

```bash
python3 quine_predicates.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** Un quine no es un concepto unívoco; la igualdad exacta de bytes ($P_1$) es estrictamente más exigente que la igualdad normalizada ($P_2$), y ninguna de las dos implica un punto fijo en la memoria ($P_4$). Jamás reportes un quine sintetizado sin declarar explícitamente bajo cuál de los 4 predicados fue verificado.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Evaluar la matriz de los 4 predicados sobre el corpus

```bash
python3 quine_predicates.py
```

**Salida real capturada en terminal:**

```text
============================================================================================
 EXPERIMENT REPORT: QUINE PREDICATE AND SOURCE IDENTITY (Lei Zhang 2026)
============================================================================================
Formal Verdict: [DEMONSTRATED]
Distinct Acceptance Sets Demonstrated: True

Fixture Name                 | P1 EXACT   | P2 NORMALIZED  | P3 BEHAVIOR  | P4 MEM_IMAGE
--------------------------------------------------------------------------------------------
CANONICAL_LUTTER_QUINE       | True       | True           | True         | False       
STRIPPED_WHITESPACE_QUINE    | False      | True           | False        | False       
MUTATED_1BYTE_QUINE          | False      | False          | False        | False       
HELLO_WORLD                  | False      | False          | False        | False       
============================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_quine_predicates.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/03 — Quine Predicate and Source Identity
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 4 items

test_quine_predicates.py ....                                            [100%]

============================== 4 passed in 0.87s ===============================
```

---

## 4. Cómo leer la salida

| Columna | Significado | Criterio de Aceptación |
|---|---|---|
| `P1 EXACT` | Igualdad exacta byte a byte ($source == output$) | Requiere que los saltos de línea y formato coincidan exactamente. |
| `P2 NORMALIZED` | Igualdad ignorando espacios en blanco ($strip(source) == strip(output)$) | Acepta programas válidos cuyo formato de saltos de línea difiere. |
| `P3 BEHAVIOR` | Punto fijo conductual ($f(f(P)) == f(P)$) | La salida es capaz de ejecutarse y reproducir el mismo comportamiento. |
| `P4 MEM_IMAGE` | Imagen de memoria invariable ($mem_{init} == mem_{final}$) | Prácticamente imposible en Malbolge clásico por la auto-encriptación destructiva. |

---

## 5. Las trampas

1. **La trampa de reclamar un quine más corto:** Si eliminas los saltos de línea del quine de Lutter pasa de 59,852 a 59,032 bytes y cumple $P_2$, pero **NO** cumple $P_1$. Reportarlo como un "quine más corto" sin aclarar el predicado es falsificación metodológica.
2. **La trampa de la auto-encriptación destructiva:** Esperar que un quine en Malbolge deje la memoria intacta ($P_4$) ignora que cada instrucción ejecutada se cifra irreversiblemente con la tabla `xlat2`.
