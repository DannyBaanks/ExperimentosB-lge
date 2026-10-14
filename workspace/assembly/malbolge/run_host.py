import subprocess, sys
from pathlib import Path
CMD = ['python', 'bootstrap_runtime.py']
proc = subprocess.run(CMD, stdin=sys.stdin.buffer, capture_output=True, cwd=str(Path(__file__).resolve().parent))
sys.stdout.buffer.write(proc.stdout)
sys.stderr.buffer.write(proc.stderr)
sys.exit(proc.returncode)
