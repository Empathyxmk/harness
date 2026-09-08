class Array:
    def __init__(self, capacity):
        self.buffer = [None] * capacity
        self.cursor = 0
        self.limit = capacity

    def push(self, item):
        if self.cursor == self.limit:
            self.buffer += [None] * self.limit
            self.limit = len(self.buffer)
        self.buffer[self.cursor] = item
        self.cursor += 1

    def length(self):
        return self.cursor

    def get(self, idx):
        if 0 <= idx < self.cursor:
            return self.buffer[idx]
        return None

    def free(self):
        self.buffer = []
        self.cursor = 0
        self.limit = 0

def test_Array_init_push_access_public():
    array = Array(6)
    a, b, c, d, e, f = 10, 99, -5, 201, 33, 101

    assert array.length() == 0

    array.push(a)
    array.push(b)
    array.push(c)
    array.push(d)
    array.push(e)
    array.push(f)

    assert array.length() == 6
    assert array.get(0) == a
    assert array.get(1) == b
    assert array.get(2) == c
    assert array.get(3) == d
    assert array.get(4) == e
    assert array.get(5) == f

    array.free()