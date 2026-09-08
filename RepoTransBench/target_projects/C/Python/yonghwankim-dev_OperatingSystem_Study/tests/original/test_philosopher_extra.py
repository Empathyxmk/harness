import pytest

N = 5
THINKING, HUNGRY, EATING = 0, 1, 2
state = [THINKING] * N

def test_take_forks(i):
    state[i] = HUNGRY
    state[i] = EATING

def test_put_forks(i):
    state[i] = THINKING

def setup_function(function):
    global state
    state = [THINKING] * N

def test_independent_philosophers():
    global state
    state = [THINKING] * N

    test_take_forks(0)
    test_take_forks(4)

    assert state[0] == EATING
    assert state[4] == EATING

    test_put_forks(0)
    test_put_forks(4)

    assert state[0] == THINKING
    assert state[4] == THINKING

def test_rapid_cycle():
    global state
    state[2] = THINKING
    test_take_forks(2)
    assert state[2] == EATING
    test_put_forks(2)
    assert state[2] == THINKING
    test_take_forks(2)
    assert state[2] == EATING