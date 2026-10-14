# GUIA DE OPERACIÓN — 04: Cross-Language External Oracle Benchmark (2026-09-25)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación del benchmark entre lenguajes evaluado por un oráculo semántico externo.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/cross_lang_oracle_benchmark.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 04: Cross-Language External Oracle Benchmark (2026-09-25) ===
Target Specification: Emit byte 114 (ASCII 'r') upon execution
Shared External Oracle: ExternalSemanticOracle.verify(output)
Structured IR: 1 evals, Pass Oracle: True in 0.0000s
Linear Tape:   4 evals, Pass Oracle: True in 0.0000s
Malbolge VM:   16 evals, Pass Oracle: True in 0.0008s
All Representations Satisfy Shared Oracle: True
Synthesis Cost Scaling: Structured(1) < Tape(4) <= Malbolge(16): True
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/test_cross_lang.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/test_cross_lang.py::test_external_semantic_oracle PASSED [ 33%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/test_cross_lang.py::test_isolated_vm_execution PASSED [ 66%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/04 — Cross-Language External Oracle Benchmark/test_cross_lang.py::test_full_experiment_run PASSED [100%]

============================== 3 passed in 0.03s ===============================
```
