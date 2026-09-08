import pytest
from src.agile6v_nginx.hello import hello_main

def test_hello_main_original_case_1():
    """
    Corresponds to the first test in original test_hello.c.
    Tests hello_main with argc=0 and argv=NULL, expecting a return of 0.
    """
    result = hello_main(0, None) # NULL in C translates to None in Python
    assert result == 0, f"Expected hello_main(0, None) to return 0, but got {result}"

def test_hello_main_original_case_2():
    """
    Corresponds to the second test in original test_hello.c.
    Tests hello_main with argc=2 and argv=NULL, expecting a return of 0.
    """
    result = hello_main(2, None)
    assert result == 0, f"Expected hello_main(2, None) to return 0, but got {result}"