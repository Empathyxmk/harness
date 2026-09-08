import pytest
from easy_thumbnails.alias import aliases

def test_set_and_get_alias_public():
    # Use different alias and size for public test
    aliases.set("gallery_medium", {"size": (320, 240)})
    retrieved = aliases.get("gallery_medium")
    assert retrieved["size"] == (320, 240)

def test_get_nonexistent_alias_returns_none_public():
    assert aliases.get("not_exist_alias_public") is None

def test_reset_public():
    aliases.set("reset_test_public", {"foo": "bar"})
    aliases.reset()
    assert aliases.get("reset_test_public") is None