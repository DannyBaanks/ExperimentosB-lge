# GUIA DE OPERACIÓN — 02: Symbolic Family Search (2026-10-02)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación de la búsqueda por familias simbólicas en Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/symbolic_family_search.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 02: Symbolic Family Search (2026-10-02) ===
Alphabet: ['(', '=', '<', '`', ':', '9'] (|Σ|=6), Max Length: 4, Space: 1296
Target Output Byte: 114 (ASCII 'r')
Exhaustive Baseline: 1296 evals, 80 hits in 0.059s
Symbolic Family Search: 1191 concrete evals, 105 candidates pruned in bulk
Family Hits: 80 in 0.126s
Result Parity: True (False Prunes: 0, Spurious: 0)
Concrete VM Reduction: 8.10% (105 executions saved)
Pruning Reasons: {'family_emits_wrong_byte_0_ne_114': 100, 'family_emits_wrong_byte_30_ne_114': 5}
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/test_symbolic_family.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/test_symbolic_family.py::test_symbolic_family_schema PASSED [ 25%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/test_symbolic_family.py::test_family_filter_soundness PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/test_symbolic_family.py::test_family_search_solution_parity PASSED [ 75%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/02 — Symbolic Family Search/test_symbolic_family.py::test_full_experiment_run PASSED [100%]

============================== 4 passed in 0.27s ===============================
```
