# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Poda de Frontera Len-10 para Len-11 (2026-09-18)

## 1. Propósito
Esta guía permite reproducir y verificar la poda controlada de candidatos de longitud 11 basada en el suelo de evidencia negativo completado hasta longitud 10 (1,073,741,824 programas evaluados con 0 aciertos), verificando cero falsos negativos en fragmentos deterministas.

## 2. Archivos del Experimento
- `frontier_pruning_shard.py`: Motor de verificación y evaluador con poda por firma de estado `FrontierVM`.
- `test_frontier_pruning.py`: Suite de 5 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/frontier_pruning_shard.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Len-10 Frontier -> Safe Pruning for Len-11 (2026-09-18) ===
Preserved Evidence Floor (HI without input):
  len_7: {'candidates': 2097152, 'hits': 0, 'status': 'DEMONSTRATED'}
  len_8: {'candidates': 16777216, 'hits': 0, 'status': 'DEMONSTRATED'}
  len_9: {'candidates': 134217728, 'hits': 0, 'status': 'DEMONSTRATED'}
  len_10: {'candidates': 1073741824, 'hits': 0, 'wall_seconds': 10252.8, 'rate_progs_per_sec': 104727, 'status': 'DEMONSTRATED'}
  len_11_exhaustive: NOT_DEMONSTRATED

Testing Len-11 Shard: 250 candidates
Baseline: 0 hits, 6458 steps in 0.107s
Pruned:   0 hits, 5914 steps, 163 pruned in 0.115s
False Negatives: 0
Step Savings: 544 (8.42%)
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py::test_evidence_floor_constants PASSED [ 20%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py::test_shard_reproducibility PASSED [ 40%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py::test_pruning_soundness_zero_false_negatives PASSED [ 60%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py::test_step_savings PASSED [ 80%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-18/01 — Len-10 Frontier Pruning/test_frontier_pruning.py::test_end_to_end_verdict PASSED [100%]

============================== 5 passed in 0.33s ===============================
```
