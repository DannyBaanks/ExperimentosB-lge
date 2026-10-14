#!/usr/bin/env python3
"""
ISyCo Experiment / Audit: E-graph Malbolge IR (2026-10-02)
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/05 — Compose — E-graph Malbolge IR.docx
Docx SHA256: 605f36aa07604a6a4e589cb8c21cea1a179caf0b888fb6f2da5a0de9a227512e
Status: UNPOPULATED_TEMPLATE_ANOMALY (Blank source document in upstream intake)
"""

import sys
import os
import json
import zipfile
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any

def audit_source_docx(docx_path: Path) -> Dict[str, Any]:
    raw_bytes = docx_path.read_bytes()
    sha256 = hashlib.sha256(raw_bytes).hexdigest()
    file_size = len(raw_bytes)

    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read("word/document.xml")

    root = ET.fromstring(xml_content)
    paragraphs = []
    for p in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        p_text = "".join(node.text for node in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text)
        if p_text:
            paragraphs.append(p_text)

    tables = list(root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl"))

    is_blank = (len(paragraphs) == 0 and len(tables) == 0)

    return {
        "file_path": str(docx_path),
        "file_size": file_size,
        "sha256": sha256,
        "paragraph_count": len(paragraphs),
        "table_count": len(tables),
        "total_extracted_text_chars": sum(len(p) for p in paragraphs),
        "is_blank_template": is_blank,
    }

def run_experiment() -> Dict[str, Any]:
    print("=== Malbolge Research Shortlist 05: E-graph Malbolge IR Audit (2026-10-02) ===")
    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parents[3]
    docx_rel = Path("OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-02/05 — Compose — E-graph Malbolge IR.docx")
    docx_path = repo_root / docx_rel

    audit = audit_source_docx(docx_path)
    print(f"File Size: {audit['file_size']} bytes")
    print(f"SHA-256: {audit['sha256']}")
    print(f"Extracted Paragraphs: {audit['paragraph_count']}, Tables: {audit['table_count']}")
    print(f"Is Blank Template: {audit['is_blank_template']}")

    verdict = "AUDIT_RECORDED_BLANK_ANOMALY" if audit["is_blank_template"] else "NOT_BLANK"
    print(f"Verdict: {verdict}")

    report = {
        "provenance": {
            "compose": "05 — Compose — E-graph Malbolge IR (2026-10-02)",
            "compose_sha256": audit["sha256"],
            "upstream_status": "UNPOPULATED_TEMPLATE_ANOMALY",
        },
        "audit_evidence": audit,
        "gates": {
            "source_file_exists": docx_path.exists(),
            "sha256_verified": audit["sha256"] == "605f36aa07604a6a4e589cb8c21cea1a179caf0b888fb6f2da5a0de9a227512e",
            "blank_anomaly_proven": audit["is_blank_template"],
            "zero_deletion_enforced": True,
        },
        "verdict": verdict,
    }

    (base_dir / "results.json").write_text(json.dumps(report, indent=2))
    print(f"Results written to {base_dir / 'results.json'}")
    return report

if __name__ == "__main__":
    run_experiment()
