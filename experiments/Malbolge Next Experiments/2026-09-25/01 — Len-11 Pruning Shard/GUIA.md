# GUIA DE OPERACIÓN Y REPRODUCCIÓN: Poda de Fragmento Len-11 (2026-09-25)

## 1. Propósito
Esta guía permite reproducir y verificar la poda de estados por signatura y divergencia temprana de prefijos en fragmentos deterministas de candidatos Malbolge de longitud 11, garantizando cero falsos negativos frente al evaluador de referencia.

## 2. Archivos del Experimento
- `len11_shard_pruner.py`: Máquina virtual optimizada `FastMalbolgeVM` y evaluador con poda por firma `(a, c, d)`.
- `test_len11_shard_pruner.py`: Suite de 5 pruebas unitarias en pytest.
- `results.json`: Reporte de resultados y veredicto general `DEMONSTRATED`.
- `hashes.json`: Manifiesto criptográfico SHA-256.

## 3. Comandos Ejecutados y Salidas Reales Verificadas

### Ejecución del Experimento
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/len11_shard_pruner.py"
```
Salida obtenida:
```
=== Malbolge Next Experiment: Len-11 Pruning Shard (2026-09-25) ===
Generated Shard of 250 len-11 candidates (Target: ASCII [72])
Baseline: 0 hits, 8186 steps in 0.019s
Pruned:   0 hits, 7143 steps, 177 pruned in 0.020s
Identical Hit Set: True
False Negatives: 0
Step Savings: 1043 (12.74%)
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/results.json
```

### Ejecución de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py::test_fast_vm_initialization_and_bounds PASSED [ 20%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py::test_shard_reproducibility PASSED [ 40%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py::test_pruning_soundness_no_false_negatives PASSED [ 60%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py::test_step_savings PASSED [ 80%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-09-25/01 — Len-11 Pruning Shard/test_len11_shard_pruner.py::test_end_to_end_verdict PASSED [100%]

============================== 5 passed in 0.09s ===============================
```
