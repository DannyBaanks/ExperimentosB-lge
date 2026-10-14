# Provenance del Experimento: Quine Predicate and Source Identity

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/03 — Compose — Quine Predicate and Source Identity.docx`
- **SHA-256 del DOCX fuente:** `2be4d285f75c7b785a4e5dda8dd385d720c7278100ea6e02b334505c00409943`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Research Shortlists` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuente:** Lei Zhang (2026-09-20), *Self-Reference and Fixed Points in Formal Systems and Language Models* (`https://www.zhanglei.page/blog/self-reference-in-llms/`).
- **Piso de evidencia:** Distingue puntos fijos de Kleene de descripción de fuente, recursión de combinador Y y puntos fijos iterativos/de memoria. En Malbolge, la auto-encriptación destructiva crea una brecha entre la salida textual y el estado final de memoria.

## 3. Hipótesis Exacta
La igualdad exacta de bytes de fuente (`P_EXACT_BYTES`), la igualdad de código normalizado (`P_NORMALIZED_CODE`), la equivalencia conductual (`P_BEHAVIORAL_QUINE`) y la igualdad de imagen de memoria en runtime (`P_RUNTIME_IMAGE_FIXEDPOINT`) producen conjuntos de aceptación estrictamente distintos. La formulación explícita de estos predicados previene falsos positivos en solvers de síntesis.

## 4. Criterio de Falsación
Rechazar la hipótesis si el verificador acepta un no-quine conocido, rechaza un artefacto positivo confiable bajo su predicado declarado, o si los cuatro predicados colapsan en conjuntos idénticos de aceptación sobre el corpus de prueba.
