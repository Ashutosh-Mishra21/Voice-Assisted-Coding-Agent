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

# Keep the top-level backend package free of imports so importing ``backend``
# never starts API setup, settings loading, indexing, or parser dependencies.
__all__: list[str] = []
