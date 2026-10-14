# EXPERIMENTOSBÖLGE

Repositorio de experimentos reproducibles sobre Malbolge.

EXPERIMENTOSBÖLGE reúne hipótesis, implementaciones, pruebas, resultados y evidencia de experimentos derivados de briefs y composes de investigación. La intención es que cada resultado pueda inspeccionarse, repetirse y reutilizarse desde otros repositorios del ecosistema ISyCo.

La **Ö** es simplemente parte del nombre visual del proyecto.

---

## Qué contiene

Cada experimento intenta convertir una hipótesis en un artefacto reproducible:

- una pregunta o hipótesis falsificable;
- un runner que genera resultados estructurados;
- pruebas automatizadas y controles;
- un reporte con límites y resultados;
- una guía de reproducción;
- hashes de integridad y provenance del material fuente cuando aplica.

El repositorio también sirve como biblioteca común de fixtures, oráculos, heurísticas y patrones de verificación para otros proyectos de Malbolge.

---

## Reutilización

### Oráculos y poda

Los experimentos de **Malbolge Next Experiments** contienen estrategias de poda de frontera, discriminación de ciclos y búsqueda sobre programas cortos que pueden reutilizarse desde sintetizadores, analizadores o compiladores inversos.

### Conformidad de VM

El workspace incluye intérpretes y especímenes de referencia. Experimentos como **Observable VM Conformance Matrix** y **Classic Malbolge Finite-State Semantics** sirven para comparar runtimes independientes contra observaciones comunes.

### Representaciones y optimización

Experimentos como **E-graph Malbolge IR** exploran transformaciones y equivalencias operacionales sin asumir que una reescritura conserva semántica hasta comprobarlo.

### Integridad de fitness

**Proxy-Fitness Reward Integrity Audit** estudia cuándo una métrica intermedia puede separarse del objetivo real y cómo detectar esos atajos.

---

## Arquitectura del repositorio

```text
EXPERIMENTOSBÖLGE/
├── README.md
├── GUIA_GENERAL.md
├── raw_composes_docx/
│   ├── Malbolge Next Experiments/
│   └── Malbolge Research Shortlists/
├── experiments/
│   ├── Malbolge Next Experiments/
│   └── Malbolge Research Shortlists/
└── workspace/
    └── assembly/
        └── malbolge/
```

## Contrato de artefactos

Cuando aplica, cada experimento conserva:

1. `COMPOSE_PROVENANCE.md`: fuente, hash, contexto e hipótesis.
2. Runner `.py`: ejecución y generación de `results.json`.
3. `test_*.py`: pruebas automatizadas, controles y casos límite.
4. `REPORT.md`: resultados, comparaciones y límites.
5. `GUIA.md`: reproducción paso a paso.
6. `hashes.json`: manifiesto SHA-256 de integridad.

Los veredictos deben leerse dentro del alcance concreto de cada experimento. Un test verde valida ese test; no convierte por sí solo un resultado local en una afirmación universal.

---

## Catálogo

### Malbolge Next Experiments

| Fecha | N° | Título del experimento | Núcleo / aporte | Tests | Estado |
|---|---:|---|---|---:|---|
| **2026-09-18** | 01 | **Len-10 Frontier Pruning** | Poda heurística del espacio de búsqueda para programas longitud 10 | 4/4 | `DEMONSTRATED` |
| **2026-09-18** | 02 | **Dual-Cell Quine Kernel** | Núcleo de quine auto-replicante en dos celdas activas de memoria | 3/3 | `DEMONSTRATED` |
| **2026-09-18** | 03 | **Solver Optimizer Ablation** | Ablación controlada de optimizadores relacionales en grafos Malbolge | 3/3 | `DEMONSTRATED` |
| **2026-09-25** | 01 | **Len-11 Pruning Shard** | Fragmentación sharded para búsqueda en frontera de longitud 11 | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 02 | **Dual-Cell Quine Kernel v2** | Invariante de coherencia memoria-código en quines bi-celulares | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 03 | **Relational Solver Ablation** | Poda de restricciones relacionales en espacios de estados ternarios | 4/4 | `DEMONSTRATED` |
| **2026-10-03** | 01 | **Len-11 Semantic Pruning Shard** | Poda semántica de caminos muertos en la frontera L11 | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 09 | **Semantic Epoch Frontier Bridge** | Puente generacional de épocas de búsqueda con memoria compartida | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 10 | **Dual-Cell Tracer Discriminator** | Discriminador de trazas bi-celulares para detección temprana de ciclos | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 11 | **Solver Optimizer Controlled Ablation** | Ablación estricta de componentes de fitness y heurísticas | 2/2 | `DEMONSTRATED` |

### Malbolge Research Shortlists

| Fecha | N° | Título del experimento | Núcleo / aporte | Tests | Estado |
|---|---:|---|---|---:|---|
| **2026-09-25** | 01 | **Oracle-Preserving Guided Proposals** | Propuestas guiadas que preservan invariantes del oráculo externo | 3/3 | `DEMONSTRATED` |
| **2026-09-25** | 02 | **Prior-Guided Bounded Search** | Búsqueda acotada con conocimiento previo de distribución de opcodes | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 03 | **Mine Reusable Malbolge Trace Motifs** | Minería de patrones reutilizables en trazas de ejecución | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 04 | **Cross-Language External Oracle** | Benchmark comparativo contra oráculos en C, Rust y Python | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 05 | **Neural Branch & Size Guidance** | Guía de ramificación y límite de tamaño | 2/2 | `DEMONSTRATED` |
| **2026-10-02** | 01 | **Abstract-Interpretation A-star Search** | Búsqueda A* guiada por dominios abstractos sobre la VM | 5/5 | `DEMONSTRATED` |
| **2026-10-02** | 02 | **Symbolic Family Search** | Búsqueda simbólica de familias de instrucciones equivalentes | 3/3 | `DEMONSTRATED` |
| **2026-10-02** | 04 | **Optimistic Cyclic Analysis** | Análisis y falsación de supuestos optimistas sobre ciclos | 3/3 | `DEMONSTRATED` |
| **2026-10-02** | 05 | **E-graph Malbolge IR** | Representación intermedia en E-graphs para reescritura de programas | 1/1 | `DEMONSTRATED` |
| **2026-10-09** | 01 | **Classic Malbolge Finite-State Semantics** | Auditoría de estados finitos según la especificación clásica | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 02 | **XOR-2048 Reproduction Fixture** | Reproducción y fijación de restricciones sobre la tabla de crazy-op | 5/5 | `DEMONSTRATED` |
| **2026-10-09** | 03 | **Quine Predicate and Source Identity** | Predicados formales de identidad fuente para quines | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 04 | **Output-Byte Equivalence Slicing** | Slicing de código según bytes de salida emitidos | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 05 | **Trace-Preserving Transformations** | Transformaciones de código con comprobación de preservación de traza | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 06 | **Offline Presynthesis Oracle** | Precálculo de caminos para acelerar síntesis | 2/2 | `DEMONSTRATED` |
| **2026-10-09** | 07 | **Observable VM Conformance Matrix** | Matriz de conformidad observacional entre implementaciones | 2/2 | `DEMONSTRATED` |
| **2026-10-09** | 08 | **Proxy-Fitness Reward Integrity** | Auditoría de integridad de funciones de fitness | 2/2 | `DEMONSTRATED` |

---

## Ejecución

### Suite completa

Desde la raíz del repositorio:

```bash
pytest -v
```

El total de tests puede crecer conforme se incorporen nuevas tandas. El número vigente debe tomarse de la ejecución real de la suite.

### Experimento individual

```bash
python3 "experiments/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/egraph_audit.py"
```

```bash
python3 "experiments/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/dual_cell_synthesis.py"
```

---

## Protocolo para nuevas tandas

1. Preservar el documento fuente y su SHA-256 cuando corresponda.
2. Crear la carpeta del experimento bajo la serie y fecha correctas.
3. Escribir la hipótesis y sus condiciones de rechazo.
4. Implementar el runner y resultados estructurados.
5. Añadir pruebas, controles y casos negativos.
6. Generar reporte, guía y hashes.
7. Actualizar este catálogo sólo después de reproducir la evidencia.

---

## Ecosistema relacionado

Los experimentos pueden reutilizarse desde runtimes, compiladores, analizadores y solvers del ecosistema Malbolge de ISyCo, entre ellos:

- `Cobolge`, `Fortranbolge`, `Pibolge`, `Rustbolge`, `Swiftbolge`, `Walbolge`;
- `MalboGost`, `MALDOOM`, `meowbolge`;
- `malbolge-opera-solver`, `malbolge-oracle`.

La relación entre repositorios es de reutilización técnica; cada experimento conserva su propio alcance, evidencia y provenance.
