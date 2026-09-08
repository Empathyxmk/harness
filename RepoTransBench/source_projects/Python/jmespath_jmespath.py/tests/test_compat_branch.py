import jmespath.compat

def test_string_type():
    assert isinstance(jmespath.compat.string_type('xyz'), str)

# Removed tests for numeric_types, unichr, mapping_type: not present in compat.py