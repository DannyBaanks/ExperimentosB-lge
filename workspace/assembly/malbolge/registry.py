import json

REGISTRY_JSON = json.dumps(
    {
        "capabilities": ["cap.boot_wizard"],
        "operations": ["registry.discover", "registry.register", "bootstrap.execute", "capability.execute"],
    }
)
