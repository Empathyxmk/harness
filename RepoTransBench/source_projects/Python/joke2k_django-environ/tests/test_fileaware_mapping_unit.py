import os
import tempfile
import shutil
import pytest

from environ import fileaware_mapping


def test_fileawaremapping_basic_get_set(monkeypatch):
    # Prepare a fake environment
    test_env = {}
    fam = fileaware_mapping.FileAwareMapping(test_env, cache=True)
    fam["A"] = "123"
    assert fam["A"] == "123"
    # Underlying env modified
    assert test_env["A"] == "123"
    fam["B"] = "xyz"
    assert fam["B"] == "xyz"

    # Now test deleting a key directly present
    del fam["B"]
    assert "B" not in test_env


def test_fileawaremapping_file_key(tmp_path):
    # Write file to temp dir
    f = tmp_path / "testenv"
    value = "value_from_file"
    f.write_text(value)
    test_env = {"VAR_FILE": str(f)}
    fam = fileaware_mapping.FileAwareMapping(test_env)
    assert fam["VAR"] == value
    # After first access and with cache, result should be cached
    assert fam.files_cache["VAR"] == value

    # If we remove file from env and use cache off, KeyError
    fam2 = fileaware_mapping.FileAwareMapping(test_env, cache=False)
    assert fam2["VAR"] == value

def test_fileawaremapping_iter_len(tmp_path):
    test_env = {
        "A": "x",
        "B_FILE": "ignore",
        "C_FILE": "ignore"
    }
    fam = fileaware_mapping.FileAwareMapping(test_env)
    keys = set(fam)
    # B_FILE, C_FILE, plus B, C (shortened)
    assert "A" in keys and "B_FILE" in keys and "B" in keys and "C_FILE" in keys and "C" in keys
    l = len(fam)
    assert l == len(keys)

def test_fileawaremapping_setitem_cache(tmp_path):
    # Test that cache is cleared when setting a _FILE key
    test_env = {"FOO_FILE": "somefile"}
    fam = fileaware_mapping.FileAwareMapping(test_env, cache=True)
    fam.files_cache["FOO"] = "should_be_deleted"
    fam["FOO_FILE"] = "newfile"
    assert "FOO" not in fam.files_cache

def test_fileawaremapping_delitem_special(tmp_path):
    # Deleting a key that has _FILE present in env, removes both
    test_env = {"HELLO_FILE": "abc", "HELLO": "world"}
    fam = fileaware_mapping.FileAwareMapping(test_env, cache=True)
    del fam["HELLO"]
    assert "HELLO_FILE" not in test_env
    assert "HELLO" not in test_env

def test_fileawaremapping_delitem_cache(tmp_path):
    # When cache=True and deleting a _FILE key, file cache is also updated
    test_env = {"BAR_FILE": "abc"}
    fam = fileaware_mapping.FileAwareMapping(test_env, cache=True)
    fam.files_cache["BAR"] = "to_be_removed"
    del fam["BAR_FILE"]
    assert "BAR" not in fam.files_cache

def test_fileawaremapping_keyerror(tmp_path):
    # When key is not present, KeyError
    test_env = {}
    fam = fileaware_mapping.FileAwareMapping(test_env)
    with pytest.raises(KeyError):
        _ = fam["XXX"]