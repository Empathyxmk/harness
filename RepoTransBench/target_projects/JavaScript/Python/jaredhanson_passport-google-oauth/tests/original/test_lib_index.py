import builtins
import pytest

def test_google_oauth_package_missing(monkeypatch):
    orig_import = builtins.__import__

    def import_side_effect(name, *args, **kwargs):
        if name in ("passport_google_oauth1", "passport-google-oauth1"):
            raise ImportError("Cannot find passport-google-oauth1")
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_side_effect)
    try:
        import importlib
        with pytest.raises(ImportError):
            importlib.import_module("lib.index")
    finally:
        monkeypatch.setattr(builtins, "__import__", orig_import)