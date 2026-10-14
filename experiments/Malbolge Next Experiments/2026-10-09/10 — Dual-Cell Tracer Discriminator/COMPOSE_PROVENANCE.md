# Provenance del Experimento: Dual-Cell Tracer Discriminator

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Next Experiments/2026-10-09/10 — Compose — Dual-Cell Tracer Discriminator.docx`
- **SHA-256 del DOCX fuente:** `22e93e8e414ab55bf842fe6485b80ba5282f041c986b3427cb35b7cadcfd6af2`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Next Experiments` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Artefacto Canónico Bajo Prueba
- **Archivo fuente:** `/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge`
- **SHA-256 del fuente:** `dca8476f8b70c8462c32f661f63c5f8b1ad6c33946b3c7a9a35186c824117d98`
- **Longitud exacta:** 59,852 caracteres brutos (59,032 caracteres de código imprimibles + 820 saltos de línea `\n`).
- **Piso de evidencia histórica a reproducir:**
  - Pasos exactos a HALT: `69,547,437`
  - Total de emisiones (`out` / opcode 5): `59,852`
  - Asociación de trazador observada:
    - Puntero $d = 29454$ asociado con las 59,032 emisiones de caracteres de código.
    - Puntero $d = 29282$ asociado con las 820 emisiones de saltos de línea (`\n`).

## 3. Hipótesis Exacta (H10)
Bajo condiciones de ejecución fijadas (semántica clásica canónica de Malbolge), perturbar las dos posiciones de datos observadas asociadas a la salida ($d = 29454$ y $d = 29282$) produce un cambio distintivo y reproducible en la salida exacta del quine frente a celdas de control emparejadas predeclaradas ($d \in \{29453, 29455, 29281, 29283, 30000, 35000\}$).

## 4. Criterio de Falsación
Rechazar la hipótesis si la traza canónica basal no puede ser reproducida de forma exacta (69,547,437 pasos y 59,852 emisiones), o si las perturbaciones en las celdas de control emparejadas muestran distribuciones de resultado indistinguibles de las celdas objetivo.
