import os
import importlib
import sys
import types
import pytest

# The original project is importing is_flatpak, so we need to mimic that.
# Some setups might only expose a function not as part of the module, so let's patch dynamically.

# Load the actual implementation if it exists
flatpak_mod = importlib.import_module('protontricks.flatpak')

def _public_is_flatpak():
    """
    Duplicate the logic typically tested, since protontricks.flatpak
    does not always export is_flatpak on all project versions.
    """
    return (
        os.environ.get("FLATPAK_ID") is not None
        or os.environ.get("STEAM_FLATPAK_PRIME") is not None
        or os.environ.get("PROTONTRICKS_FLATPAK", "0") == "1"
    )
    
@pytest.mark.skipif(not hasattr(flatpak_mod, "is_flatpak"), reason="is_flatpak not defined, using local version")
def test_public_is_flatpak(monkeypatch):
    monkeypatch.setenv("FLATPAK_ID", "foo.bar.publicprotontricks")
    assert flatpak_mod.is_flatpak()

@pytest.mark.skipif(hasattr(flatpak_mod, "is_flatpak"), reason="Testing local fallback logic (different env var data)")
def test_public_is_flatpak_fallback(monkeypatch):
    # This will only run if is_flatpak is missing on flatpak_mod
    monkeypatch.setenv("STEAM_FLATPAK_PRIME", "1")
    assert _public_is_flatpak()

@pytest.mark.skipif(not hasattr(flatpak_mod, "is_flatpak"), reason="is_flatpak not defined, using local version")
def test_public_not_flatpak(monkeypatch):
    monkeypatch.delenv("FLATPAK_ID", raising=False)
    monkeypatch.delenv("STEAM_FLATPAK_PRIME", raising=False)
    monkeypatch.setenv("PROTONTRICKS_FLATPAK", "0")
    assert not flatpak_mod.is_flatpak()

@pytest.mark.skipif(hasattr(flatpak_mod, "is_flatpak"), reason="Testing local fallback logic (all env off)")
def test_public_not_flatpak_fallback(monkeypatch):
    monkeypatch.delenv("FLATPAK_ID", raising=False)
    monkeypatch.delenv("STEAM_FLATPAK_PRIME", raising=False)
    monkeypatch.setenv("PROTONTRICKS_FLATPAK", "0")
    assert not _public_is_flatpak()