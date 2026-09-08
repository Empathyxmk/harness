def test_values():
    reps = [ "BASE32", "BASE64" ]
    assert reps is not None
    assert len(reps) > 0

def test_value_of():
    assert "BASE32" == "BASE32"
    assert "BASE64" == "BASE64"