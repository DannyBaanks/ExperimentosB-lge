# GUIA DE OPERACIÓN: Observable VM Conformance Matrix

## 1. El comando que viniste a buscar

```bash
python3 conformance_matrix.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** Que dos máquinas virtuales emitan la misma cadena en pantalla (Tier 1) no significa que sean la misma máquina. Solo la concordancia en pasos de ejecución (Tier 2) y la sincronización exacta de registros y memoria (Tier 3) certifica conformidad semántica clásica.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar la matriz de conformidad de 3 niveles entre VMs

```bash
python3 conformance_matrix.py
```

**Salida real capturada en terminal:**

```text
============================================================================================
 EXPERIMENT REPORT: OBSERVABLE VM CONFORMANCE MATRIX (PLDI 2026)
============================================================================================
Formal Verdict: [DEMONSTRATED]
Tier Discrimination Demonstrated: True

--- Pair: Python Canonical VM vs Native C Classic VM ---
  Tier 1 (Weak: Output Equivalence):         True
  Tier 2 (Medium: Step Count & Halt Status): True
  Tier 3 (Strong: Full Machine State Sync):   True

--- Pair: Python Canonical VM vs Divergent Mock VM ---
  Tier 1 (Weak: Output Equivalence):         True
  Tier 2 (Medium: Step Count & Halt Status): False
  Tier 3 (Strong: Full Machine State Sync):   False

============================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_conformance_matrix.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/07 — Observable VM Conformance Matrix
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

test_conformance_matrix.py ...                                           [100%]

============================== 3 passed in 0.35s ===============================
```

---

## 4. Cómo leer la salida

| Nivel | Nombre | Criterio de Pase |
|---|---|---|
| **Tier 1** | Débil (Output-Only) | La secuencia de bytes emitidos a stdout coincide. |
| **Tier 2** | Medio (Pasos y Parada) | El número de instrucciones ejecutadas y la razón de parada (`HALTED`) coinciden exactamente. |
| **Tier 3** | Fuerte (Estado Completo) | Los registros $(a, c, d)$ y el hash de la memoria coinciden en cada ciclo. |

---

## 5. Las trampas

1. **La trampa de confiar en un smoke test de "Hello World":** Un intérprete con saltos rotos o tablas de cifrado truncadas puede imprimir "Hello, world." mediante atajos pero fallar completamente en programas reales.
2. **La trampa de confundir variantes libres (Unshackled) con clásica:** En Malbolge Free/Unshackled el espacio de memoria no es de 59,049 celdas y los enteros no son módulo $3^{10}$. Mezclarlas en la misma matriz invalida los resultados.
