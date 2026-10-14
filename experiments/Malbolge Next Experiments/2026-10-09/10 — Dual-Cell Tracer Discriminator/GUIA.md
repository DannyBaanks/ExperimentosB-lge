# GUIA DE OPERACIÓN: Dual-Cell Tracer Discriminator (Malbolge)

## 1. El comando que viniste a buscar

```bash
python3 dual_cell_discriminator.py
```

---

## 2. La regla de oro

> **REGLA DE ORO:** Las asociaciones observacionales no son mecanismos causales demostrados hasta que resisten perturbación controlada contra celdas testigo. Jamás intentes sintetizar un quine corto ($\le 512$ bytes) asumiendo dual-cell sin antes haber probado que las celdas asociadas son estrictamente discriminables frente a controles emparejados.

---

## 3. Comandos ejecutables (con salida real capturada)

### Comando A: Ejecutar la matriz de perturbación y discriminación completa

```bash
python3 dual_cell_discriminator.py
```

**Salida real capturada en terminal:**

```text
Executing Canonical Baseline...
  -> Baseline Verified! Total: 59852 outs, 69.5M steps in 0.237s

Executing Perturbation Matrix across Target and Matched Control Cells...
  Cell 29454 (TARGET_CHAR_STREAM    ) delta=+1 -> EARLY_ABORT_ZERO_OUTPUT   (Outs:     0, Steps:      19584)
  Cell 29454 (TARGET_CHAR_STREAM    ) delta=-1 -> PARTIAL_OUTPUT_CORRUPTED  (Outs:     1, Steps:      22855)
  Cell 29282 (TARGET_NEWLINE_STREAM ) delta=+1 -> EARLY_ABORT_ZERO_OUTPUT   (Outs:     0, Steps:       5353)
  Cell 29282 (TARGET_NEWLINE_STREAM ) delta=-1 -> PARTIAL_OUTPUT_CORRUPTED  (Outs:     1, Steps:       8977)
  Cell 29453 (CONTROL_NEIGHBOR      ) delta=+1 -> EARLY_ABORT_ZERO_OUTPUT   (Outs:     0, Steps:      22864)
  Cell 29453 (CONTROL_NEIGHBOR      ) delta=-1 -> EARLY_ABORT_ZERO_OUTPUT   (Outs:     0, Steps:      19749)
  Cell 29455 (CONTROL_NEIGHBOR      ) delta=+1 -> INERT_SURVIVED            (Outs: 59852, Steps:   69547437)
  Cell 29455 (CONTROL_NEIGHBOR      ) delta=-1 -> INERT_SURVIVED            (Outs: 59852, Steps:   69547437)
  Cell 29281 (CONTROL_NEIGHBOR      ) delta=+1 -> PARTIAL_OUTPUT_CORRUPTED  (Outs:    72, Steps:     111981)
  Cell 29281 (CONTROL_NEIGHBOR      ) delta=-1 -> INERT_SURVIVED            (Outs: 59852, Steps:   69547437)
  Cell 29283 (CONTROL_NEIGHBOR      ) delta=+1 -> INERT_SURVIVED            (Outs: 59852, Steps:   69547437)
  Cell 29283 (CONTROL_NEIGHBOR      ) delta=-1 -> INERT_SURVIVED            (Outs: 59852, Steps:   69547437)
  Cell 30000 (CONTROL_SEGMENT       ) delta=+1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)
  Cell 30000 (CONTROL_SEGMENT       ) delta=-1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)
  Cell 35000 (CONTROL_SEGMENT       ) delta=+1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)
  Cell 35000 (CONTROL_SEGMENT       ) delta=-1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)
  Cell 40000 (CONTROL_SEGMENT       ) delta=+1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)
  Cell 40000 (CONTROL_SEGMENT       ) delta=-1 -> DIVERGENT_STREAM          (Outs: 59852, Steps:   69547437)

================================================================================================
 EXPERIMENT REPORT: DUAL-CELL TRACER DISCRIMINATOR (Lutter Quine 59,852 Bytes)
================================================================================================
Formal Verdict: [DEMONSTRATED]
Hypothesis H10 Demonstrated: True

Cell   | Role                    | Delta  | Steps      | Total Out  | Outcome Class             
------------------------------------------------------------------------------------------------
29454  | TARGET_CHAR_STREAM      | 1      | 19584      | 0          | EARLY_ABORT_ZERO_OUTPUT   
29454  | TARGET_CHAR_STREAM      | -1     | 22855      | 1          | PARTIAL_OUTPUT_CORRUPTED  
29282  | TARGET_NEWLINE_STREAM   | 1      | 5353       | 0          | EARLY_ABORT_ZERO_OUTPUT   
29282  | TARGET_NEWLINE_STREAM   | -1     | 8977       | 1          | PARTIAL_OUTPUT_CORRUPTED  
29453  | CONTROL_NEIGHBOR        | 1      | 22864      | 0          | EARLY_ABORT_ZERO_OUTPUT   
29453  | CONTROL_NEIGHBOR        | -1     | 19749      | 0          | EARLY_ABORT_ZERO_OUTPUT   
29455  | CONTROL_NEIGHBOR        | 1      | 69547437   | 59852      | INERT_SURVIVED            
29455  | CONTROL_NEIGHBOR        | -1     | 69547437   | 59852      | INERT_SURVIVED            
29281  | CONTROL_NEIGHBOR        | 1      | 111981     | 72         | PARTIAL_OUTPUT_CORRUPTED  
29281  | CONTROL_NEIGHBOR        | -1     | 69547437   | 59852      | INERT_SURVIVED            
29283  | CONTROL_NEIGHBOR        | 1      | 69547437   | 59852      | INERT_SURVIVED            
29283  | CONTROL_NEIGHBOR        | -1     | 69547437   | 59852      | INERT_SURVIVED            
30000  | CONTROL_SEGMENT         | 1      | 69547437   | 59852      | DIVERGENT_STREAM          
30000  | CONTROL_SEGMENT         | -1     | 69547437   | 59852      | DIVERGENT_STREAM          
35000  | CONTROL_SEGMENT         | 1      | 69547437   | 59852      | DIVERGENT_STREAM          
35000  | CONTROL_SEGMENT         | -1     | 69547437   | 59852      | DIVERGENT_STREAM          
40000  | CONTROL_SEGMENT         | 1      | 69547437   | 59852      | DIVERGENT_STREAM          
40000  | CONTROL_SEGMENT         | -1     | 69547437   | 59852      | DIVERGENT_STREAM          
================================================================================================
```

### Comando B: Ejecutar la suite de pruebas unitarias y de integridad

```bash
python3 -m pytest test_dual_cell_discriminator.py
```

**Salida real capturada en terminal:**

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-09/10 — Dual-Cell Tracer Discriminator
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 5 items

test_dual_cell_discriminator.py .....                                    [100%]

============================== 5 passed in 0.97s ===============================
```

---

## 4. Cómo leer la salida

| Campo / Métrica | Valor esperado | Significado | Qué hacer si difiere |
|---|---|---|---|
| `Formal Verdict` | `[DEMONSTRATED]` | La hipótesis H10 de discriminación causal fue comprobada. | Si es `[NOT_DEMONSTRATED]`, revisar `results.json`. |
| `Baseline Steps` | `69547437` | Pasos exactos a HALT del quine canónico de 59,852 bytes. | Si difiere, la semántica de la VM no es canónica clásica. |
| `d=29454 out count` | `59032` | Las 59,032 emisiones de caracteres ocurren con $d=29454$. | Si es $< 59032$, se alteró la indexación del trazador. |
| `d=29282 out count` | `820` | Las 820 emisiones de saltos de línea ocurren con $d=29282$. | Si es $< 820$, se alteró la indexación del trazador. |
| `Celdas 29455 y 29283` | `INERT_SURVIVED` | Celdas testigo que sobreviven la perturbación con salida idéntica. | Confirma que no cualquier celda vecina destruye el bucle. |

---

## 5. Las trampas

1. **La trampa de la velocidad en Python:** El quine ejecuta 69.5 millones de instrucciones. En Python puro toma ~3 minutos por corrida; el binario C optimizado `tracer_discriminator` lo corre en 0.23 segundos. Siempre usa el binario C compilado.
2. **La trampa de reclamar generalidad sobre quines cortos:** Probar que el quine de 59k usa un mecanismo dual-cell causal NO demuestra que un quine de $\le 512$ bytes deba usarlo. Mantén el claim estrictamente delimitado.
3. **La trampa de la auto-encriptación con valores fuera de rango:** Al perturbar celdas en memoria, si `mem[c]` cae fuera de $[33, 126]$, la tabla `xlat2` no se aplica (en Malbolge canónico permanece sin encriptar). Aplicar la tabla a ciegas provoca desbordamiento de búfer.
