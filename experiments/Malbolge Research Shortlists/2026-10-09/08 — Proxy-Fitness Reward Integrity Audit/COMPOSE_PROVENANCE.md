# Provenance del Experimento: Proxy-Fitness Reward Integrity Audit

## 1. Documento Fuente (Compose)
- **Ruta original:** `/home/danny/Development/ISyCo/OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/08 — Compose — Proxy-Fitness Reward Integrity Audit.docx`
- **SHA-256 del DOCX fuente:** `7859f226c19990144366794e8754f981d237afe5b82f7045311efad9ab986436`
- **Fecha de programación:** 2026-10-09
- **Clasificación:** `Malbolge Research Shortlists` / `OPENISY`
- **Estado original:** `PROPOSED / NOT EXECUTED`

## 2. Evidencia Externa de Referencia
- **Fuente:** Karwowski et al., *Likelihood hacking in probabilistic program synthesis*, UAI 2026 (Aug 17–21), PMLR 337 (`https://proceedings.mlr.press/v337/karwowski26a.html`).
- **Piso de evidencia:** Demostración de vulnerabilidad de reward hacking en síntesis de programas cuando se usan métricas de proxy heurísticas (coincidencia de prefijos, conteo de pasos, similitud aproximada de caracteres).

## 3. Hipótesis Exacta
Las métricas heurísticas de aptitud (proxy-fitness), tales como coincidencia de prefijo, similitud por distancia de edición o consumo de pasos, pueden puntuar a candidatos inválidos o truncados por encima de programas correctos o generar falsos positivos ("reward hacking"); únicamente una compuerta estricta de verificación de máquina virtual clásica previene estas aceptaciones erróneas.

## 4. Criterio de Falsación
Rechazar la hipótesis si en el corpus de prueba no se observa ningún exploit de métrica proxy, o si un candidato inválido logra superar una compuerta estricta de verificación exacta.
