def test_iterclass_traversal():
    # Simple inheritance
    from xworkflows import utils

    class A:
        a = 1

    class B(A):
        b = 2

    result = dict(utils.iterclass(B))
    assert result["a"] == 1
    assert result["b"] == 2

def test_iterclass_overrides():
    from xworkflows import utils

    class A:
        foo = 3

    class B(A):
        foo = 4

    result = dict(utils.iterclass(B))
    assert result["foo"] == 4