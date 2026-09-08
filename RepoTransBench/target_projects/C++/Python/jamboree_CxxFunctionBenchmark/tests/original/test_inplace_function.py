import pytest

# Simulate the behavior of an "inplace_function" using Python callables.
# This is just for demonstration/testing purposes.
class InplaceFunction:
    def __init__(self, func=None):
        self._func = func

    def __call__(self, *args, **kwargs):
        if not self._func:
            raise TypeError("Empty InplaceFunction cannot be called")
        return self._func(*args, **kwargs)

    def __bool__(self):
        return self._func is not None

    # Simulate move: after moving, source is empty, target is full.
    def move_from(self, other):
        self._func = other._func
        other._func = None

def add1(x):
    return x + 1

class Mult2:
    def __call__(self, x):
        return x * 2

def test_basic_lambda_assign_and_call():
    f = InplaceFunction(lambda x: x + 7)
    assert f(5) == 12

def test_functor_assign_and_call():
    m2 = Mult2()
    f = InplaceFunction(m2)
    assert f(3) == 6

def test_function_ptr_assign_and_call():
    f = InplaceFunction(add1)
    assert f(10) == 11

def test_empty_inplace_function():
    f = InplaceFunction()
    assert not bool(f)
    with pytest.raises(TypeError):
        f(123)

def test_move_and_copy():
    f1 = InplaceFunction(lambda x: x + 10)
    f2 = InplaceFunction()
    f2.move_from(f1)
    assert bool(f2)
    assert not bool(f1)
    assert f2(1) == 11