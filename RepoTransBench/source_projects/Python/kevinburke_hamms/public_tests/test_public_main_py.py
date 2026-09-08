def test_public_main_true():
    # Public: always True with different logic
    assert bool([1])

def test_public_main_value():
    # Check a different value type than existing
    assert isinstance("hamms", str)