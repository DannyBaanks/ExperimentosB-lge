# GUIA DE OPERACIÓN — 02: Prior-Guided Bounded Search (2026-09-25)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación de la búsqueda acotada guiada por distribución a priori para Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/prior_guided_search.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 02: Prior-Guided Bounded Search (2026-09-25) ===
Alphabet: ['(', '=', '<', '`', ':', '9'], Max Length: 4, Exact Space: 1296 candidates
Uniform Lexicographic: First Hit at eval 16, Total hits: 80 in 0.063s
  Coverage: {'10%': 3, '25%': 14, '50%': 35, '75%': 59, '100%': 80}
Prior-Guided Search:   First Hit at eval 3, Total hits: 80 in 0.065s
  Coverage: {'10%': 30, '25%': 50, '50%': 59, '75%': 70, '100%': 80}
Space Preservation: True (Sets Equal: True)
Hit Set Exact Parity: True (80 == 80)
First-Hit Speedup: 5.33x (16 evals vs 3 evals)
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/test_prior_guided.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/test_prior_guided.py::test_production_prior_scorer PASSED [ 33%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/test_prior_guided.py::test_search_completeness_and_space_invariance PASSED [ 66%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/02 — Prior-Guided Bounded Search/test_prior_guided.py::test_full_experiment_run PASSED [100%]

============================== 3 passed in 0.17s ===============================
```
