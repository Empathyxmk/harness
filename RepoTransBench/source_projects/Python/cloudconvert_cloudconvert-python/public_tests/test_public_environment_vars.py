import os
import importlib

def test_environment_import_public(monkeypatch):
    # Set new env var and reload
    monkeypatch.setenv("SOME_PUBLIC_API_KEY", "keypublic123")
    # Remove any existing cached import
    import sys
    sys.modules.pop('cloudconvert.environment_vars', None)
    import cloudconvert.environment_vars as env_mod
    assert hasattr(env_mod, "os")
    # The presence of variable doesn't cause import error

def test_env_var_not_set_public(monkeypatch):
    # Unset possible env variable
    monkeypatch.delenv("API_KEY", raising=False)
    import importlib
    import cloudconvert.environment_vars as env_mod
    assert env_mod is not None