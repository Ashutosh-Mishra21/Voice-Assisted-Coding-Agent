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
    "ParserFactory": (".parser_factory", "ParserFactory"),
    "SymbolExtractor": (".symbol_extractor", "SymbolExtractor"),
}

# PythonParser is kept behind ParserFactory to avoid making parser
# implementation dependencies part of the package API.
__all__ = [
    "ParserFactory",
    "SymbolExtractor",
]


def __getattr__(name: str):
    if name in _EXPORTS:
        module_name, symbol_name = _EXPORTS[name]
        module = import_module(module_name, __name__)
        value = getattr(module, symbol_name)
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
