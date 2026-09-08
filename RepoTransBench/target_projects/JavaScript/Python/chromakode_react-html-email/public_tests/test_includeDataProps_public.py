from src.includeDataProps import include_data_props

def test_returns_only_data_props_public_variant():
    props = {
        "hello": "world",
        "data-public": "xyz",
        "data-bar": 123,
        "aria-hidden": "false",
        "className": "my-class",
    }
    result = include_data_props(props)
    assert result == {"data-public": "xyz", "data-bar": 123}
    assert "hello" not in result
    assert "aria-hidden" not in result

def test_returns_empty_when_only_non_data_props_public():
    assert include_data_props({"alpha": 7, "bravo": "zulu"}) == {}

def test_handles_empty_input_public_variant():
    assert include_data_props({}) == {}