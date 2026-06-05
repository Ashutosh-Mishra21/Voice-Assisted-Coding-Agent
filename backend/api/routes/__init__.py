"""
Package exports.

Export only stable public interfaces.

DO:

* Models
* Base classes
* Factories
* Public APIs

DO NOT EXPORT:

* Heavy implementations
* Runtime services
* Executors
* Internal utilities
* Cross-package dependencies that may create import cycles

When unsure, keep imports local and avoid re-exporting.
"""

from importlib import import_module

_EXPORTS = {
    "agent_router": (".agent", "router"),
    "health_router": (".health", "router"),
}

__all__ = [
    "agent_router",
    "health_router",
]


def __getattr__(name: str):
    if name in _EXPORTS:
        module_name, symbol_name = _EXPORTS[name]
        module = import_module(module_name, __name__)
        value = getattr(module, symbol_name)
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
