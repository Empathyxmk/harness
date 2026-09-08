from src.mylib.my_strlen import my_strlen

def test_my_strlen_empty():
    assert my_strlen("") == 0

def test_my_strlen_numbers():
    assert my_strlen("1234567890") == 10

def test_my_strlen_symbols():
    assert my_strlen("!@#$") == 4

def test_my_strlen_sentence():
    assert my_strlen("The quick brown fox") == 19

def test_my_strlen_unicode_like_ascii():
    assert my_strlen("abcXYZ123") == 9