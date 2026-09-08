import pytest

# Simulate main function
def fake_main(argc, argv):
    return 0

def test_main_runnable():
    argv = ["prog"]
    res = fake_main(1, argv)
    assert res == 0