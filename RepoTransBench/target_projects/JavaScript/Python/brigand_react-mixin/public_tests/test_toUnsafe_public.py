from src.toUnsafe import toUnsafe

def test_works_with_different_functions_and_keys_public_test():
    def x(): return 'foo'
    def y(): return 'bar'
    def z(): return 'baz'

    m1 = {"componentWillMount": x, "componentWillReceiveProps": y, "componentWillUpdate": z}
    m2 = toUnsafe(m1)
    # m1 not modified
    assert m1 == {
        "componentWillMount": x, "componentWillReceiveProps": y, "componentWillUpdate": z
    }
    assert m2 == {
        "UNSAFE_componentWillMount": x,
        "UNSAFE_componentWillReceiveProps": y,
        "UNSAFE_componentWillUpdate": z
    }
    assert sorted(m2.keys()) == [
        "UNSAFE_componentWillMount", "UNSAFE_componentWillReceiveProps", "UNSAFE_componentWillUpdate"
    ]