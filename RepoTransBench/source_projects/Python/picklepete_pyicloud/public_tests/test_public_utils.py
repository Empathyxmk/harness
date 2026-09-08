import pytest
import sys

import pyicloud.utils as utils
from pyicloud.exceptions import PyiCloudNoStoredPasswordAvailableException

class PublicDummyKeyring:
    def __init__(self):
        self.saved = {}
        self.deleted = []
    def get_password(self, system, username):
        return self.saved.get(username, None)
    def set_password(self, system, username, password):
        self.saved[username] = password
        return "store"
    def delete_password(self, system, username):
        self.deleted.append(username)
        return "removed"

@pytest.fixture(autouse=True)
def patch_keyring(monkeypatch):
    dkr = PublicDummyKeyring()
    monkeypatch.setattr(utils, "keyring", dkr)
    return dkr

def test_get_password_from_keyring_success(patch_keyring):
    patch_keyring.saved["baz"] = "qux"
    assert utils.get_password_from_keyring("baz") == "qux"

def test_get_password_from_keyring_failure(patch_keyring):
    with pytest.raises(PyiCloudNoStoredPasswordAvailableException):
        utils.get_password_from_keyring("does-not-exist")

def test_password_exists_in_keyring_true(patch_keyring):
    patch_keyring.saved["public_user"] = "public_pw"
    assert utils.password_exists_in_keyring("public_user") is True

def test_password_exists_in_keyring_false(patch_keyring):
    assert utils.password_exists_in_keyring("anonymous") is False

def test_store_password_in_keyring(patch_keyring):
    out = utils.store_password_in_keyring("user2", "passwd2")
    assert patch_keyring.saved["user2"] == "passwd2"
    assert out == "store"

def test_delete_password_in_keyring(patch_keyring):
    patch_keyring.saved["deleteme"] = "secret"
    out = utils.delete_password_in_keyring("deleteme")
    assert "deleteme" in patch_keyring.deleted
    assert out == "removed"

def test_underscore_to_camelcase_basic():
    assert utils.underscore_to_camelcase("foo_bar_baz") == "fooBarBaz"
    assert utils.underscore_to_camelcase("Bar_c", initial_capital=True) == "BarC"

def test_get_password_interactive_false(monkeypatch):
    # disables interactive mode, keyring throws
    monkeypatch.setattr(utils, "get_password_from_keyring", lambda _u: (_ for _ in ()).throw(PyiCloudNoStoredPasswordAvailableException()))
    with pytest.raises(PyiCloudNoStoredPasswordAvailableException):
        utils.get_password("userx", interactive=False)

def test_get_password_interactive_true(monkeypatch):
    monkeypatch.setattr(utils, "get_password_from_keyring", lambda _u: (_ for _ in ()).throw(PyiCloudNoStoredPasswordAvailableException()))
    monkeypatch.setattr(utils.getpass, "getpass", lambda prompt: "public_secret")
    out = utils.get_password("userx", interactive=True)
    assert out == "public_secret"