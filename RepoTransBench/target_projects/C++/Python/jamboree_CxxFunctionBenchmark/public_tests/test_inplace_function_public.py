import pytest

# Python simulation for inplace_function as above
class InplaceFunction:
    def __init__(self, func=None):
        self._func = func

    def __call__(self, *args, **kwargs):
        if not self._func:
            raise TypeError("Empty InplaceFunction cannot be called")
        return self._func(*args, **kwargs)

    def __bool__(self):
        return self._func is not None

    def move_from(self, other):
        self._func = other._func
        other._func = None

def add2(x):
    return x + 2

class Mult3:
    def __call__(self, x):
        return x * 3

def test_public_basic_lambda_assign_and_call():
    f = InplaceFunction(lambda x: x + 9)
    assert f(6) == 15

def test_public_functor_assign_and_call():
    m3 = Mult3()
    f = InplaceFunction(m3)
    assert f(4) == 12

def test_public_function_ptr_assign_and_call():
    f = InplaceFunction(add2)
    assert f(9) == 11

def test_public_empty_inplace_function():
    f = InplaceFunction()
    assert not bool(f)
    with pytest.raises(TypeError):
        f(123)

def test_public_move_and_copy():
    f1 = InplaceFunction(lambda x: x + 20)
    f2 = InplaceFunction()
    f2.move_from(f1)
    assert bool(f2)
    assert not bool(f1)
    assert f2(2) == 22