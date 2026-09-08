try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

# Export submodule access for usage in tests (and for general API consistency)
# Insert export attribute for patching and testability, but do it safely.
try:
    import importlib
    export = importlib.import_module("honcho.export")
except Exception:
    pass