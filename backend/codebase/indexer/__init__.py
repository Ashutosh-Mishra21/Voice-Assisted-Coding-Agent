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

# RepositoryScanner and ChunkBuilder are internal implementation collaborators.
__all__ = [
    "RepositoryIndexer",
]


def __getattr__(name: str):
    if name == "RepositoryIndexer":
        module = import_module(".repository_indexer", __name__)
        value = module.RepositoryIndexer
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
