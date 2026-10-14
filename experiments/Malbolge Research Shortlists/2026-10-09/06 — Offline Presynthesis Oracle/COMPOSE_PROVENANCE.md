# Provenance del Experimento: Offline Presynthesis Oracle

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/06 — Compose — Offline Presynthesis Oracle.docx`
- **SHA-256 del DOCX fuente:** `f690a25b66252547f44d6e3e44d25531b60628611b8359b44af2428e34c86be8`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Research Shortlists` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuente:** Dong et al., *Presynthesis / Foresighter*, PLDI 2026 (`https://arxiv.org/abs/2604.13290` / `https://doi.org/10.1145/3808288`).
- **Piso de evidencia:** Fase de semántica abstracta basada en autómatas de árboles y oráculos de poda precomputados fuera de línea para amortizar el costo de síntesis repetida.

## 3. Hipótesis Exacta
Precomputar abstracciones de transición y viabilidad para vecindarios de instrucciones de longitud fija en Malbolge amortiza el costo de poda sin incurrir en falsos negativos (soundness: ningún candidato válido es descartado por el oráculo abstracto), reduciendo el tiempo total de síntesis frente a la enumeración exhaustiva con VM completa.

## 4. Criterio de Falsación
Rechazar la hipótesis si el oráculo de presíntesis descarta algún candidato que el oráculo exhaustivo exacto acepta (falso negativo / unsoundness), o si el tiempo total (construcción + búsqueda) no mejora frente a la enumeración directa.
