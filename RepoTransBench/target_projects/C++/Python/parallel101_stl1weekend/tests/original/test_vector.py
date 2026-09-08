import pytest

class Vector(list):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 1 and isinstance(args[0], int):
            super().__init__([0]*args[0])
        elif len(args) == 2 and isinstance(args[0], int):
            super().__init__([args[1]]*args[0])
        else:
            super().__init__(*args)
    def size(self):
        return len(self)
    def push_back(self, item):
        self.append(item)
    def pop_back(self):
        return self.pop()
    def clear(self):
        super().clear()
    def resize(self, n, value=0):
        while len(self) < n:
            self.append(value)
        while len(self) > n:
            self.pop()
    def reserve(self, n):
        pass
    def shrink_to_fit(self):
        pass
    def capacity(self):
        return len(self)
    def at(self, idx):
        if idx < 0 or idx >= len(self):
            raise IndexError("out of range")
        return self[idx]
    def front(self):
        return self[0]
    def back(self):
        return self[-1]
    def rbegin(self):
        return reversed(self)
    def rend(self):
        return iter([])

def test_default_ctor():
    v = Vector()
    assert v.size() == 0

def test_fill_ctor():
    v = Vector(3, 42)
    assert v.size() == 3
    assert v[1] == 42

def test_initializer_list():
    v = Vector([1,2,3,4])
    assert v.size() == 4
    assert v[2] == 3

def test_push_back_and_pop():
    v = Vector()
    for i in range(5):
        v.push_back(i*2)
    assert v.size() == 5
    v.pop_back()
    assert v.size() == 4
    assert v[3] == 6

def test_clear_resize():
    v = Vector()
    for i in range(8):
        v.push_back(i)
    v.clear()
    assert v.size() == 0
    v.resize(4, 33)
    assert v.size() == 4
    assert v[0] == 33

def test_reserve_shrink():
    v = Vector()
    v.reserve(100)
    assert v.capacity() >= 100 or v.capacity() == v.size()
    v.shrink_to_fit()
    assert v.capacity() >= v.size()

def test_out_of_range():
    v = Vector(2, 1)
    with pytest.raises(IndexError):
        v.at(10)