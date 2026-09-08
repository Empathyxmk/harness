import pickle

def test_serialization_with_different_string():
    test_str = "PublicTestingStringXYZ"
    data = pickle.dumps(test_str)
    result = pickle.loads(data)
    assert result == test_str
    assert result != ""
    assert result.startswith("Public")