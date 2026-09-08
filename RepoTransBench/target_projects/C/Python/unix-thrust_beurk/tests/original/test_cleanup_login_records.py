import pytest

# --- Simulate the cleanup_login_records.c logic ---
# Not actual logic, but relevant for branch coverage illustration.
def cleanup_login_records(filename):
    if not filename:
        return -1
    if filename.startswith('/'):
        return 1
    return 0

def test_null_filename():
    assert cleanup_login_records(None) == -1

def test_absolute_path():
    assert cleanup_login_records("/var/log/utmp") == 1

def test_rel_path():
    assert cleanup_login_records("utmp") == 0