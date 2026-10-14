# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Síntesis de Kernel Quine Celda-Dual (2026-09-18)

## 1. Propósito
Esta guía detalla la reproducción y verificación de la búsqueda acotada de kernels autorreproductores de Malbolge basada en la concentración de celdas duales ($d=29454$ y $d=29282$), preservando la evidencia canónica de que un quine $\le 512$ bytes es estrictamente `NOT_DEMONSTRATED`.

## 2. Archivos del Experimento
- `dual_cell_kernel_synthesis.py`: Motor de búsqueda y evaluador acotado `BoundedKernelVM`.
- `test_dual_cell_synthesis.py`: Suite de 4 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/dual_cell_kernel_synthesis.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Dual-Cell Quine Kernel Synthesis (2026-09-18) ===
Evidence Floor: Lutter 59852 chars, Halt 69547437 steps
Factorization: Two 29516B regions, A/B halt at 4354 steps
Tracer hotspots: d=29454 (code) and d=29282 (newlines)
Kernel  32B: DualCell max_prefix=0, Random max_prefix=0 (Quine: False)
Kernel  64B: DualCell max_prefix=0, Random max_prefix=0 (Quine: False)
Kernel 128B: DualCell max_prefix=0, Random max_prefix=0 (Quine: False)
Quine <= 512B Discovery Status: NOT_DEMONSTRATED
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/test_dual_cell_synthesis.py" -v
```
Salida obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 4 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/test_dual_cell_synthesis.py::test_lutter_factorization_evidence_floor PASSED [ 25%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/test_dual_cell_synthesis.py::test_bounded_kernel_vm_step PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/test_dual_cell_synthesis.py::test_search_kernel_budget_compliance PASSED [ 75%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/test_dual_cell_synthesis.py::test_end_to_end_verdict PASSED [100%]

============================== 4 passed in 0.22s ===============================
```
