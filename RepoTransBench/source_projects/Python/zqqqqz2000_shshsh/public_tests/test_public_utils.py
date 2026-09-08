from shshsh import utils

def test_public_is_list_tuple_str():
    assert utils.is_list([1, 2, 3])
    assert utils.is_tuple((4, 5, 6))
    assert not utils.is_list("something")
    assert utils.is_str("public_test")

def test_public_flatten():
    l = [1, [2, [3, 4]], 5]
    flat = list(utils.flatten(l))
    assert flat == [1, 2, 3, 4, 5]

def test_public_range_list():
    # Use a different range
    r = utils.range_list(7)
    assert r == [0, 1, 2, 3, 4, 5, 6]

def test_public_patch_object(tmp_path):
    class Dummy:
        pass
    d = Dummy()
    utils.patch_object(d, "x", 100)
    assert getattr(d, "x") == 100