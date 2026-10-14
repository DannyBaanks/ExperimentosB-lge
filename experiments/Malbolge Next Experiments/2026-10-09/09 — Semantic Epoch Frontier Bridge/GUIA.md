# GUIA DE OPERACIÓN MANUAL: Puente de Frontera entre Épocas Semánticas

> **Regla de oro:** No extrapoles los negativos de búsqueda de una época semántica histórica a la época actual sin verificar las reglas de divergencia (por ejemplo, el tratamiento de underflow en la lectura de entrada). Utiliza siempre fixtures de control positivo para garantizar que un podador no descarte soluciones válidas.

---

## 1. Propósito
Esta guía permite al operador reproducir el experimento de puente entre épocas semánticas de Malbolge/Autobolge y auditar la poda por prefijo sobre un fragmento determinista (*paired shard*).

---

## 2. Requisitos Previos
- Linux (Ubuntu 24.04 o compatible).
- Python 3.12+ con `pytest`.

---

## 3. Comandos de Ejecución

### A. Ejecutar el Experimento Principal
```bash
python3 "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-09/09 — Semantic Epoch Frontier Bridge/semantic_epoch_bridge.py"
```

**Salida real observada:**
```
=== Semantic Epoch Frontier Bridge Experiment ===
Generated deterministic shard: 202 candidates across 10 prefix families
Historical Epoch: 13549 steps, 1 hits, elapsed=12.742s
Current Epoch Baseline: 13549 steps, 1 hits, elapsed=13.317s
Current Epoch Pruned: 12640 steps, 1 hits, pruned=11, elapsed=10.906s

--- Soundness & Performance Gate ---
Baseline Hits: 1 | Pruned Hits: 1
False Negatives: 0 ([])
False Positives: 0
Pruned Candidates: 11 / 202 (5.4%)
Step Savings: 6.71% (13549 -> 12640)
Time Speedup: 1.22x (15.2/s -> 18.5/s)

Results saved to .../results.json
```

### B. Ejecutar la Suite de Pruebas Automatizadas
```bash
pytest "EXPERIMENTS-COMPOSES-OPENAI/Malbolge Next Experiments/2026-10-09/09 — Semantic Epoch Frontier Bridge/test_epoch_bridge.py" -v
```

**Salida real observada:**
```
test_epoch_semantic_divergence_on_underflow PASSED [ 25%]
test_shard_generation_and_positive_controls PASSED [ 50%]
test_pruning_soundness_zero_false_negatives PASSED [ 75%]
test_falsification_pruner_savings PASSED [100%]
============================== 4 passed in 10.17s ==============================
```

---

## 4. Interpretación de Resultados
1. **`False Negatives: 0`**: El podador no descartó ningún candidato que generara un acierto positivo.
2. **`Pruned Candidates: 11 / 202`**: Un 5.4% de candidatos compartían un tallo de prefijo que no podía alcanzar el objetivo y fueron descartados a coste cero de máquina virtual.
3. **`Time Speedup: 1.22x`**: Se observa una aceleración medible en tiempo real, superando el overhead de inspección de prefijos.

---

## 5. Trampas y Resolución de Problemas
- **Trampa de falsos negativos por prefijo corto:** Si el prefijo analizado es menor a la distancia de un salto indirecto, podar agresivamente puede descartar saltos válidos hacia atrás. El podador solo marca como muerto un prefijo que no realiza saltos externos durante la cuota de combustible inicial.
