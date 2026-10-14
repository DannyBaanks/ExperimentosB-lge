# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Ablación de Solucionador Relacional (2026-09-25)

## 1. Propósito
Esta guía permite reproducir y verificar la comparación controlada entre la búsqueda relacional guiada por catálogo y las estrategias de búsqueda aleatoria y templado simulado bajo presupuestos idénticos de llamadas al evaluador, garantizando que todo candidato exitoso pase por doble verificación independiente.

## 2. Archivos del Experimento
- `relational_solver_ablation.py`: Evaluador de estrategias y verificador independiente `MalbolgeVerifierVM`.
- `test_relational_solver.py`: Suite de 5 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/relational_solver_ablation.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Relational Solver Ablation (2026-09-25) ===
Preserved Evidence Floor: Catalog Size = 299593
Random Search:         Hits =  0, First Hit = None, Success Rate = 0.0%
Simulated Annealing:   Hits =  0, First Hit = None, Success Rate = 0.0%
Relational Guidance:   Hits =  6, First Hit = 24, Success Rate = 5.0%
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py::test_evidence_floor_constants PASSED [ 20%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py::test_independent_verifier_validates_target PASSED [ 40%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py::test_equal_evaluator_budgets PASSED [ 60%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py::test_relational_strategy_improves_success_rate PASSED [ 80%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/03 — Relational Solver Ablation/test_relational_solver.py::test_end_to_end_verdict PASSED [100%]

============================== 5 passed in 0.34s ===============================
```
