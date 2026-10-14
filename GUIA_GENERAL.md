# GUÍA OPERATIVA Y METODOLÓGICA — EXPERIMENTOSBÖLGE

Esta guía describe cómo utilizar el repositorio como base de datos viva para consultar, reutilizar y diseñar nuevos experimentos de Malbolge.

---

## 1. Consultar experimentos previos

Cuando surja una nueva hipótesis sobre síntesis de código, quines o análisis de trazas en Malbolge:

1. Revisa la matriz en [README.md](README.md) para localizar la técnica más cercana.
   - Para explosión combinatoria en búsquedas de longitud >= 11, revisa `Len-11 Semantic Pruning Shard` y `Abstract-Interpretation A-star Search`.
   - Para quines y auto-modificación, revisa `Dual-Cell Quine Kernel` y `Quine Predicate and Source Identity`.
   - Para discrepancias entre emuladores, revisa `Observable VM Conformance Matrix` y `Classic Malbolge Finite-State Semantics`.
   - Para optimización y poda de espacios de búsqueda, revisa `E-graph Malbolge IR` y `Mine Reusable Malbolge Trace Motifs`.

2. Inspecciona `REPORT.md` y `results.json` para conocer el resultado medido, el baseline, los controles y los límites del claim.

3. Reutiliza runners, fixtures y utilidades sólo después de comprobar sus supuestos y alcance.

---

## 2. Contrato para nuevos experimentos

Cuando aplique, un experimento debe conservar seis artefactos:

1. **`COMPOSE_PROVENANCE.md`**
   - Título, fecha y fuente.
   - Hipótesis falsificable y condiciones de rechazo.
   - Hash del material fuente cuando corresponda.

2. **Runner `.py`**
   - No destructivo por defecto.
   - Genera métricas estructuradas en `results.json`.
   - Distingue claramente éxito de ejecución y veredicto experimental.

3. **Suite `test_*.py`**
   - Casos principales, límites y controles negativos.
   - Los tests validan el comportamiento cubierto; no amplían por sí solos el alcance del claim.

4. **`REPORT.md`**
   - Resultados cuantitativos.
   - Baseline y candidato cuando aplique.
   - Gates de verificación y limitaciones.

5. **`GUIA.md`**
   - Reproducción paso a paso.
   - Comandos reales y salidas relevantes.

6. **`hashes.json`**
   - Manifiesto SHA-256 de los artefactos que forman parte de la evidencia.

Los veredictos deben conservar semántica explícita, por ejemplo `DEMONSTRATED`, `PARTIAL`, `BLOCKED`, `FALSIFIED` o `NOT_DEMONSTRATED`, según el experimento.

---

## 3. Comandos útiles

```bash
# Validar toda la base de datos
pytest -v

# Ejecutar pruebas con cobertura, si pytest-cov está instalado
pytest --cov=experiments

# Ejecutar sólo Malbolge Next Experiments
pytest "experiments/Malbolge Next Experiments" -v

# Ejecutar sólo Malbolge Research Shortlists
pytest "experiments/Malbolge Research Shortlists" -v
```

---

## 4. Disciplina de evidencia

Antes de elevar un resultado a claim:

1. registra el input exacto;
2. conserva versiones o hashes de herramientas relevantes;
3. separa artefacto de build, implementación y comportamiento observado;
4. incluye controles negativos cuando sean posibles;
5. documenta contraejemplos y resultados falsificados;
6. evita reescribir findings históricos: corrige con addenda cuando importe conservar provenance.

El objetivo del repositorio no es acumular resultados verdes, sino conservar experimentos que otra persona pueda inspeccionar y reproducir.
