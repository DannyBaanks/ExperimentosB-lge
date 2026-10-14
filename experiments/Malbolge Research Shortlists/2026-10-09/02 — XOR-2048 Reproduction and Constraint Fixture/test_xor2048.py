import pytest
import hashlib
from pathlib import Path
from reproduce_xor2048 import (
    PythonClassicVM,
    verify_loader_legality,
    extract_constraint_fixture,
    crazy_op,
)

BASE_DIR = Path(__file__).resolve().parent
MAL_FILE = BASE_DIR / "gpt-6-astra.mal"

def test_artifact_integrity_and_provenance():
    assert MAL_FILE.exists(), "gpt-6-astra.mal must exist"
    code = MAL_FILE.read_bytes()
    assert len(code) == 2028, f"Expected 2028 bytes, got {len(code)}"
    sha256 = hashlib.sha256(code).hexdigest()
    assert sha256 == "cb28ec05a4d9d8780273ed79eb49a6be4b9fcd7427e68578e5758f860a4a4015"

def test_loader_legality():
    code = MAL_FILE.read_bytes()
    res = verify_loader_legality(code)
    assert res["valid"] is True
    assert res["error_count"] == 0

def test_falsification_loader_corruption():
    code = bytearray(MAL_FILE.read_bytes())
    # Corrupt one byte with an illegal opcode character (e.g., '@' or unprintable)
    code[50] = 32  # space inside dense block (unprintable/disallowed in classic source array)
    res = verify_loader_legality(bytes(code))
    assert res["valid"] is False
    assert res["error_count"] > 0

def test_constraint_fixture_structure():
    code = MAL_FILE.read_bytes()
    fixture = extract_constraint_fixture(code)
    assert fixture["table_offset"] == 124
    assert fixture["table_len"] == 772
    assert fixture["target_xor_constant"] == 0x51
    assert fixture["masks"] == [3, 20, 21, 18, 19, 24, 16, 7]
    assert fixture["passes"] == 8
    assert fixture["mutable_cells_per_pass"] == 5

def test_pyvm_boundary_cases():
    code = MAL_FILE.read_bytes()
    vm = PythonClassicVM(code)
    for inp in [0, 1, 81, 128, 255]:
        res = vm.run(inp)
        assert res["halted"] is True
        assert res["steps"] == 1148
        assert res["out_count"] == 1
        assert res["out_byte"] == (inp ^ 0x51)

def test_falsification_wrong_oracle():
    code = MAL_FILE.read_bytes()
    vm = PythonClassicVM(code)
    res = vm.run(42)
    # Correct is 42 ^ 0x51 = 83. An invalid claim (e.g., 42 ^ 0x50 = 82) must fail.
    assert res["out_byte"] != (42 ^ 0x50)
    assert res["out_byte"] == (42 ^ 0x51)
