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

# Route exports live in backend.api.routes so importing backend.api remains
# lightweight and does not construct routers unnecessarily.
__all__: list[str] = []
