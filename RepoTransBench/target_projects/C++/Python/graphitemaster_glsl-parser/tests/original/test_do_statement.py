import pytest

def test_do_statement_emulation():
    results = []
    a_was_run = []

    def a():
        a_was_run.append(True)

    i = 0
    while True:
        a()
        break
    assert a_was_run

    # Second form: do { } while(true);
    executed = False
    for _ in range(1):
        executed = True
    assert executed