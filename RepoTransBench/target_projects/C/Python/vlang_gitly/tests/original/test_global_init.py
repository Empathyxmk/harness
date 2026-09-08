import pytest

# We mimic global initialization as in V ("const x = my_init()", with my_init doing assert true and returning 1)
def my_init():
    assert True
    return 1

x = my_init()

def test_my_init():
    assert x == 1