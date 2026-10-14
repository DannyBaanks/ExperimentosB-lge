# Provenance del Experimento: Observable VM Conformance Matrix

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/07 — Compose — Observable VM Conformance Matrix.docx`
- **SHA-256 del DOCX fuente:** `1ec487eee0536a8bbf836ca184263fc53442b2d11747425bcf75b268bfde5473`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Research Shortlists` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuente:** Morse and Kozsik, *Emulation-Completeness of Programming Languages*, arXiv:2604.11021 (PLDI 2026).
- **Piso de evidencia:** Taxonomía de niveles de emulación y observabilidad:
  - **Tier 1 (Weak / Output-Only):** Igualdad de secuencia en stdout.
  - **Tier 2 (Medium / Steps & Halt):** Igualdad en pasos de ejecución y razón de parada.
  - **Tier 3 (Strong / Full Machine State):** Sincronización exacta ciclo a ciclo de registros $(a, c, d)$ y digest de memoria.

## 3. Hipótesis Exacta
Exigir el nivel de observabilidad Tier 3 (estado interno completo y digest de memoria) en lugar de Tier 1 (solo salida de texto) discrimina divergencias sutiles de máquina en casos de borde (manejo de EOF en `/`, opcodes no imprimibles, saltos computados y auto-cifrado) que las pruebas superficiales pasan por alto.

## 4. Criterio de Falsación
Rechazar la hipótesis si la clasificación por niveles no detecta discrepancias de estado entre implementaciones discrepantes, o si dos implementaciones formalmente divergentes obtienen falsamente un Tier 3 PASS.
