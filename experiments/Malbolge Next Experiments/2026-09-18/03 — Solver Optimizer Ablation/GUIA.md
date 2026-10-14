# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Ablación del Optimizador del Solucionador (2026-09-18)

## 1. Propósito
Esta guía permite reproducir y verificar la ablación del optimizador del solucionador de Malbolge, comparando la búsqueda exhaustiva, el templado simulado y la guía semántica bajo presupuestos iguales de llamadas al evaluador, exigiendo verificación cruzada en Autobolge y Walbolge.

## 2. Archivos del Experimento
- `solver_optimizer_ablation.py`: Motor de ablación y verificadores independientes `AutobolgeVerifier` y `WalbolgeVerifier`.
- `test_solver_optimizer_ablation.py`: Suite de 4 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/solver_optimizer_ablation.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Solver / Optimizer Ablation (2026-09-18) ===
Target ASCII byte: 25
Exhaustive:       Hits =  0, First Hit = None, Success = 0.0%
Simulated Anneal: Hits =  0, First Hit = None, Success = 0.0%
Semantic Guided:  Hits = 16, First Hit = 5, Success = 16.0%
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/test_solver_optimizer_ablation.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/test_solver_optimizer_ablation.py::test_cross_verifier_agreement PASSED [ 25%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/test_solver_optimizer_ablation.py::test_equal_evaluator_budgets PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/test_solver_optimizer_ablation.py::test_semantic_guidance_improvement PASSED [ 75%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/03 — Solver Optimizer Ablation/test_solver_optimizer_ablation.py::test_end_to_end_verdict PASSED [100%]

============================== 4 passed in 0.31s ===============================
```
