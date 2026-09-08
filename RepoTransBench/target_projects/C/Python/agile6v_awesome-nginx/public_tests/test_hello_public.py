import pytest
from src.agile6v_nginx.hello import hello_main

def test_hello_main_public_case_1():
    """
    Corresponds to the first test in public tests/test_hello_public.c.
    Tests hello_main with argc=1 and argv=NULL, expecting a return of 0.
    """
    result = hello_main(1, None)
    assert result == 0, f"Expected hello_main(1, None) to return 0, but got {result}"

def test_hello_main_public_case_2():
    """
    Corresponds to the second test in public tests/test_hello_public.c.
    Tests hello_main with argc=10 and argv=NULL, expecting a return of 0.
    """
    result = hello_main(10, None)
    assert result == 0, f"Expected hello_main(10, None) to return 0, but got {result}"