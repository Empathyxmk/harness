import pytest

# --- Simulated logic for drop_shell_backdoor ---
def drop_shell_backdoor(cmd):
    if cmd is None:
        return -1
    if cmd == "evil":
        return 1
    return 0

def test_drop_null_cmd():
    assert drop_shell_backdoor(None) == -1

def test_drop_evil_cmd():
    assert drop_shell_backdoor("evil") == 1

def test_drop_benign_cmd():
    assert drop_shell_backdoor("benign") == 0