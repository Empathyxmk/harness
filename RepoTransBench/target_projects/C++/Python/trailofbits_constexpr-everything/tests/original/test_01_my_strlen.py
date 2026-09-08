from src.mylib.my_strlen import my_strlen


def get_input(in_str: str) -> str:
    # Simulate input instead of input() for testability.
    return in_str

def test_my_strlen_cases():
    assert my_strlen("abc") == 3
    assert my_strlen("") == 0
    assert my_strlen("hello world") == 11
    assert my_strlen("hi\nbye") == 6

def test_get_input_cases():
    assert get_input("abc") == "abc"
    assert get_input("") == ""
    assert get_input("with space") == "with space"