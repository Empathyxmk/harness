from src.toUnsafe import toUnsafe

def test_works():
    def a(): pass
    def b(): pass
    def c(): pass

    m1 = {"componentWillMount": a, "componentWillReceiveProps": b, "componentWillUpdate": c}
    m2 = toUnsafe(m1)
    # m1 not modified
    assert m1 == {
        "componentWillMount": a, "componentWillReceiveProps": b, "componentWillUpdate": c
    }
    assert m2 == {
        "UNSAFE_componentWillMount": a,
        "UNSAFE_componentWillReceiveProps": b,
        "UNSAFE_componentWillUpdate": c
    }
    assert sorted(m2.keys()) == [
        "UNSAFE_componentWillMount", "UNSAFE_componentWillReceiveProps", "UNSAFE_componentWillUpdate"
    ]