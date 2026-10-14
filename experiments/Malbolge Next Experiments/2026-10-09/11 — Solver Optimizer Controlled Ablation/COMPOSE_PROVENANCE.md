# Provenance del Experimento: Solver Optimizer Controlled Ablation

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-10-09/11 — Compose — Solver Optimizer Controlled Ablation.docx`
- **SHA-256 del DOCX fuente:** `c6dffaec408e65382e7ad9d4364a0866c4cf0c3d7d7ee39db9bab06b5d56eb9b`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Next Experiments` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuentes:** Autobolge dense-Classic catalog & parity matrix (DannyBaanks), Lou Scheffer constraint theory, MalbolgeOperaSolver.
- **Piso de evidencia:** 417 casos dense-Classic y 299,593 entradas de catálogo sin discrepancias; 294,606 programas terminantes registrados. Familias call_return (396/396) y rot_sequence (34/34).

## 3. Hipótesis Exacta (H11)
La intervención de guía semántica (restricciones de viabilidad posicional y poda de prefijos inviables) mejora al menos una métrica primaria preregistrada (tasa de éxito verificado, llamadas medianas de evaluador al primer acierto) frente a controles emparejados de búsqueda aleatoria pura y recocido simulado (simulated annealing) bajo presupuestos iguales de evaluación.

## 4. Criterio de Falsación
Rechazar la hipótesis si el brazo semánticamente guiado no logra una mejora estadísticamente medible en la tasa de éxito o evaluaciones al primer acierto frente a los controles emparejados, o si genera algún falso positivo no verificable por la máquina virtual.
