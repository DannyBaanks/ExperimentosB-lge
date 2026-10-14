"""security_context.py - ExecutionContext inmutable de la peticion."""

from security_authority import Authority

MAX_VARS = 8


class ExecutionContext:
    def __init__(self) -> None:
        self.knowledge_source = "bootstrap"
        self.vars: dict[str, str] = {}
        self.authority = Authority()

    def set(self, key: str, value: str) -> None:
        if len(self.vars) < MAX_VARS:
            self.vars[key] = value

    def get(self, key: str):
        return self.vars.get(key)
