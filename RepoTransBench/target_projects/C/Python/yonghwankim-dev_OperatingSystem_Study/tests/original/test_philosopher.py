import pytest

N = 5
THINKING, HUNGRY, EATING = 0, 1, 2
state = [THINKING] * N

def test_take_forks(i):
    # Simulate: set to HUNGRY and arbitrarily go to EATING for test
    state[i] = HUNGRY
    state[i] = EATING

def test_put_forks(i):
    state[i] = THINKING

def setup_function(function):
    global state
    state = [THINKING] * N

def test_philo_cycle():
    global state
    state = [THINKING] * N
    test_take_forks(1)
    assert state[1] == EATING
    test_put_forks(1)
    assert state[1] == THINKING