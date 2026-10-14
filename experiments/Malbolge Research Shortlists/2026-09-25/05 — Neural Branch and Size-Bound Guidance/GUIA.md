# GUIA DE OPERACIÓN — 05: Neural Branch and Size-Bound Guidance (2026-09-25)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación de la guía neuronal de ramas y estimación de cotas de tamaño para Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/neural_guidance_search.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 05: Neural Branch and Size-Bound Guidance (2026-09-25) ===
Alphabet: ['(', '=', '<', '`', ':', '9'], Max Length: 4, Space: 1296 candidates
Baseline Unguided: First Hit at eval 16, Total hits: 80 in 0.068s
Conservative Priority Guidance: First Hit at eval 3, Total hits: 80 in 0.070s
Bounded Guidance Mode: 346 candidates evaluated (950 pruned)
  First Hit at eval 3, Total hits: 50 in 0.018s
  False Negatives in Bounded Mode: 30
Priority Guidance Speedup: 5.33x (16 vs 3)
Conservative Mode Completeness: True (0 solutions lost)
Optimal Size Bound Prediction: True
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/test_neural_guidance.py" -v
```

Salida verbatim obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 3 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/test_neural_guidance.py::test_feature_extraction_and_prediction PASSED [ 33%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/test_neural_guidance.py::test_size_bound_estimator PASSED [ 66%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/05 — Neural Branch and Size-Bound Guidance/test_neural_guidance.py::test_full_experiment_run PASSED [100%]

============================== 3 passed in 0.26s ===============================
```
