import pytest
import pythonflow as pf
from pythonflow.util import default

def test_default_func_public():
    def f(x=13):
        return x
    assert default(f) == 13

def test_default_func_with_arg_public():
    def f(x, y=77):
        return x + y
    assert default(f, 2) == 77

def test_default_func_kwargs_public():
    def f(a, b=12, c=100):
        return a + b + c
    assert default(f, 4, 5) == 100

def test_default_func_no_defaults_public():
    def f(x, y):
        return x + y
    with pytest.raises(TypeError):
        default(f)