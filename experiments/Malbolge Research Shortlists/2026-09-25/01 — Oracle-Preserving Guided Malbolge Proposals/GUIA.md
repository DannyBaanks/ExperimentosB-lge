# GUIA DE OPERACIÓN — 01: Oracle-Preserving Guided Proposals (2026-09-25)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación de las propuestas guiadas que preservan el oráculo para Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/guided_proposals.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 01: Oracle-Preserving Guided Proposals (2026-09-25) ===
Alphabet: ['(', '=', '<', '`', ':', '9'], Length: 4, Target: 114, Matched Budget: 400, Seeds: 10
Unguided: Avg First Hit=18.0 evals, Avg Yield=25.2 hits
Guided:   Avg First Hit=5.5 evals, Avg Yield=54.8 hits
First-hit Speedup: 3.27x (18.0 vs 5.5)
Yield Multiplier: 2.17x (54.8 vs 25.2)
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/test_guided_proposals.py" -v
```

Salida verbatim obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 4 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/test_guided_proposals.py::test_concrete_vm_oracle_execution PASSED [ 25%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/test_guided_proposals.py::test_unguided_search_budget_enforcement PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/test_guided_proposals.py::test_guided_search_oracle_soundness PASSED [ 75%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/01 — Oracle-Preserving Guided Malbolge Proposals/test_guided_proposals.py::test_full_experiment_run PASSED [100%]

============================== 4 passed in 0.45s ===============================
```
