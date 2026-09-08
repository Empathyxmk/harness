import pytest

# We'll use Python's built-in apply approach, which is similar to C++17's std::apply
# For pre-3.3, there's no unpacking for tuples, but on Python 3+ we'll just use *args.

def f0():
    return 100

def f1(a):
    return a + 1

def f2(a, b):
    return a * b

def f3(a, b, c):
    return a + b + c

class Callable:
    def __call__(self, a, b, c, d):
        return a * b * c * d

def apply_tuple(fn, tup):
    return fn(*tup)

def test_apply_tuple_function0():
    t = tuple()
    result = apply_tuple(f0, t)
    assert result == 100

def test_apply_tuple_function1():
    t = (2,)
    result = apply_tuple(f1, t)
    assert result == 3

def test_apply_tuple_function2():
    t = (3, 4)
    result = apply_tuple(f2, t)
    assert result == 12

def test_apply_tuple_function3():
    t = (1, 2, 3)
    result = apply_tuple(f3, t)
    assert result == 6

def test_apply_tuple_callable():
    t = (2, 2, 2, 2)
    result = apply_tuple(Callable(), t)
    assert result == 16

def test_apply_tuple_ref():
    # Mimic reference semantics: use mutable objects, here as list
    x = [7]
    y = [5]
    # Lambda modifies x[0] and y[0]
    def lambda_fn(a, b):
        a[0] += 2
        b[0] *= 2
        return a[0] + b[0]

    tup = (x, y)
    val = apply_tuple(lambda_fn, tup)
    assert val == ((7+2)+(5*2))
    assert x[0] == 9
    assert y[0] == 10

def const_fun(a, b):
    return a - b

def test_apply_tuple_const_ref():
    t = (5, 2)
    result = apply_tuple(const_fun, t)
    assert result == 3