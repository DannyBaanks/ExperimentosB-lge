from pathlib import Path


def find_root() -> str:
    cur = Path.cwd()
    while True:
        if (cur / ".iesyroot").exists():
            return str(cur)
        if cur.parent == cur:
            return ""
        cur = cur.parent
