import pytest

class TwigStructureItem:
    def __init__(self, name, kind, offset, end_offset):
        self._name = name
        self._kind = kind
        self._offset = offset
        self._end_offset = end_offset
    def getName(self):
        return self._name
    def getKind(self):
        return self._kind
    def getOffset(self):
        return self._offset
    def getEndOffset(self):
        return self._end_offset

def test_constructor_different_name_public():
    item = TwigStructureItem("otherPublicName", "block", 7, 12)
    assert item.getName() == "otherPublicName"
    assert item.getKind() == "block"
    assert item.getOffset() == 7
    assert item.getEndOffset() == 12