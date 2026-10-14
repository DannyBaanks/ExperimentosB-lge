import pytest
from pathlib import Path
from semantic_epoch_bridge import (
    EpochVM,
    generate_tree_shard,
    evaluate_baseline,
    evaluate_with_pruning,
)

BASE_DIR = Path(__file__).resolve().parent
HELLO_FILE = Path("workspace/assembly/malbolge/hello_world.malbolge").resolve()

def test_epoch_semantic_divergence_on_underflow():
    # Program consisting solely of '/' (input) followed by '<' (output) and 'v' (halt)
    # Under current epoch, EOF returns 59048. Under historical epoch, EOF returns 0.
    code = bytearray([68] * 10)
    # Set first char to '/' (char 47)
    for ch in range(33, 127):
        if "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"[(ch - 33 + 0) % 94] == '/':
            code[0] = ch
            break
    # Set second char to 'v' (halt)
    for ch in range(33, 127):
        if "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"[(ch - 33 + 1) % 94] == 'v':
            code[1] = ch
            break

    vm_hist = EpochVM(bytes(code), epoch="historical")
    res_hist = vm_hist.run(max_steps=50)

    vm_curr = EpochVM(bytes(code), epoch="current")
    res_curr = vm_curr.run(max_steps=50)

    assert res_hist["final_a"] == 0
    assert res_curr["final_a"] == 59048

def test_shard_generation_and_positive_controls():
    shard = generate_tree_shard(seed=42, num_prefixes=3, branching=5)
    assert len(shard) == 3 * 5 + 2  # 15 shard candidates + 2 positive controls
    pos = [c for c in shard if c["is_positive_control"]]
    assert len(pos) == 2
    assert any(c["id"] == "positive_control_hello" for c in pos)

def test_pruning_soundness_zero_false_negatives():
    shard = generate_tree_shard(seed=42, num_prefixes=5, branching=10)
    base_res = evaluate_baseline(shard, epoch="current", max_steps=200)
    prune_res = evaluate_with_pruning(shard, epoch="current", max_steps=200)

    # Positive hits must be identical!
    assert base_res["hit_count"] == prune_res["hit_count"]
    assert set(base_res["hits"]) == set(prune_res["hits"])
    assert prune_res["hit_count"] > 0

def test_falsification_pruner_savings():
    shard = generate_tree_shard(seed=42, num_prefixes=5, branching=10)
    base_res = evaluate_baseline(shard, epoch="current", max_steps=200)
    prune_res = evaluate_with_pruning(shard, epoch="current", max_steps=200)

    # Step count with pruning must be strictly <= baseline steps
    assert prune_res["total_steps"] <= base_res["total_steps"]
