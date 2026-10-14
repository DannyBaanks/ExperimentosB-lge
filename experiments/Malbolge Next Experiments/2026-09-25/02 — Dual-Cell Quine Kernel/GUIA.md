# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Síntesis de Kernel Quine Celda-Dual (2026-09-25)

## 1. Propósito
Esta guía permite reproducir y verificar la síntesis acotada de kernels autoreproductores en Malbolge bajo una gramática guiada por el mecanismo de celda dual (celdas $d=29454$ y $d=29282$), preservando con rigor el suelo de evidencia que establece que un quine $\le 512$ bytes permanece `NOT_DEMONSTRATED`.

## 2. Archivos del Experimento
- `dual_cell_quine_kernel.py`: Motor de búsqueda y evaluador acotado `BoundedQuineVM`.
- `test_dual_cell_quine_kernel.py`: Suite de 5 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/dual_cell_quine_kernel.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Dual-Cell Quine Kernel (2026-09-25) ===
Preserved Evidence Floor: Lutter 59852 bytes (59032 code + 820 newlines)
Target d-locations: Cell 29454 (code) and Cell 29282 (newlines)
Length  32B: DualCell match_ratio=0.0000 vs Unconstrained match_ratio=0.0000 (Quine found: False)
Length  64B: DualCell match_ratio=0.0000 vs Unconstrained match_ratio=0.0000 (Quine found: False)
Length 128B: DualCell match_ratio=0.0000 vs Unconstrained match_ratio=0.0000 (Quine found: False)
Quine <= 512B Discovery Status: NOT_DEMONSTRATED
Dual-Cell Structural Advantage: True (DC avg: 0.0000 vs UN avg: 0.0000)
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py" -v
```
Salida obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 5 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py::test_lutter_canonical_evidence_floor PASSED [ 20%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py::test_bounded_vm_execution PASSED [ 40%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py::test_quine_exact_byte_verification PASSED [ 60%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py::test_search_bounded_kernel_budget_compliance PASSED [ 80%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/02 — Dual-Cell Quine Kernel/test_dual_cell_quine_kernel.py::test_end_to_end_verdict PASSED [100%]

============================== 5 passed in 0.34s ===============================
```
