import pytest

from src.editorconfig import utils

class FakeOutPair(utils.OutPair):
    def __init__(self, key, val):
        self._key = key
        self._val = val

    def get_key(self):
        return self._key

    def get_val(self):
        return self._val

def test_config_value_for_key_finds_different_existing_key():
    pairs = [FakeOutPair("alpha", "beta"), FakeOutPair("gamma", "delta")]
    assert utils.config_value_for_key(pairs, "alpha") == "beta"
    assert utils.config_value_for_key(pairs, "gamma") == "delta"

def test_config_value_for_key_returns_empty_for_another_missing_key():
    pairs = [FakeOutPair("one", "two")]
    assert utils.config_value_for_key(pairs, "absent") == ""

def test_config_value_for_key_empty_list_still_returns_empty():
    assert utils.config_value_for_key([], "doesnotexist") == ""

def test_config_value_for_key_multiple_same_keys_returns_first_public():
    pairs = [
        FakeOutPair("dup", "uno"),
        FakeOutPair("dup", "dos"),
        FakeOutPair("other", "tres")
    ]
    assert utils.config_value_for_key(pairs, "dup") == "uno"

def test_invalid_config_message_makes_correct_string_public():
    msg = utils.invalid_config_message("42", "answer", "deepfile")
    assert msg == '"42" is not a valid value for answer for file deepfile'

def test_applied_config_message_makes_correct_string_public():
    msg = utils.applied_config_message("enabled", "feature", "file.txt")
    assert msg == 'Applied "enabled" as feature for file file.txt'