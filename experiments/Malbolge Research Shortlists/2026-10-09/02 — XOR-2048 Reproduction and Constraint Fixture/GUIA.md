# GUIA DE OPERACIÓN MANUAL: Reproducción Malbolge XOR-2048

> **Regla de oro:** No asumas que Malbolge ejecuta instrucciones fijas; la memoria se auto-modifica con `xlat2` en cada ciclo de reloj. Siempre valida la legalidad estática del código y su comportamiento de terminación sobre el espacio de entrada completo ($0..255$).

---

## 1. Propósito
Esta guía permite a un operador humano reproducir la ejecución independiente del programa en Malbolge clásico `gpt-6-astra.mal` (2,028 bytes) que calcula la función $y = x \oplus 0x51$, verificar los 256 casos de prueba del dominio y extraer el fixture de restricciones de diseño.

---

## 2. Requisitos Previos
- Linux (Ubuntu 24.04 o compatible).
- Python 3.12+ y GCC instalados.
- Compilador GCC para la ejecución nativa en C de alta velocidad (opcional para spot-check en Python, pero requerido para los 256 casos completos en milisegundos).

---

## 3. Comandos de Ejecución

### A. Ejecutar el Experimento Completo
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/02 — XOR-2048 Reproduction and Constraint Fixture/reproduce_xor2048.py"
```

**Salida real observada:**
```
=== XOR-2048 Malbolge Reproduction ===
Artifact: gpt-6-astra.mal (2028 bytes, SHA-256: cb28ec05a4d9d8780273ed79eb49a6be4b9fcd7427e68578e5758f860a4a4015)
Loader legality: PASS
Extracted constraint fixture: Table offset=124, len=772
PyVM in=  0 -> out= 81 (expected  81) steps=1148 match=True
PyVM in=  1 -> out= 80 (expected  80) steps=1148 match=True
PyVM in=  2 -> out= 83 (expected  83) steps=1148 match=True
PyVM in= 65 -> out= 16 (expected  16) steps=1148 match=True
PyVM in= 81 -> out=  0 (expected   0) steps=1148 match=True
PyVM in=128 -> out=209 (expected 209) steps=1148 match=True
PyVM in=254 -> out=175 (expected 175) steps=1148 match=True
PyVM in=255 -> out=174 (expected 174) steps=1148 match=True
C Evaluator: 256 / 256 perfect matches across all byte inputs
Step count distribution: {1148}
C Evaluator elapsed: 0.0115s (22232.7 cases/s)
Results written to .../results.json
```

### B. Ejecutar la Suite de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-09/02 — XOR-2048 Reproduction and Constraint Fixture/test_xor2048.py" -v
```

**Salida real observada:**
```
test_artifact_integrity_and_provenance PASSED [ 16%]
test_loader_legality PASSED [ 33%]
test_falsification_loader_corruption PASSED [ 50%]
test_constraint_fixture_structure PASSED [ 66%]
test_pyvm_boundary_cases PASSED [ 83%]
test_falsification_wrong_oracle PASSED [100%]
============================== 6 passed in 0.35s ===============================
```

---

## 4. Interpretación de Resultados
1. **`Loader legality: PASS`**: Significa que los 2,028 bytes cumplen la sintaxis exacta del cargador de Ben Olmstead (ASCII 33 a 126 y decodificación válida).
2. **`256 / 256 perfect matches`**: Confirma que para cualquier valor $x \in [0, 255]$ enviado a través de `stdin`, el programa emite exactamente 1 byte con valor $x \oplus 0x51$.
3. **`Step count distribution: {1148}`**: Demuestra que el programa tarda exactamente 1,148 pasos para cualquier entrada, confirmando ejecución determinista en tiempo constante.

---

## 5. Trampas y Resolución de Problemas
- **Trampa de orden de argumentos en `crz` (Crazy Op):** En Malbolge, la operación loca tiene orden estricto de parámetros: `op(x, y)` donde `y` indexa las filas y `x` las columnas en la tabla ternaria canónica. Invertir este orden rompe los cálculos internos.
- **Trampa de simulación en Python puro:** Ejecutar 256 casos en Python puro toma ~8 segundos debido a los 59,049 accesos a memoria por caso; el binario `c_evaluator` en C optimizado realiza la corrida en 11 milisegundos.
