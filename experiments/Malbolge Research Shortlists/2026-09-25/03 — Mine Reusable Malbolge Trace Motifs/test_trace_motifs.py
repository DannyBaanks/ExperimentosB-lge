#!/usr/bin/env python3
"""
Unit and integration tests for Mine Reusable Malbolge Trace Motifs.
"""

import os
import json
import pytest
from pathlib import Path

from mine_trace_motifs import (
    crazy,
    ConcreteVM,
    TraceMotifMiner,
    search_scratch,
    search_with_motif,
    run_experiment,
)

def test_trace_motif_miner():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    motifs = TraceMotifMiner.mine_motifs_from_traces(alphabet, length=2)
    assert len(motifs) > 0
    top_m, freq = motifs[0]
    assert len(top_m) == 2
    assert freq > 0

def test_motif_search_soundness():
    alphabet = ["(", "=", "<", "`", ":", "9"]
    hit, evals = search_with_motif(alphabet, "(=", target_byte=57, suffix_len=2)
    assert hit == "(=<`"
    vm = ConcreteVM(hit)
    out = vm.run(25)
    assert len(out) > 0 and out[0] == 57

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["held_out_evaluations_reduced"] is True
    assert report["gates"]["canonical_replay_verified"] is True
    assert report["gates"]["non_empty_motif_library"] is True
    assert len(report["held_out_benchmarks"]) == 2
    for b in report["held_out_benchmarks"]:
        assert b["evaluation_reduction_ratio"] > 0.5
