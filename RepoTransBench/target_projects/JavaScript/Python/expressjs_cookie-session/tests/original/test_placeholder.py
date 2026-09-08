# Equivalent to the JS test "test('placeholder', ...)"
def test_placeholder():
    """
    Equivalent to:
    test('placeholder', () => {
      expect(true).toBe(true)
    });
    """
    assert True is True