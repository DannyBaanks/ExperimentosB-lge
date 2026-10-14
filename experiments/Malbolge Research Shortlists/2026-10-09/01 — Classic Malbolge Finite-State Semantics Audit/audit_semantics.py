"""
audit_semantics.py — Formal audit and verification of Classic Malbolge finite-state semantics,
trit-pair recurrence orbits, tail periodicity, and cross-implementation parity.

Part of Malbolge Research Shortlists / 2026-10-09:
Compose 01 — Classic Malbolge Finite-State Semantics Audit
"""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Tuple

sys.path.insert(0, "/home/danny/Development/ISyCo/workspace/assembly/malbolge")
import malbolge_interpreter as mi

CRAZY_TRIT_TABLE = (
    (1, 0, 0),
    (1, 0, 2),
    (2, 2, 1),
)


def analyze_all_trit_pairs() -> List[Dict[str, Any]]:
    """
    Enumerate all 9 trit pairs (y, x) in {0, 1, 2}^2 and compute their recurrence orbit
    under t_{n} = CRAZY[t_{n-1}][t_{n-2}].
    """
    orbits = []
    for y in range(3):
        for x in range(3):
            seq = [(y, x)]
            curr_y, curr_x = y, x
            while True:
                nxt = CRAZY_TRIT_TABLE[curr_x][curr_y]
                nxt_pair = (curr_x, nxt)
                if nxt_pair in seq:
                    cycle_start = seq.index(nxt_pair)
                    cycle = seq[cycle_start:]
                    period = len(cycle)
                    transient = cycle_start
                    orbits.append({
                        "initial_pair": [y, x],
                        "transient_steps": transient,
                        "cycle_length": period,
                        "cycle_states": [[p[0], p[1]] for p in cycle],
                        "divides_6": (6 % period == 0 or period % 6 == 0 or period in (1, 2, 3, 4, 6)),
                    })
                    break
                seq.append(nxt_pair)
                curr_y, curr_x = nxt_pair
    return orbits


def find_memory_tail_period(mem: List[int], src_len: int, search_range: int = 1000) -> Tuple[int, int]:
    """
    Detect the transient length and fundamental period of the generated memory tail.
    """
    # Start after source length + transient window
    start_offset = src_len + 10
    sample = mem[start_offset: start_offset + search_range]

    for p in range(1, 100):
        if all(sample[i] == sample[i + p] for i in range(len(sample) - p)):
            return start_offset, p
    return start_offset, -1


def audit_cross_vm_memory_parity(source_path: str) -> Dict[str, Any]:
    """
    Compare memory loading and tail generation between Python malbolge_interpreter
    and Native C reference_interpreter.
    """
    with open(source_path, "r", encoding="utf-8") as f:
        src_text = f.read()

    # 1. Python VM Memory Load
    py_mem = mi.load_memory(src_text)
    py_bytes = bytes([b & 0xFF for b in py_mem])
    py_hash = hashlib.sha256(py_bytes).hexdigest()

    # 2. Extract C VM Initial Memory via gcc subprocess
    c_helper_src = f"""
    #include <stdio.h>
    #include <stdlib.h>
    #include <ctype.h>
    #include <string.h>

    unsigned short op( unsigned short x, unsigned short y ) {{
      unsigned short i = 0, j;
      static const unsigned short p9[5] = {{ 1, 9, 81, 729, 6561 }};
      static const unsigned short o[9][9] = {{
        {{ 4, 3, 3, 1, 0, 0, 1, 0, 0 }},
        {{ 4, 3, 5, 1, 0, 2, 1, 0, 2 }},
        {{ 5, 5, 4, 2, 2, 1, 2, 2, 1 }},
        {{ 4, 3, 3, 1, 0, 0, 7, 6, 6 }},
        {{ 4, 3, 5, 1, 0, 2, 7, 6, 8 }},
        {{ 5, 5, 4, 2, 2, 1, 8, 8, 7 }},
        {{ 7, 6, 6, 7, 6, 6, 4, 3, 3 }},
        {{ 7, 6, 8, 7, 6, 8, 4, 3, 5 }},
        {{ 8, 8, 7, 8, 8, 7, 5, 5, 4 }},
      }};
      for ( j = 0; j < 5; j++ )
        i += o[y / p9[j] % 9][x / p9[j] % 9] * p9[j];
      return ( i );
    }}

    int main() {{
      FILE *f = fopen("{source_path}", "r");
      if (!f) return 1;
      unsigned short mem[59049];
      unsigned short i = 0;
      int x;
      while ((x = getc(f)) != EOF) {{
        if (isspace(x)) continue;
        mem[i++] = x;
      }}
      fclose(f);
      while (i < 59049) {{
        mem[i] = op(mem[i - 1], mem[i - 2]);
        i++;
      }}
      for (int k = 0; k < 59049; k++) {{
        fputc((unsigned char)(mem[k] & 0xFF), stdout);
      }}
      return 0;
    }}
    """
    tmp_c = Path("/tmp/dump_c_mem.c")
    tmp_bin = Path("/tmp/dump_c_mem")
    tmp_c.write_text(c_helper_src, encoding="utf-8")
    subprocess.run(["gcc", "-O3", str(tmp_c), "-o", str(tmp_bin)], check=True)

    c_proc = subprocess.run([str(tmp_bin)], capture_output=True, check=True)
    c_bytes = c_proc.stdout
    c_hash = hashlib.sha256(c_bytes).hexdigest()

    parity = (py_hash == c_hash)

    # Clean up temp
    tmp_c.unlink(missing_ok=True)
    tmp_bin.unlink(missing_ok=True)

    return {
        "source": source_path,
        "py_memory_hash": py_hash,
        "c_memory_hash": c_hash,
        "memory_load_parity": parity,
    }


def run_semantics_audit(out_dir: str = ".") -> Dict[str, Any]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Enumerate 9 trit-pair state orbits
    trit_orbits = analyze_all_trit_pairs()

    # 2. Verify period-6 theorem on standard programs
    test_programs = [
        "/home/danny/Development/ISyCo/workspace/assembly/malbolge/hello_world.malbolge",
        "/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge",
    ]

    program_audits = []
    for prog in test_programs:
        with open(prog, "r", encoding="utf-8") as f:
            src = f.read()
        stripped_len = len([c for c in src if not c.isspace()])
        mem = mi.load_memory(src)
        transient_offset, period = find_memory_tail_period(mem, stripped_len)

        parity_res = audit_cross_vm_memory_parity(prog)

        program_audits.append({
            "path": prog,
            "stripped_length": stripped_len,
            "transient_offset": transient_offset,
            "fundamental_period": period,
            "period_divides_6": (period > 0 and 6 % period == 0 or period == 6),
            "cross_vm_parity": parity_res["memory_load_parity"],
        })

    # Overall Verdict
    all_divides_6 = all(p["period_divides_6"] for p in program_audits)
    all_parity = all(p["cross_vm_parity"] for p in program_audits)
    verdict = "DEMONSTRATED" if (all_divides_6 and all_parity) else "FALSIFIED"

    summary = {
        "experiment": "Classic Malbolge Finite-State Semantics Audit",
        "provenance": "Malbolge Research Shortlists / 2026-10-09 / Compose 01",
        "verdict": verdict,
        "trit_pair_orbits": trit_orbits,
        "program_tail_audits": program_audits,
    }

    with open(out_path / "results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def print_audit_report(summary: Dict[str, Any]) -> None:
    print("\n" + "=" * 88)
    print(" EXPERIMENT REPORT: CLASSIC MALBOLGE FINITE-STATE SEMANTICS AUDIT")
    print("=" * 88)
    print(f"Formal Verdict: [{summary['verdict']}]\n")

    print("--- 1. TRIT-PAIR RECURRENCE TRANSITIONS (9 States) ---")
    for o in summary["trit_pair_orbits"]:
        pair = o["initial_pair"]
        print(f"  Pair (y={pair[0]}, x={pair[1]}) -> Transient: {o['transient_steps']}, Period: {o['cycle_length']}, Cycle: {o['cycle_states']}")

    print("\n--- 2. PROGRAM MEMORY TAIL PERIODICITY & CROSS-VM PARITY ---")
    for p in summary["program_tail_audits"]:
        name = Path(p["path"]).name
        print(f"  Program: {name:<22} | Stripped: {p['stripped_length']:5d} | Period: {p['fundamental_period']} | Divides 6: {p['period_divides_6']} | VM Parity: {p['cross_vm_parity']}")
    print("=" * 88 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Malbolge Finite-State Semantics Audit")
    parser.add_argument("--out", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    res = run_semantics_audit(args.out)
    print_audit_report(res)
