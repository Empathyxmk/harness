import jmespath.compat as compat

def test_string_type():
    assert isinstance(compat.string_type("abc"), str)

# Removed test_numeric_types, test_unichr, test_mapping_type:
# These attributes are not present in jmespath.compat, skip such tests