import pytest

class Span:
    """
    Minimal Python equivalent of the C++ span from the martinmoene_span-lite project.
    This implementation is only intended for public test demonstration purposes.
    """
    def __init__(self, data, start=0, length=None):
        # Allow reference to a list or similar sequence, with start/length "view"
        self._data = data
        self._start = start
        if length is None:
            self._length = len(data) - start
        else:
            self._length = length
        if self._start < 0 or self._length < 0 or self._start + self._length > len(data):
            raise IndexError("Span out of range")
    def __getitem__(self, idx):
        # Accept ints or slices, apply to the span's slice view
        if isinstance(idx, slice):
            new_start, new_stop, new_step = idx.indices(self._length)
            elements = [self._data[self._start + i] for i in range(new_start, new_stop, new_step)]
            return Span(elements)
        # Handle negative indices within the span
        adj_idx = idx if idx >= 0 else self._length + idx
        if adj_idx < 0 or adj_idx >= self._length:
            raise IndexError("Span index out of range")
        return self._data[self._start + adj_idx]
    def __len__(self):
        return self._length
    def subspan(self, offset, count=None):
        if count is None:
            count = self._length - offset
        if offset < 0 or count < 0 or offset + count > self._length:
            raise IndexError("Subspan out of range")
        return Span(self._data, self._start + offset, count)
    def data(self):
        return self._data[self._start:self._start+self._length]
    def __eq__(self, other):
        if isinstance(other, Span):
            return self.data() == other.data()
        return False

def test_span_basic_access():
    arr = [1, 2, 3, 4, 5]
    s = Span(arr)
    assert len(s) == 5
    assert s[0] == 1
    assert s[4] == 5
    assert s[-1] == 5
    assert list(s.data()) == arr

def test_span_out_of_bounds_access():
    arr = [10, 20, 30]
    s = Span(arr)
    with pytest.raises(IndexError):
        _ = s[3]
    with pytest.raises(IndexError):
        _ = s[-4]

def test_span_slicing():
    arr = list(range(10))
    s = Span(arr)
    s2 = s.subspan(3, 4)
    assert list(s2.data()) == [3, 4, 5, 6]
    s3 = s.subspan(5)
    assert list(s3.data()) == [5, 6, 7, 8, 9]
    s4 = s[1:5]
    assert list(s4.data()) == [1, 2, 3, 4]

def test_span_subspan_edgecases():
    arr = list(range(5))
    s = Span(arr)
    # subspan at start
    s_start = s.subspan(0, 2)
    assert list(s_start.data()) == [0, 1]
    # subspan at end
    s_end = s.subspan(3, 2)
    assert list(s_end.data()) == [3, 4]
    # subspan zero-length
    s_zero = s.subspan(5, 0)
    assert list(s_zero.data()) == []

    with pytest.raises(IndexError):
        s.subspan(-1, 2)
    with pytest.raises(IndexError):
        s.subspan(2, 10)

def test_span_equality():
    arr = [7,8,9]
    s1 = Span(arr)
    s2 = Span(arr)
    assert s1 == s2
    s3 = Span([7,8,9])
    assert s1 == s3
    arr2 = [7,8,0]
    s4 = Span(arr2)
    assert s1 != s4