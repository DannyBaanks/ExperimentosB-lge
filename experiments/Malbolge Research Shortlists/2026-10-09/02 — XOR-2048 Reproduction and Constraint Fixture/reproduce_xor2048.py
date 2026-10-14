#!/usr/bin/env python3
"""
ISyCo Experiment: XOR-2048 Reproduction and Constraint Fixture
Provenance: OPENAI_Composes_2026-10-09/Malbolge Research Shortlists/2026-10-09/02 — Compose — XOR-2048 Reproduction and Constraint Fixture.docx
Docx SHA256: d392f38b1d9560a4a536fa69b31c2d481c90021cbc6cb7e8e7e72a1bdc670b72
Artifact: gpt-6-astra.mal (2,028 bytes)
Artifact SHA256: cb28ec05a4d9d8780273ed79eb49a6be4b9fcd7427e68578e5758f860a4a4015
"""

import sys
import os
import json
import hashlib
import subprocess
import time
from pathlib import Path

XLAT1 = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"
XLAT2 = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@"

CRZ_TABLE = [
    [4, 3, 3, 1, 0, 0, 1, 0, 0],
    [4, 3, 5, 1, 0, 2, 1, 0, 2],
    [5, 5, 4, 2, 2, 1, 2, 2, 1],
    [4, 3, 3, 1, 0, 0, 7, 6, 6],
    [4, 3, 5, 1, 0, 2, 7, 6, 8],
    [5, 5, 4, 2, 2, 1, 8, 8, 7],
    [7, 6, 6, 7, 6, 6, 4, 3, 3],
    [7, 6, 8, 7, 6, 8, 4, 3, 5],
    [8, 8, 7, 8, 8, 7, 5, 5, 4],
]
P9 = [1, 9, 81, 729, 6561]

def crazy_op(x: int, y: int) -> int:
    res = 0
    for j in range(5):
        res += CRZ_TABLE[(y // P9[j]) % 9][(x // P9[j]) % 9] * P9[j]
    return res

class PythonClassicVM:
    def __init__(self, code_bytes: bytes):
        self.raw_code = code_bytes
        self.init_mem = [0] * 59049
        i = 0
        for b in code_bytes:
            if chr(b).isspace():
                continue
            self.init_mem[i] = b
            i += 1
        while i < 59049:
            self.init_mem[i] = crazy_op(self.init_mem[i - 1], self.init_mem[i - 2])
            i += 1

    def run(self, input_byte: int, max_steps: int = 20000):
        mem = list(self.init_mem)
        a = 0
        c = 0
        d = 0
        steps = 0
        output = []
        halted = False

        while steps < max_steps:
            val = mem[c]
            if val < 33 or val > 126:
                c = 0 if c == 59048 else c + 1
                d = 0 if d == 59048 else d + 1
                continue

            steps += 1
            op_char = XLAT1[(val - 33 + c) % 94]
            if op_char == 'j':
                d = mem[d]
            elif op_char == 'i':
                c = mem[d]
            elif op_char == '*':
                a = mem[d] = (mem[d] // 3) + ((mem[d] % 3) * 19683)
            elif op_char == 'p':
                a = mem[d] = crazy_op(a, mem[d])
            elif op_char == '<':
                output.append(a & 0xFF)
            elif op_char == '/':
                a = input_byte
            elif op_char == 'v':
                halted = True
                break

            mem[c] = ord(XLAT2[val - 33])
            c = 0 if c == 59048 else c + 1
            d = 0 if d == 59048 else d + 1

        return {
            "steps": steps,
            "output": output,
            "halted": halted,
            "out_count": len(output),
            "out_byte": output[0] if output else None,
        }

def verify_loader_legality(code: bytes) -> dict:
    errors = []
    if len(code) != 2028:
        errors.append(f"Invalid code length: {len(code)} != 2028")
    for i, b in enumerate(code):
        if b < 33 or b > 126:
            errors.append(f"Non-printable byte {b} at index {i}")
        instr = XLAT1[(b - 33 + i) % 94]
        if instr not in "ji*p</vo":
            errors.append(f"Illegal instruction '{instr}' at index {i}")
    return {
        "valid": len(errors) == 0,
        "byte_count": len(code),
        "error_count": len(errors),
        "errors": errors[:5],
    }

def extract_constraint_fixture(code: bytes) -> dict:
    table_offset = 124
    table_len = 772
    table_bytes = code[table_offset : table_offset + table_len]
    table_hash = hashlib.sha256(table_bytes).hexdigest()
    
    # Oklo documented masks for 8 passes over 5 mutable cells
    masks = [3, 20, 21, 18, 19, 24, 16, 7]
    
    return {
        "table_offset": table_offset,
        "table_len": table_len,
        "table_sha256": table_hash,
        "masks": masks,
        "mutable_cells_per_pass": 5,
        "passes": 8,
        "stride": 3,
        "final_crazy_cells": 2,
        "router_depth": 4,
        "target_xor_constant": 0x51,
    }

def run_experiment():
    base_dir = Path(__file__).resolve().parent
    mal_file = base_dir / "gpt-6-astra.mal"
    code = mal_file.read_bytes()
    code_sha256 = hashlib.sha256(code).hexdigest()

    print(f"=== XOR-2048 Malbolge Reproduction ===")
    print(f"Artifact: {mal_file.name} ({len(code)} bytes, SHA-256: {code_sha256})")

    # 1. Loader legality
    legality = verify_loader_legality(code)
    print(f"Loader legality: {'PASS' if legality['valid'] else 'FAIL'}")
    assert legality['valid'], f"Loader failed: {legality['errors']}"

    # 2. Constraint fixture
    fixture = extract_constraint_fixture(code)
    print(f"Extracted constraint fixture: Table offset={fixture['table_offset']}, len={fixture['table_len']}")

    # 3. C Evaluation (256 cases)
    c_bin = base_dir / "c_evaluator"
    if not c_bin.exists():
        subprocess.run(["gcc", "-O3", str(base_dir / "c_evaluator.c"), "-o", str(c_bin)], check=True)
    t0 = time.perf_counter()
    c_out = subprocess.check_output([str(c_bin), str(mal_file)]).decode()
    t_c = time.perf_counter() - t0
    c_data = json.loads(c_out)

    # 4. Spot-check Python VM on selected domain inputs (boundary and random)
    py_vm = PythonClassicVM(code)
    py_samples = [0, 1, 2, 65, 81, 128, 254, 255]
    py_results = {}
    for inp in py_samples:
        t_py0 = time.perf_counter()
        res = py_vm.run(inp)
        t_py = time.perf_counter() - t_py0
        py_results[inp] = {
            "in": inp,
            "out": res["out_byte"],
            "expected": inp ^ 0x51,
            "match": res["out_byte"] == (inp ^ 0x51),
            "steps": res["steps"],
            "halted": res["halted"],
            "elapsed_s": round(t_py, 4),
        }
        print(f"PyVM in={inp:3d} -> out={res['out_byte']:3d} (expected {inp ^ 0x51:3d}) steps={res['steps']} match={res['out_byte'] == (inp ^ 0x51)}")

    # 5. Full 256 validation from C runner
    matches = 0
    all_steps = set()
    for row in c_data:
        expected = row["in"] ^ 0x51
        if row["out"] == expected and row["halted"] == 1 and row["out_count"] == 1:
            matches += 1
        all_steps.add(row["steps"])

    print(f"C Evaluator: {matches} / 256 perfect matches across all byte inputs")
    print(f"Step count distribution: {all_steps}")
    print(f"C Evaluator elapsed: {t_c:.4f}s ({256/t_c:.1f} cases/s)")

    results = {
        "provenance": {
            "compose": "OPENISY COMPOSE 02 — 2026-10-09 (XOR-2048 Reproduction and Constraint Fixture)",
            "compose_sha256": "d392f38b1d9560a4a536fa69b31c2d481c90021cbc6cb7e8e7e72a1bdc670b72",
            "artifact": "gpt-6-astra.mal",
            "artifact_bytes": len(code),
            "artifact_sha256": code_sha256,
            "upstream_manifest": "manifest.json",
        },
        "legality": legality,
        "constraint_fixture": fixture,
        "oracle_validation": {
            "total_cases": 256,
            "passed_cases": matches,
            "success_rate": matches / 256.0,
            "constant_step_count": list(all_steps)[0] if len(all_steps) == 1 else None,
            "all_step_counts": sorted(list(all_steps)),
            "c_elapsed_seconds": round(t_c, 4),
        },
        "python_spot_check": py_results,
        "verdict": "DEMONSTRATED" if matches == 256 and legality['valid'] and len(all_steps) == 1 and list(all_steps)[0] == 1148 else "NOT_DEMONSTRATED",
    }

    res_path = base_dir / "results.json"
    with open(res_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results written to {res_path}")
    return results

if __name__ == "__main__":
    run_experiment()
