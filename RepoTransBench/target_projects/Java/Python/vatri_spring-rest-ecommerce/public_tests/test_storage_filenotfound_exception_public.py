import pytest

class StorageFileNotFoundException(Exception):
    pass

def test_message_constructor_public():
    ex = StorageFileNotFoundException("public-message")
    assert str(ex) == "public-message"

def test_message_and_cause_constructor_public():
    cause = Exception("different-inner")
    try:
        raise StorageFileNotFoundException("different-outer") from cause
    except StorageFileNotFoundException as ex:
        assert str(ex) == "different-outer"
        assert ex.__cause__ == cause