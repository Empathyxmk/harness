def add(a, b):
    return a + b

def is_palindrome(s):
    return s == s[::-1]

def test_add_adds_numbers_public():
    assert add(10, 7) == 17
    assert add(-3, 3) == 0
    assert add(42, 0) == 42

def test_is_palindrome_public():
    assert is_palindrome('noon') is True
    assert is_palindrome('world') is False
    assert is_palindrome('rotator') is True