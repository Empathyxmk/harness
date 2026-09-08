import pytest
from src.como_lang.mocks import ComoStack

def test_stack_push_pop_public():
    stack = ComoStack().como_stack_create() # Use the creator method
    value = 987654
    stack.como_stack_push(value) # Push the value directly

    ret = stack.como_stack_pop()
    assert ret == 987654

    stack.como_stack_free() # Call the mock free method

def test_stack_push2_public():
    stack = ComoStack().como_stack_create()
    a = -1
    b = 0
    stack.como_stack_push(a)
    stack.como_stack_push(b)

    retb = stack.como_stack_pop()
    reta = stack.como_stack_pop()

    assert retb == 0
    assert reta == -1

    stack.como_stack_free()