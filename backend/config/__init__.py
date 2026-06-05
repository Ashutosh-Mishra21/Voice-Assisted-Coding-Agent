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

# Do not re-export paths.py constants here because importing that module creates
# storage directories as a side effect.
__all__ = [
    "Settings",
    "settings",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module(".settings", __name__)
        value = getattr(module, name)
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
