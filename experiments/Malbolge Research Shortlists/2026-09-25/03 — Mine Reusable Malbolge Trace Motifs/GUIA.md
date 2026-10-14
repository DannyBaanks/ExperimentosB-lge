# GUIA DE OPERACIÓN — 03: Mine Reusable Trace Motifs (2026-09-25)

Esta guía documenta los comandos ejecutados y la salida real obtenida durante la ejecución y validación de la minería de motivos de traza reutilizables para Malbolge.

## 1. Ejecución del Experimento

Comando ejecutado en la raíz del repositorio:
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/mine_trace_motifs.py"
```

Salida verbatim obtenida:
```
=== Malbolge Research Shortlist 03: Mine Reusable Trace Motifs (2026-09-25) ===
Mining trace motifs from intermediate exploration traces...
Top Mined Motif: '(=' (Frequency: 6)
Top 5 Candidate Motifs: [('(=', 6), ('==', 6), ('<=', 6), ('`=', 6), (':=', 6)]
Held-Out Target 57 ('9'): Scratch=52 evals ((=<`), Motif=16 evals ((=<`) -> Reduction: 69.23% (3.25x speedup)
Held-Out Target 60 ('<'): Scratch=59 evals ((=`:), Motif=23 evals ((=`:) -> Reduction: 61.02% (2.57x speedup)
Verdict: DEMONSTRATED
Results written to /home/danny/Development/ISyCo/EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/results.json
```

## 2. Ejecución de la Suite de Pruebas Unitarias

Comando ejecutado:
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/test_trace_motifs.py" -v
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

EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/test_trace_motifs.py::test_trace_motif_miner PASSED [ 33%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/test_trace_motifs.py::test_motif_search_soundness PASSED [ 66%]
EXPERIMENTS-COMPOSES-OPENAI/Malbolge Research Shortlists/2026-09-25/03 — Mine Reusable Malbolge Trace Motifs/test_trace_motifs.py::test_full_experiment_run PASSED [100%]

============================== 3 passed in 0.44s ===============================
```
