import pytest

class SafeSpan:
    """
    Safe span variant: throws/catches errors for out-of-bounds much like a C++ test might.
    Used to demonstrate a 'public_safe' translation.
    """
    def __init__(self, data, start=0, length=None):
        self._data = data
        self._start = start
        if length is None:
            self._length = len(data) - start
        else:
            self._length = length
        if self._start < 0 or self._length < 0 or self._start + self._length > len(data):
            raise IndexError("SafeSpan out of range")
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            new_start, new_stop, new_step = idx.indices(self._length)
            elements = [self._data[self._start + i] for i in range(new_start, new_stop, new_step)]
            return SafeSpan(elements)
        adj_idx = idx if idx >= 0 else self._length + idx
        if adj_idx < 0 or adj_idx >= self._length:
            raise IndexError("SafeSpan index out of range")
        return self._data[self._start + adj_idx]
    def __len__(self):
        return self._length
    def subspan(self, offset, count=None):
        if count is None:
            count = self._length - offset
        if offset < 0 or count < 0 or offset + count > self._length:
            raise IndexError("SafeSpan subspan out of range")
        return SafeSpan(self._data, self._start + offset, count)
    def data(self):
        return self._data[self._start:self._start+self._length]

def test_safe_span_access():
    arr = ['a', 'b', 'c']
    s = SafeSpan(arr)
    assert s[0] == 'a'
    assert s[2] == 'c'
    assert s[-1] == 'c'
    with pytest.raises(IndexError):
        _ = s[3]
    with pytest.raises(IndexError):
        _ = s[-4]

def test_safe_span_subspan():
    arr = list(range(20, 30))
    s = SafeSpan(arr)
    ss = s.subspan(5, 2)
    assert list(ss.data()) == [25, 26]
    ss2 = s.subspan(0, 10)
    assert list(ss2.data()) == arr[:10]
    with pytest.raises(IndexError):
        s.subspan(-1, 1)
    with pytest.raises(IndexError):
        s.subspan(9, 20)

def test_safe_span_slice_and_compare():
    arr = [10, 20, 30, 40]
    s = SafeSpan(arr)
    assert list(s[1:4].data()) == [20, 30, 40]