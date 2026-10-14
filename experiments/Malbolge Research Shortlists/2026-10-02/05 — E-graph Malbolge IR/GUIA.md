# GUIA DE OPERACIÓN — 05: E-graph Malbolge IR Audit (2026-10-02)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la auditoría del documento no poblado `05 — Compose — E-graph Malbolge IR.docx`.

## 1. Ejecución de la Auditoría

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/egraph_malbolge_ir_audit.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 05: E-graph Malbolge IR Audit (2026-10-02) ===
File Size: 6485 bytes
SHA-256: 605f36aa07604a6a4e589cb8c21cea1a179caf0b888fb6f2da5a0de9a227512e
Extracted Paragraphs: 0, Tables: 0
Is Blank Template: True
Verdict: AUDIT_RECORDED_BLANK_ANOMALY
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/test_egraph_audit.py" -v
```

Salida verbatim obtenida:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/danny/Development/ISyCo
plugins: mock-3.15.1, asyncio-1.4.0, cov-7.1.0, anyio-4.15.1, timeout-2.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 2 items

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/test_egraph_audit.py::test_source_docx_properties PASSED [ 50%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/test_egraph_audit.py::test_audit_experiment_run PASSED [100%]

============================== 2 passed in 0.03s ===============================
```
