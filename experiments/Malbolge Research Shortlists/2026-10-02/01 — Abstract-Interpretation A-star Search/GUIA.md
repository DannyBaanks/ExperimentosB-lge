# GUIA DE OPERACIÓN — 01: Abstract-Interpretation A* Search (2026-10-02)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación del sintetizador guiado por interpretación abstracta para Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/abstract_astar_search.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 01: Abstract-Interpretation A* Search (2026-10-02) ===
Alphabet: ['(', '=', '<', '`', ':', '9'] (|Σ|=6), Max Length: 4, Space: 1296
Target Output Byte: 114 (ASCII 'r')
Exhaustive Oracle: 1296 nodes, 80 hits in 0.059s
Abstract A* Search: 1191 nodes, 105 pruned, 80 hits in 0.117s
Result Parity: True (False Prunes: 0, Spurious: 0)
Pruning Ratio: 8.10% (105/1296)
Pruning Reasons: {'provably_wrong_output_byte_30_ne_114': 5, 'provably_wrong_output_byte_0_ne_114': 100}
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py" -v
```

Salida verbatim obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 6 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_crazy_table PASSED [ 16%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_concrete_vm_execution PASSED [ 33%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_sound_domain_evaluation PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_exhaustive_oracle_consistency PASSED [ 66%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_abstract_astar_sound_parity PASSED [ 83%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/01 — Abstract-Interpretation A-star Search/test_abstract_astar.py::test_full_experiment_run PASSED [100%]

============================== 6 passed in 0.25s ===============================
```
