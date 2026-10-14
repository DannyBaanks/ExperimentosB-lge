#!/usr/bin/env python3
"""
Unit and integration tests for Neural Branch and Size-Bound Guidance.
"""

import os
import json
import pytest
from pathlib import Path

from neural_guidance_search import (
    crazy,
    ConcreteVM,
    NeuralAdvisoryPredictor,
    run_experiment,
)

def test_feature_extraction_and_prediction():
    feats_out = NeuralAdvisoryPredictor.extract_features("((<`")
    assert feats_out["has_terminal_out"] == 1.0
    assert feats_out["active_density"] > 0.0

    score_out = NeuralAdvisoryPredictor.predict_priority("((<`")
    score_nop = NeuralAdvisoryPredictor.predict_priority("9999")
    assert score_out > score_nop

def test_size_bound_estimator():
    predicted_bound = NeuralAdvisoryPredictor.predict_size_bound(114)
    assert predicted_bound == 4

def test_full_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "DEMONSTRATED"
    assert report["gates"]["faster_first_hit_in_priority_mode"] is True
    assert report["gates"]["zero_lost_hits_in_conservative_mode"] is True
    assert report["gates"]["size_bound_prediction_verified"] is True
    assert report["gates"]["explicit_false_negative_accounting"] is True
    assert report["mode_a_conservative_priority"]["solutions_lost"] == 0
    assert report["mode_a_conservative_priority"]["speedup_ratio"] > 1.0
