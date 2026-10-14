# Provenance del Experimento: Classic Malbolge Finite-State Semantics Audit

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/01 — Compose — Classic Malbolge Finite-State Semantics Audit.docx`
- **SHA-256 del DOCX fuente:** `d37cc3ce5f3909b0ff385f5dc88b133a188658b35179a5b0dac8a50580287e2c`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Research Shortlists` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuentes:** LangLib formal semantics & computability notes (Ilya Sergey / 2026-08-31):
  - `https://github.com/ilyasergey/langlib/blob/master/docs/malbolge/computability.md`
  - `https://github.com/ilyasergey/langlib/blob/master/docs/malbolge/spec.md`
- **Piso de evidencia:** Límite finito de control $59049^{59049} \times 59049^3 \times (n+1) \times 2$. Transiciones entre pares de tritos en la cola generada implican una periodicidad en palabras con período divisor de 6.

## 3. Hipótesis Exacta
Para programas clásicos válidos, la cola de memoria generada ($m_i = \text{op}(m_{i-1}, m_{i-2})$ para $i \ge \text{len}$) entra en un estado periódico con período fundamental que divide a 6; y las implementaciones independientes (Python canónico y C nativo de Ben Olmstead) mantienen estricta paridad en la carga, ciclo de cola y tratamiento de opcodes inválidos.

## 4. Criterio de Falsación
Rechazar la hipótesis si existe algún contraejemplo donde el período de la cola no divida a 6, o si se observa discrepancia de estado o salida entre los motores canónicos independientes.
