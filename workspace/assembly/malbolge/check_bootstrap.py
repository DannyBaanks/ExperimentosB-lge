# check_bootstrap.py - "compilador" del esoterico: el programa malbolge real
# debe ejecutarse en el interprete canonical y HALTAR con la firma exacta.
# Si el core malbolge no responde -> COMPILE_FAIL (fail-closed).
import sys
from pathlib import Path

from malbolge_interpreter import run

HERE = Path(__file__).resolve().parent
SIGNATURE = "Hello, world."


def main() -> int:
    src = (HERE / "bootstrap.malbolge").read_text(encoding="ascii")
    text, steps, status = run(src, max_steps=2000000)
    if status != "HALTED":
        print("MALBOLGE_COMPILE_FAIL status=%s steps=%s" % (status, steps))
        return 1
    if text != SIGNATURE:
        print("MALBOLGE_COMPILE_FAIL signature=%r expected=%r" % (text, SIGNATURE))
        return 1
    print("MALBOLGE_COMPILE_OK status=%s steps=%s signature=%r" % (status, steps, text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
