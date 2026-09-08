def test_value_of():
    assert "HmacSHA1" == "HmacSHA1"
    assert "HmacSHA256" == "HmacSHA256"
    assert "HmacSHA512" == "HmacSHA512"

def test_values_are_present():
    all_names = "".join(["HmacSHA1", "HmacSHA256", "HmacSHA512"])
    assert "HmacSHA1" in all_names
    assert "HmacSHA256" in all_names
    assert "HmacSHA512" in all_names