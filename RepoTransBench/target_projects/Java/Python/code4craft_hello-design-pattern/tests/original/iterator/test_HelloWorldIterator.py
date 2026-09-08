import pytest

class HelloWorldCharacterIterator:
    def __init__(self, chars):
        self.chars = chars
        self.index = 0

    def hasNext(self):
        return self.index < len(self.chars)

    def next(self):
        if self.index >= len(self.chars):
            raise Exception("UnsupportedOperationException")
        ch = self.chars[self.index]
        self.index += 1
        return ch

    def remove(self):
        raise Exception("UnsupportedOperationException")

def test_HelloWorldIterator():
    helloIterator = list("Hello Iterator!")
    iter = HelloWorldCharacterIterator(helloIterator)
    stringBuffer = []
    while iter.hasNext():
        stringBuffer.append(iter.next())
    assert "".join(stringBuffer) == "Hello Iterator!"

def test_HelloWorldIteratorRemove():
    helloIterator = list("Hello Iterator!")
    iter = HelloWorldCharacterIterator(helloIterator)
    try:
        iter.remove()
        assert False, "Should raise UnsupportedOperationException"
    except Exception as ex:
        assert str(ex) == "UnsupportedOperationException"