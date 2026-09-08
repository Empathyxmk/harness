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

def test_config_value_for_key_finds_existing_key():
    pairs = [FakeOutPair("foo", "bar"), FakeOutPair("baz", "qux")]
    assert utils.config_value_for_key(pairs, "foo") == "bar"
    assert utils.config_value_for_key(pairs, "baz") == "qux"

def test_config_value_for_key_returns_empty_for_missing_key():
    pairs = [FakeOutPair("foo", "bar")]
    assert utils.config_value_for_key(pairs, "notfound") == ""

def test_config_value_for_key_empty_list():
    assert utils.config_value_for_key([], "foo") == ""

def test_config_value_for_key_multiple_same_keys_returns_first():
    pairs = [
        FakeOutPair("foo", "first"),
        FakeOutPair("foo", "second"),
        FakeOutPair("bar", "other"),
    ]
    assert utils.config_value_for_key(pairs, "foo") == "first"

def test_invalid_config_message_makes_correct_string():
    msg = utils.invalid_config_message("value", "key", "file")
    assert msg == '"value" is not a valid value for key for file file'

def test_applied_config_message_makes_correct_string():
    msg = utils.applied_config_message("value", "key", "file")
    assert msg == 'Applied "value" as key for file file'