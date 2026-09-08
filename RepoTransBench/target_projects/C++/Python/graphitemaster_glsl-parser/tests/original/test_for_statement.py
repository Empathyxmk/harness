import pytest

def test_for_statement_patterns():
    # for(;;)
    i = 0
    for _ in range(1):
        pass

    # for(i = 0;;)
    i = 0
    for _ in range(1):
        pass

    # for(int i = 0; (i < 10);)
    i = 0
    for _ in range(10):
        pass

    # for(int i = 0; (i < 10); i++)
    for i in range(10):
        pass