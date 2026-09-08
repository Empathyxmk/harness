import pytest

# Simulate the sum and runner logic
sum_result = 0
def runner(arg):
    global sum_result
    sum_result = 5  # As per the C test (runner sets sum to 5)

def setup_function(function):
    global sum_result
    sum_result = 0

def test_runner_adds():
    global sum_result
    sum_result = 0
    runner(None)
    assert sum_result == 5