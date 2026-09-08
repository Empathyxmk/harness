def test_iterclass_traversal_different():
    # Different simple inheritance with different attributes
    from xworkflows import utils

    class C:
        x = 10

    class D(C):
        y = 20

    result = dict(utils.iterclass(D))
    assert result["x"] == 10
    assert result["y"] == 20

def test_iterclass_overrides_different():
    from xworkflows import utils

    class C:
        alpha = 7

    class D(C):
        alpha = 42

    result = dict(utils.iterclass(D))
    assert result["alpha"] == 42