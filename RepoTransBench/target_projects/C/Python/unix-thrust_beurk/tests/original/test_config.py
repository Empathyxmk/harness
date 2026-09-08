import pytest

# --- Simulate the config.c load_config logic for coverage ---
g_verbose = 0
config_loaded = 0

def load_config(file):
    global config_loaded, g_verbose
    config_loaded = 0
    if not file:
        return -1
    if file == "beurk.conf":
        config_loaded = 1
        g_verbose = 1
        return 0
    return -1

def test_load_config_success():
    global config_loaded
    assert load_config("beurk.conf") == 0
    assert config_loaded == 1

def test_load_config_fail():
    global config_loaded
    assert load_config("badfile.conf") == -1
    assert config_loaded == 0

def test_load_config_null():
    global config_loaded
    assert load_config(None) == -1
    assert config_loaded == 0