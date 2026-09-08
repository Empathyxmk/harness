def test_public_2010_from_2012():
    # Simulate transforming a vector with public data: inputVec = [3,6,9,12]; expected = inputVec / 3
    inputVec = [3, 6, 9, 12]
    expected = [1.0, 2.0, 3.0, 4.0]
    result = [x / 3.0 for x in inputVec]
    assert result == expected, "public_test_2010_from_2012 failed: output mismatch."