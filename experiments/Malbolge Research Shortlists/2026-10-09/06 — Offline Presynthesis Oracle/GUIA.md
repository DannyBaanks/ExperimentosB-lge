# GUIA DE OPERACIÓN: Offline Presynthesis Oracle

## 1. El comando que viniste a buscar

```bash
python3 presynthesis_oracle.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** Un oráculo de presíntesis debe ser estrictamente *sound* (cero falsos negativos); podar ramas inviables es valioso sólo si ningún candidato válido es descartado antes de llegar a la máquina virtual. Jamás descartes prefijos basándote en heurísticas aproximadas; usa únicamente restricciones sintácticas formales de posición y semántica de parada inmediata.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar el benchmark comparativo del oráculo de presíntesis frente a búsqueda exhaustiva

```bash
python3 presynthesis_oracle.py
```

**Salida real capturada en terminal:**

```text
============================================================================================
 EXPERIMENT REPORT: OFFLINE PRESYNTHESIS ORACLE (PLDI 2026)
============================================================================================
Formal Verdict: [DEMONSTRATED]
Soundness (Zero False Negatives): True
Candidates Pruned: 214 / 216 (99.07%)
VM Calls Reduced: 216 -> 2
Speedup Factor: 134.61x

============================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias

```bash
python3 -m pytest test_presynthesis_oracle.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/06 — Offline Presynthesis Oracle
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

test_presynthesis_oracle.py ...                                          [100%]

============================== 3 passed in 26.03s ==============================
```

---

## 4. Cómo leer la salida

| Métrica | Valor obtenido | Significado |
|---|---|---|
| `Soundness` | `True` | Cero falsos negativos: todo programa válido fue retenido por el filtro. |
| `Candidates Pruned` | `99.07%` | Porcentaje de candidatos inviables descartados sin tocar la VM. |
| `Speedup Factor` | `134.61x` | Factor de aceleración en tiempo total frente a la enumeración directa. |

---

## 5. Las trampas

1. **La trampa de ignorar la posición:** En Malbolge, la validez de un carácter depende de su dirección $(code - 33 + c) \pmod{94}$. Un carácter válido en $c=0$ puede ser ilegal en $c=1$. El oráculo debe indexar por posición.
2. **La trampa de podar candidatos con prefijo de salida nula:** Si el objetivo de síntesis incluye bytes nulos (`\x00`), descartar la primera instrucción `<` sería un falso negativo. El oráculo debe condicionarse al objetivo declarado.
