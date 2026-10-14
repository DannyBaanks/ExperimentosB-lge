# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Fragmento de Poda Semántica Len-11

## 1. Propósito
Esta guía permite reproducir y verificar el mecanismo de poda semántica de estado y prefijo en un fragmento (*shard*) determinista de candidatos Malbolge de longitud 11, comprobando un ahorro significativo de pasos de VM sin generar falsos negativos respecto a la línea base.

## 2. Archivos del Experimento
- `len11_semantic_pruning.py`: Generador de fragmento determinista y evaluadores con/sin poda.
- `test_len11_pruning.py`: Suite de 5 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/len11_semantic_pruning.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Len-11 Semantic Pruning Shard ===
Generated Shard of 300 len-11 candidates (Target: ASCII [72])
Baseline: 0 hits, 9722 steps in 14.854s
Pruned:   0 hits, 8633 steps, 206 pruned in 15.084s
Hits Match: True (False Negatives: 0)
Step Savings: 1089 steps (11.20%)
Verdict: DEMONSTRATED
Results saved to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py::test_crazy_operation_truth_table PASSED [ 20%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py::test_deterministic_shard_generation PASSED [ 40%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py::test_pruning_zero_false_negatives PASSED [ 60%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py::test_step_savings_achieved PASSED [ 80%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-03/01 — Len-11 Semantic Pruning Shard/test_len11_pruning.py::test_results_json_verdict_demonstrated PASSED [100%]

============================== 5 passed in 7.21s ===============================
```
