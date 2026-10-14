#!/usr/bin/env python3
"""
Unit and integration tests for E-graph Malbolge IR Audit.
"""

import os
import json
import pytest
from pathlib import Path

from egraph_malbolge_ir_audit import (
    audit_source_docx,
    run_experiment,
)

def test_source_docx_properties():
    docx_rel = Path("OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/05 — Compose — E-graph Malbolge IR.docx")
    assert docx_rel.exists()
    audit = audit_source_docx(docx_rel)
    assert audit["file_size"] == 6485
    assert audit["sha256"] == "605f36aa07604a6a4e589cb8c21cea1a179caf0b888fb6f2da5a0de9a227512e"
    assert audit["is_blank_template"] is True
    assert audit["paragraph_count"] == 0
    assert audit["table_count"] == 0

def test_audit_experiment_run():
    report = run_experiment()
    assert report["verdict"] == "AUDIT_RECORDED_BLANK_ANOMALY"
    assert report["gates"]["source_file_exists"] is True
    assert report["gates"]["sha256_verified"] is True
    assert report["gates"]["blank_anomaly_proven"] is True
    assert report["gates"]["zero_deletion_enforced"] is True
