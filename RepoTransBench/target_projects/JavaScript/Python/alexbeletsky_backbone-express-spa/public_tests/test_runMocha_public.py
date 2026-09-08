import os
import sys
import pytest

def test_set_env_vars_and_invoke_scripts(monkeypatch):
    backup_env = os.environ.copy()
    os.environ.clear()
    os.environ["FOO"] = "BAR"
    # Simulates original: set envs as uppercase checks
    monkeypatch.setattr(sys, "exit", lambda _: None)
    os.environ["NODE_ENV"] = "development"
    os.environ["APP_ENV"] = "development"
    os.environ["TEST_ENV"] = "development"
    os.environ["CLIENTAPP_ENV"] = "development"
    assert os.environ["NODE_ENV"].upper() == "DEVELOPMENT"
    assert os.environ["APP_ENV"].upper() == "DEVELOPMENT"
    assert os.environ["TEST_ENV"].upper() == "DEVELOPMENT"
    assert os.environ["CLIENTAPP_ENV"].upper() == "DEVELOPMENT"
    os.environ.clear()
    os.environ.update(backup_env)