# GUIA OPERATIVA Y METODOLÓGICA — EXPERIMENTOSBÖLGE 😲

Esta guía describe cómo utilizar este repositorio como base de datos viva para consultar, reutilizar y diseñar **nuevos experimentos de Malbolge**.

---

## 1. Cómo Consultar Experimentos Previos

Cuando surja una nueva hipótesis sobre síntesis de código, quines o análisis de trazas en Malbolge:

1. **Revisa la matriz en [README.md](file:///home/danny/Development/ISyCo%20Git/EXPERIMENTOSBÖLGE/README.md)** para localizar la técnica más cercana:
   - ¿Problemas de explosión combinatoria al buscar cadenas de longitud $\ge 11$? Revisa `Len-11 Semantic Pruning Shard` y `Abstract-Interpretation A-star Search`.
   - ¿Diseño de quines y auto-modificación segura? Revisa los tres experimentos de `Dual-Cell Quine Kernel` y `Quine Predicate and Source Identity`.
   - ¿Comportamiento no determinista o discrepancias entre emuladores? Revisa `Observable VM Conformance Matrix` y `Classic Malbolge Finite-State Semantics Audit`.
   - ¿Optimización y poda de grafos de búsqueda? Revisa `E-graph Malbolge IR` y `Mine Reusable Malbolge Trace Motifs`.

2. **Inspecciona el `REPORT.md` y `results.json`** de ese experimento para conocer los números basales, la aceleración cuantitativa obtenida y los límites demostrados.

3. **Reutiliza los scripts ejecutores `.py` y fixtures**:
   - Los módulos contienen clases puras de simulación (`MalbolgeVM`, `EGraph`, `AStarSolver`, `PrunerShard`) que pueden ser importadas directamente en nuevos experimentos.

---

## 2. Contrato Obligatorio para Nuevos Experimentos

Cualquier nuevo experimento que se incorpore a esta base de datos semanal debe satisfacer el **Contrato de los 6 Artefactos**:

1. **`COMPOSE_PROVENANCE.md`**:
   - Título, fecha y fuente de inspiración (conversación con GPT, issue o paper de investigación).
   - Hipótesis falsificable explícita con condiciones de rechazo.
2. **Script ejecutor `.py`**:
   - Debe ser no destructivo.
   - Debe guardar sus métricas estructuradas en `results.json` con veredicto `DEMONSTRATED` o `NOT_DEMONSTRATED`.
3. **Suite de pruebas `test_*.py`**:
   - Al menos 2-4 pruebas unitarias que validen casos límite, controles negativos e hipótesis principal.
   - 100% PASS en `pytest`.
4. **`REPORT.md`**:
   - Resumen ejecutivo con tablas comparativas numéricas (baseline vs candidato).
   - Tabla de puertas de verificación lógica (`gates`).
5. **`GUIA.md`**:
   - Instrucciones paso a paso en español con comandos reales y salidas verbatim.
6. **`hashes.json`**:
   - Manifiesto criptográfico generado con SHA-256 de todos los archivos del directorio.

---

## 3. Comandos Útiles

```bash
# Validar toda la base de datos
pytest -v

# Ejecutar pruebas con reporte de cobertura
pytest --cov=experiments

# Ejecutar únicamente las pruebas de la serie 'Next Experiments'
pytest "experiments/Malbolge Next Experiments" -v

# Ejecutar únicamente las pruebas de 'Research Shortlists'
pytest "experiments/Malbolge Research Shortlists" -v
```

---

*Base de datos de experimentación radical en Malbolge — OpenISy / Danny.* 😲
