# EXPERIMENTOSBÖLGE 😲

**Base de Datos Semanal de Experimentos de Frontera en Malbolge planteados por GPT / OpenAI Composes**

> *«La computación más retorcida, criptográfica y bella del universo, catalogada, formalizada y verificada con rigor matemático.»*

---

## 🌟 ¿Qué es este Repositorio?

**EXPERIMENTOSBÖLGE** es nuestra **base de datos experimental viviente y semanal** dedicada a la investigación avanzada del lenguaje esotérico **Malbolge**, originada a partir de los briefs y composes de investigación planteados por modelos de frontera de OpenAI (GPT-5, GPT-6 y OpenAI Composes).

Cada semana, los modelos plantean hipótesis audaces sobre computabilidad no determinista, optimización de espacios de búsqueda combinatoria intratables, quines auto-modificables, representaciones intermedias en grafos de equivalencia (E-graphs) y oráculos de síntesis de programas. 

En lugar de dejar estas propuestas en el terreno especulativo, **EXPERIMENTOSBÖLGE** las materializa en **implementaciones de software concretas, reproducibles y verificadas al 100%**, asegurando que cada claim cuente con una suite de pruebas automatizadas y evidencia empírica incontrovertible.

### 😲 ¿Por qué la «Ö» en el nombre?
El nombre lleva la **Ö** con diéresis como un homenaje visual a una **carita impresionada (😲)** ante la naturaleza desconcertante, intratable y fascinante de la máquina virtual de Malbolge:
- Memoria ternaria balanceada (trits).
- Cifrado dinámico de instrucciones tras cada ciclo de reloj (tabla de encriptación).
- Operación no lineal `crazy` ($crz$).
- Punteros que saltan y mutan el propio código fuente en ejecución.

---

## 🛠️ ¿Cómo Apoyarnos en esta Base de Datos para Futuros Experimentos?

Este repositorio fue concebido expresamente como una **cantera técnica y biblioteca de referencia** para todos los proyectos presentes y futuros de Malbolge en el ecosistema de Danny (`~/Development/ISyCo Git/`):

1. **Reutilización de Oráculos y Heurísticas de Poda:**
   - Si estás creando un sintetizador de código o un compilador inverso (ej. en `malbolge-opera-solver`, `Cobolge` o `Swiftbolge`), consulta los experimentos de **Serie 1 (Next Experiments)** para extraer las estrategias de poda de frontera (`Len-10`, `Len-11 Shard`), detección de caminos muertos y discriminadores de ciclos.
2. **Sustrato y Fixtures de Conformidad de la VM:**
   - En `workspace/assembly/malbolge/` dispones del intérprete canónico, scripts de ejecución, y ejemplos dorados (`hello_world.malbolge`, quines 4D).
   - El experimento `07 — Observable VM Conformance Matrix` proporciona un testbed para verificar que cualquier nuevo runtime (en C++, Rust, Swift o Python) cumpla estrictamente con la especificación original de 1998.
3. **Representaciones Intermedias y Optimización de Código:**
   - El experimento `05 — E-graph Malbolge IR` demuestra cómo reescribir y simplificar equivalencias operacionales sin romper la coherencia del cifrado.
4. **Prevención de Reward Hacking:**
   - El experimento `08 — Proxy-Fitness Reward Integrity Audit` documenta los peligros de optimizar métricas intermedias y ofrece funciones de fitness a prueba de atajos tramposos.

---

## 📂 Arquitectura del Repositorio

El repositorio es completamente autónomo y portable (cero dependencias externas rotas):

```
EXPERIMENTOSBÖLGE/
├── README.md                          # Este manifiesto maestro y catálogo explicativo
├── GUIA_GENERAL.md                    # Manual de operaciones y guía de extensión semanal
├── pyproject.toml                     # Configuración estandarizada para pytest
├── raw_composes_docx/                 # Archivos originales .docx de OpenAI con sus hashes SHA-256
│   ├── Malbolge Next Experiments/
│   └── Malbolge Research Shortlists/
├── experiments/
│   ├── Malbolge Next Experiments/     # 10 experimentos de síntesis de quines y poda de fronteras
│   └── Malbolge Research Shortlists/  # 17 experimentos de oráculos, E-graphs, análisis cíclico y VMs
└── workspace/
    └── assembly/
        └── malbolge/                  # Intérprete canónico, quines 4D, hello_world y runtime local
```

### 📋 El Contrato de 6 Artefactos por Experimento
Cada uno de los 27 experimentos implementa estrictamente:
1. `COMPOSE_PROVENANCE.md`: Procedencia criptográfica del documento `.docx` original (hash SHA-256), formulación teórica e hipótesis falsificable.
2. Script ejecutor `.py`: Motor de simulación o búsqueda que produce el archivo `results.json` con veredicto estructurado (`DEMONSTRATED`).
3. Suite de pruebas `test_*.py`: Pruebas automatizadas en `pytest` que validan determinismo e hipótesis.
4. `REPORT.md`: Informe cuantitativo detallado con matrices comparativas y verificación de puertas de seguridad.
5. `GUIA.md`: Manual en español con comandos reales ejecutables y salida verbatim de consola.
6. `hashes.json`: Manifiesto criptográfico SHA-256 de integridad para prevenir cualquier alteración accidental.

---

## 📊 Catálogo Maestro de los 27 Experimentos Canónicos

### 🚀 Serie 1: Malbolge Next Experiments (10 Experimentos — 41 Tests Green)

| Fecha | N° | Título del Experimento | Núcleo Teórico / Aporte | Tests | Estado |
|---|---|---|---|---|---|
| **2026-09-18** | 01 | **Len-10 Frontier Pruning** | Poda heurística del espacio de búsqueda para programas longitud 10 | 4/4 | `DEMONSTRATED` |
| **2026-09-18** | 02 | **Dual-Cell Quine Kernel** | Núcleo de quine auto-replicante en dos celdas activas de memoria | 3/3 | `DEMONSTRATED` |
| **2026-09-18** | 03 | **Solver Optimizer Ablation** | Ablación controlada de optimizadores relacionales en grafos Malbolge | 3/3 | `DEMONSTRATED` |
| **2026-09-25** | 01 | **Len-11 Pruning Shard** | Fragmentación sharded para búsqueda en frontera de longitud 11 | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 02 | **Dual-Cell Quine Kernel v2** | Invariante de coherencia memoria-código en quines bi-celulares | 4/4 | `DEMONSTRATED` |
| **2026-09-25** | 03 | **Relational Solver Ablation** | Poda de restricciones relacionales en espacios de estados ternarios | 4/4 | `DEMONSTRATED` |
| **2026-10-03** | 01 | **Len-11 Semantic Pruning Shard** | Poda semántica de caminos muertos en la frontera L11 | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 09 | **Semantic Epoch Frontier Bridge** | Puente generacional de épocas de búsqueda con memoria compartida | 3/3 | `DEMONSTRATED` |
| **2026-10-09** | 10 | **Dual-Cell Tracer Discriminator** | Discriminador de trazas bi-celulares para detección temprana de ciclos | 4/4 | `DEMONSTRATED` |
| **2026-10-09** | 11 | **Solver Optimizer Controlled Ablation**| Ablación estricta de componentes de fitness y heurísticas | 2/2 | `DEMONSTRATED` |

---

### 🔬 Serie 2: Malbolge Research Shortlists (17 Experimentos — 68 Tests Green)

| Fecha | N° | Título del Experimento | Núcleo Teórico / Aporte | Tests | Estado |
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

## ⚡ Cómo Ejecutar y Validar

### 1. Validación Integral de la Suite
Para correr los 109 tests de la base de datos completa:

```bash
cd "/home/danny/Development/ISyCo Git/EXPERIMENTOSBÖLGE"
pytest -v
```

Salida esperada:
```text
============================= 109 passed in ~29s =============================
```

### 2. Ejecutar un Experimento Individual
Puedes correr directamente cualquier script de experimento para regenerar sus métricas:

```bash
# Ejemplo 1: E-graph Malbolge IR
python3 "experiments/Malbolge Research Shortlists/2026-10-02/05 — E-graph Malbolge IR/egraph_audit.py"

# Ejemplo 2: Dual-Cell Quine Kernel
python3 "experiments/Malbolge Next Experiments/2026-09-18/02 — Dual-Cell Quine Kernel/dual_cell_synthesis.py"
```

---

## 🔄 Protocolo Semanal: Cómo Agregar Nuevos Experimentos de GPT

Cuando recibas un nuevo lote de composes semanales planteados por GPT:
1. **Preserva el documento fuente:** Copia el archivo `.docx` en `raw_composes_docx/<Serie>/<Fecha>/` y calcula su SHA-256.
2. **Crea la carpeta del experimento:** En `experiments/<Serie>/<Fecha>/<Número> — <Nombre>/`.
3. **Implementa los 6 artefactos obligatorios:**
   - Redacta `COMPOSE_PROVENANCE.md` con la hipótesis y el hash del `.docx`.
   - Escribe el runner `.py` generando `results.json`.
   - Desarrolla `test_*.py` y asegúrate de que pase con `pytest`.
   - Genera `REPORT.md` y `GUIA.md`.
   - Calcula `hashes.json` para sellar criptográficamente el experimento.
4. **Actualiza la tabla en este `README.md`** y ejecuta `pytest` para certificar que el total siga 100% verde.

---

## 🤝 Conexión con el Ecosistema de Malbolge de Danny

Este repositorio retroalimenta de forma directa los motores y herramientas del workspace:
- **`Cobolge` / `Fortranbolge` / `Pibolge` / `Rustbolge` / `Swiftbolge` / `Walbolge`**: Compiladores y puentes transpiladores.
- **`MalboGost` / `MALDOOM` / `meowbolge`**: Runtimes interactivos y gráficos sobre la VM.
- **`malbolge-opera-solver` / `malbolge-oracle`**: Motores de búsqueda que aprovechan directamente los oráculos y técnicas de poda probadas aquí.

---

*Base de datos de investigación viva desarrollada por Danny & Antigravity para ISyCo.* 😲✨
