import pytest

class HelloWorldCharacterIterator:
    def __init__(self, chars):
        self.chars = chars
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.chars):
            ch = self.chars[self.index]
            self.index += 1
            return ch
        raise StopIteration

    def hasNext(self):
        return self.index < len(self.chars)

    def next(self):
        if self.index < len(self.chars):
            ch = self.chars[self.index]
            self.index += 1
            return ch
        raise IndexError("No more elements")

def test_iterator():
    arr = ['A', 'B', 'C']
    iter = HelloWorldCharacterIterator(arr)
    assert iter.hasNext()
    assert iter.next() == 'A'
    assert iter.hasNext()
    assert iter.next() == 'B'
    assert iter.hasNext()
    assert iter.next() == 'C'
    assert not iter.hasNext()

def test_next_throws():
    arr = []
    iter = HelloWorldCharacterIterator(arr)
    with pytest.raises(IndexError):
        iter.next()