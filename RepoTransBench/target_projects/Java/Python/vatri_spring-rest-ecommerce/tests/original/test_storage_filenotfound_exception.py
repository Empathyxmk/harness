import pytest

class StorageFileNotFoundException(Exception):
    pass

def test_message_constructor():
    ex = StorageFileNotFoundException("testmsg")
    assert str(ex) == "testmsg"

def test_message_and_cause_constructor():
    cause = Exception("inner")
    try:
        raise StorageFileNotFoundException("outer") from cause
    except StorageFileNotFoundException as ex:
        assert str(ex) == "outer"
        assert ex.__cause__ == cause