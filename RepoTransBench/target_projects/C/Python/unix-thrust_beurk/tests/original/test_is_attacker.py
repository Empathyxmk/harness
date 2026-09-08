import pytest

# --- Stubs and Test Globals/Macros --- #
init_call_count = 0
getenv_call_count = 0
mock_env_val = None

def init():
    global init_call_count
    init_call_count += 1

def getenv(s):
    global getenv_call_count, mock_env_val
    getenv_call_count += 1
    if mock_env_val and s == "BEURK_ATK_ENV":
        return mock_env_val
    return None

# Code-under-test: Simulated, replicating key logic for is_attacker
def is_attacker():
    init()
    if not hasattr(is_attacker, "_attacker"):
        is_attacker._attacker = -1
    if is_attacker._attacker != -1:
        return is_attacker._attacker
    if getenv("BEURK_ATK_ENV"):
        is_attacker._attacker = 1
    else:
        is_attacker._attacker = 0
    return is_attacker._attacker

def test_attacker_path():
    # Reset static & globals
    global mock_env_val
    mock_env_val = "dummy"
    if hasattr(is_attacker, "_attacker"):
        del is_attacker._attacker
    ret = is_attacker()
    assert ret == 1
    ret = is_attacker() # should use static value
    assert ret == 1

def test_non_attacker_path():
    global mock_env_val
    mock_env_val = None
    if hasattr(is_attacker, "_attacker"):
        del is_attacker._attacker
    ret = is_attacker()
    assert ret == 0
    ret = is_attacker() # should use static value
    assert ret == 0