import pytest

def get_hello_string(name: str) -> str:
    if name == "":
        return "Hello, World!"
    else:
        return f"Hello, {name}!"

def test_normal_case(capfd):
    greet = get_hello_string("World")
    print(greet)
    assert greet == "Hello, World!"
    out, err = capfd.readouterr()
    assert "Hello, World!" in out

def test_edge_case_empty_string(capfd):
    greet = get_hello_string("")
    print(greet)
    assert greet == "Hello, World!"
    out, err = capfd.readouterr()
    assert "Hello, World!" in out

def test_another_name(capfd):
    greet = get_hello_string("Alice")
    print(greet)
    assert greet == "Hello, Alice!"
    out, err = capfd.readouterr()
    assert "Hello, Alice!" in out

def test_all_tests_passed_output(capfd):
    print("All tests passed.")
    out, err = capfd.readouterr()
    assert "All tests passed." in out