import pytest
from src.como_lang.mocks import ComoStack

def test_stack_push_and_pop():
    s = ComoStack()
    s.como_stack_init()

    s.como_stack_push(10)
    assert s.como_stack_top() == 10

    v = s.como_stack_pop()
    assert v == 10

    # Pop from empty stack
    assert s.como_stack_pop() == 0 # Simulate C returning 0 for pop from empty

def test_stack_clear():
    s = ComoStack()
    s.como_stack_init()
    s.como_stack_push(1)
    s.como_stack_push(2)
    s.como_stack_clear()
    assert s.size == 0