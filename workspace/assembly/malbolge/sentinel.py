ALLOWED_OPS = {
    "bootstrap.find_root",
    "bootstrap.load_manifest",
    "bootstrap.init_transport",
    "bootstrap.execute",
    "registry.discover",
    "registry.register",
    "capability.execute",
}


def allowed(op: str) -> bool:
    return op in ALLOWED_OPS
