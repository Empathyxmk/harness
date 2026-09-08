import pytest

class int3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

def add(a, b):
    return int3(a.x + b.x, a.y + b.y, a.z + b.z)

def test_add():
    a = int3(10, 20, 30)
    b = int3(-5, 4, 0)
    c = add(a, b)
    assert c.x == 5 and c.y == 24 and c.z == 30

def test_vector_loop():
    vec = []
    for i in range(4):
        vec.append(int3(i, i*2, i*3))
    total_sum = 0
    for v in vec:
        total_sum += v.x + v.y + v.z
    assert total_sum == (0+0+0) + (1+2+3) + (2+4+6) + (3+6+9)