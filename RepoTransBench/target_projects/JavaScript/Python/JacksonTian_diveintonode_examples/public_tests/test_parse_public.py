def test_parseint_on_hexadecimal_string_public():
    assert int('2A', 16) == 42

def test_parsefloat_with_leading_trailing_whitespace_public():
    assert abs(float('   9.81  ') - 9.81) < 1e-2

def test_parseint_returns_nan_for_nonparsable_input_public():
    try:
        int('duck', 10)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Python raises exception, JS returns NaN