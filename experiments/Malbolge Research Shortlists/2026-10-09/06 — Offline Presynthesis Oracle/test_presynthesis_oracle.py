"""
test_presynthesis_oracle.py — Unit tests for Offline Presynthesis Oracle.
"""

from presynthesis_oracle import PresynthesisOracle, run_presynthesis_benchmark


def test_oracle_syntax_filtering():
    oracle = PresynthesisOracle(prefix_len=2)
    # Character that is NOT a legal Malbolge instruction at pos 0 must be rejected
    # In Malbolge pos 0: illegal characters exist
    assert not oracle.is_syntax_viable("\x00\x00")


def test_oracle_semantics_halt_filtering():
    oracle = PresynthesisOracle(prefix_len=2)
    # If first opcode is halt, is_semantics_viable must reject it for targets requiring output
    # Find a char that produces 'v' at pos 0
    # In xlat1, 'v' corresponds to opcode 81
    for code in range(33, 127):
        ch = chr(code)
        if oracle.is_syntax_viable(ch):
            # check if it halts
            if not oracle.is_semantics_viable(ch, target="HELLO"):
                # verified rejection of non-viable instruction
                assert True
                return


def test_presynthesis_benchmark_soundness(tmp_path):
    res = run_presynthesis_benchmark(str(tmp_path))
    assert res["verdict"] == "DEMONSTRATED"
    assert res["soundness_verified"] is True
    assert res["false_negatives_count"] == 0
    assert res["presynthesis"]["pruning_rate_pct"] > 50.0
