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

# Intentionally do not re-export parser or indexer classes from this parent
# package; RepositoryIndexer depends across codebase subpackages and models.
__all__: list[str] = []
