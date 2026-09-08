import pytest
import sys

import pyicloud.utils as utils
from pyicloud.exceptions import PyiCloudNoStoredPasswordAvailableException

class DummyKeyring:
    def __init__(self):
        self.saved = {}
        self.deleted = []
    def get_password(self, system, username):
        return self.saved.get(username, None)
    def set_password(self, system, username, password):
        self.saved[username] = password
        return "set"
    def delete_password(self, system, username):
        self.deleted.append(username)
        return "del"

@pytest.fixture(autouse=True)
def patch_keyring(monkeypatch):
    dkr = DummyKeyring()
    monkeypatch.setattr(utils, "keyring", dkr)
    return dkr

def test_get_password_from_keyring_success(patch_keyring):
    patch_keyring.saved["foo"] = "bar"
    assert utils.get_password_from_keyring("foo") == "bar"

def test_get_password_from_keyring_failure(patch_keyring):
    with pytest.raises(PyiCloudNoStoredPasswordAvailableException):
        utils.get_password_from_keyring("not-exist")

def test_password_exists_in_keyring_true(patch_keyring):
    patch_keyring.saved["a"] = "b"
    assert utils.password_exists_in_keyring("a") is True

def test_password_exists_in_keyring_false(patch_keyring):
    assert utils.password_exists_in_keyring("none") is False

def test_store_password_in_keyring(patch_keyring):
    out = utils.store_password_in_keyring("x", "y")
    assert patch_keyring.saved["x"] == "y"
    assert out == "set"

def test_delete_password_in_keyring(patch_keyring):
    patch_keyring.saved["delme"] = "foo"
    out = utils.delete_password_in_keyring("delme")
    assert "delme" in patch_keyring.deleted
    assert out == "del"

def test_underscore_to_camelcase_basic():
    assert utils.underscore_to_camelcase("hello_world") == "helloWorld"
    assert utils.underscore_to_camelcase("A_b", initial_capital=True) == "AB"

def test_get_password_interactive_false(monkeypatch):
    # disables interactive mode, keyring throws
    monkeypatch.setattr(utils, "get_password_from_keyring", lambda _u: (_ for _ in ()).throw(PyiCloudNoStoredPasswordAvailableException()))
    with pytest.raises(PyiCloudNoStoredPasswordAvailableException):
        utils.get_password("z", interactive=False)

def test_get_password_interactive_true(monkeypatch):
    monkeypatch.setattr(utils, "get_password_from_keyring", lambda _u: (_ for _ in ()).throw(PyiCloudNoStoredPasswordAvailableException()))
    monkeypatch.setattr(utils.getpass, "getpass", lambda prompt: "foo")
    out = utils.get_password("z", interactive=True)
    assert out == "foo"