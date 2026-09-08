import pytest

def test_while_statement_variants():
    i = 0
    run = 0
    while True:
        run += 1
        break
    assert run == 1

    i = 0
    count = 0
    while (i < 10):
        count += 1
        i += 1
    assert count == 10