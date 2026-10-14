# EXPERIMENTOSBÖLGE 😲

**Base de Datos Semanal de Experimentos de Frontera en Malbolge planteados por GPT / OpenAI Composes**

> *«La computación más retorcida y bella del universo, catalogada, formalizada y verificada con rigor criptográfico.»*

---

## 🧭 Visión y Propósito

**EXPERIMENTOSBÖLGE** (con la **Ö** de asombro 😲) es el repositorio canónico y la base de datos experimental de todas las propuestas y composes de investigación de frontera en **Malbolge** generados semanalmente por GPT en el ecosistema OpenISy.

Este repositorio consolida **27 experimentos de investigación avanzada** con **109 pruebas unitarias e integradas (100% PASS)**, sirviendo como la biblioteca de conocimiento, fixtures y oráculos para inspirar y fundamentar las próximas generaciones de motores, sintetizadores de quines 4D, podadores de grafos de búsqueda y solucionadores relacionales en Malbolge.

---

## 📂 Arquitectura del Repositorio

```
EXPERIMENTOSBÖLGE/
├── README.md                          # Este manifiesto central y catálogo de experimentos
├── GUIA_GENERAL.md                    # Guía operativa para reproducir y extender experimentos
├── pyproject.toml                     # Configuración de pruebas pytest
├── raw_composes_docx/                 # Documentos originales .docx (procedencia y hashes SHA-256)
│   ├── Malbolge Next Experiments/
│   └── Malbolge Research Shortlists/
├── experiments/
│   ├── Malbolge Next Experiments/     # 10 experimentos de la frontera de síntesis y podado
│   └── Malbolge Research Shortlists/  # 17 experimentos de oráculos, IR, análisis cíclico y VMs
└── workspace/
    └── assembly/
        └── malbolge/                  # Intérprete canónico, quines 4D, hello_world y runtime
```

Cada experimento cuenta con **6 artefactos canónicos obligatorios**:
1. `COMPOSE_PROVENANCE.md`: Procedencia del `.docx` fuente con hash SHA-256 e hipótesis falsificable.
2. Script ejecutor `.py` que genera el artefacto verificable `results.json`.
3. Suite de pruebas unitarias e integradas `test_*.py` (100% passing).
4. `REPORT.md`: Reporte cuantitativo con matrices de métricas, puertas lógicas y veredicto `DEMONSTRATED`.
5. `GUIA.md`: Guía en español con comandos reales y salida verbatim.
6. `hashes.json`: Manifiesto criptográfico de integridad de los artefactos.

---

## 📊 Catálogo de los 27 Experimentos

### 🚀 Serie 1: Malbolge Next Experiments (10 Experimentos)

| Fecha | N° | Título del Experimento | Núcleo Teórico / Aporte | Tests | Veredicto |
|---|---|---|---|---|---|
| **2026-09-18** | 01 | **Len-10 Frontier Pruning** | Poda heurística del espacio de búsqueda para programas longitud 10 | 4/4 | `DEMONSTRATED` |
| **2026-09-18** | 02 | **Dual-Cell Quine Kernel** | Núcleo de quine auto-replicante en dos celdas activas | 3/3 | `DEMONSTRATED` |
| **2026-09-18** | 03 | **Solver Optimizer Ablation** | Ablación controlada de optimizadores relacionales en grafos Malbolge | 3/3 | `DEMONSTRATED` |
| **2026-09-25** | 01 | **Len-11 Pruning Shard** | Fragmentación sharded para búsqueda en frontera de longitud 11 | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 02 | **Dual-Cell Quine Kernel v2** | Invariante de coherencia memoria-código en quines bi-celulares | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 03 | **Relational Solver Ablation** | Poda de restricciones relacionales en espacios de estados ternarios | 4/4 | `DEMONSTRATED` |
| **2026-10-03** | 01 | **Len-11 Semantic Pruning Shard** | Poda semántica de caminos muertos en la frontera L11 | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 09 | **Semantic Epoch Frontier Bridge** | Puente generacional de épocas de búsqueda con memoria compartida | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 10 | **Dual-Cell Tracer Discriminator** | Discriminador de trazas bi-celulares para detección temprana de ciclos | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 11 | **Solver Optimizer Controlled Ablation**| Ablación estricta de componentes de fitness y heurísticas | 2/2 | `DEMONSTRATED` |

---

### 🔬 Serie 2: Malbolge Research Shortlists (17 Experimentos)

| Fecha | N° | Título del Experimento | Núcleo Teórico / Aporte | Tests | Veredicto |
|---|---|---|---|---|---|
| **2026-09-25** | 01 | **Oracle-Preserving Guided Proposals** | Propuestas guiadas que preservan invariantes del oráculo externo | 3/3 | `DEMONSTRATED` |
| **2026-09-25** | 02 | **Prior-Guided Bounded Search** | Búsqueda acotada con conocimiento previo de distribución de opcodes | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 03 | **Mine Reusable Malbolge Trace Motifs** | Minería de patrones y motivos reusables en trazas de ejecución | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 04 | **Cross-Language External Oracle** | Benchmark comparativo contra oráculos en C, Rust y Python | 2/2 | `DEMONSTRATED` |
| **2026-09-25** | 05 | **Neural Branch & Size Guidance** | Red neuronal superficial para guiar la ramificación y límite de tamaño | 2/2 | `DEMONSTRATED` |
| **2026-10-02** | 01 | **Abstract-Interpretation A-star Search**| Búsqueda A* guiada por dominios abstractos sobre la VM | 5/5 | `DEMONSTRATED` |
| **2026-10-02** | 02 | **Symbolic Family Search** | Búsqueda simbólica de familias de instrucciones equivalentes | 3/3 | `DEMONSTRATED` |
| **2026-10-02** | 04 | **Optimistic Cyclic Analysis** | Detección optimista de atractores cíclicos en la memoria de cifrado | 3/3 | `DEMONSTRATED` |
| **2026-10-02** | 05 | **E-graph Malbolge IR** | Representación intermedia en E-graphs para reescritura de programas | 1/1 | `DEMONSTRATED` |
| **2026-10-09** | 01 | **Classic Malbolge Finite-State Semantics** | Auditoría formal de estados finitos según la especificación de Ben Olmstead | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 02 | **XOR-2048 Reproduction Fixture** | Reproducción y fijación de restricciones sobre la tabla de crazy-op | 5/5 | `DEMONSTRATED` |
| **2026-10-09** | 03 | **Quine Predicate and Source Identity** | Predicados formales de identidad fuente para quines certificados | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 04 | **Output-Byte Equivalence Slicing** | Slicing de código según bytes de salida emitidos sin efecto colateral | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 05 | **Trace-Preserving Transformations** | Habilidades de transformación de código que conservan la traza original | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 06 | **Offline Presynthesis Oracle** | Oráculo offline de pre-cálculo de caminos para acelerar síntesis | 2/2 | `DEMONSTRATED` |
| **2026-10-09** | 07 | **Observable VM Conformance Matrix** | Matriz de conformidad observacional de la VM en todas las operaciones | 2/2 | `DEMONSTRATED` |
| **2026-10-09** | 08 | **Proxy-Fitness Reward Integrity** | Auditoría de integridad de recompensas para evitar reward hacking | 2/2 | `DEMONSTRATED` |

---

## ⚡ Cómo Ejecutar las Pruebas

Para validar el 100% de la suite de pruebas (109 tests):

```bash
cd "/home/danny/Development/ISyCo Git/EXPERIMENTOSBÖLGE"
pytest -v
```

Salida esperada:
```
============================= 109 passed in ~28s =============================
```

Para ejecutar un experimento específico (por ejemplo, el oráculo de E-graphs o el Quine Bi-celular):
```bash
python3 "experiments/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/egraph_audit.py"
python3 "experiments/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/dual_cell_synthesis.py"
```

---

## 🤝 Conexión con el Ecosistema de Malbolge de Danny

Este repositorio se conecta de forma natural con los desarrollos del ecosistema en `~/Development/ISyCo Git/`:
- **`Cobolge` / `Fortranbolge` / `Pibolge` / `Rustbolge` / `Swiftbolge` / `Wasmbolge`**: Compiladores y puentes transpiladores.
- **`MalboGost` / `MALDOOM` / `meowbolge`**: Juegos y runtimes gráficos sobre la máquina virtual.
- **`malbolge-opera-solver` / `malbolge-oracle`**: Motores de búsqueda guiada que se nutren directamente de los oráculos y técnicas de poda probadas en **EXPERIMENTOSBÖLGE**.

---

*Desarrollado y consolidado con amor por la informática teórica radical y el esoterismo computacional.* 😲✨
