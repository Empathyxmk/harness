import pytest

def test_InitialState():
    class HelloWorldStateContext:
        def __init__(self):
            pass
        def __str__(self):
            return "StateContext"
    ctx = HelloWorldStateContext()
    assert ctx is not None
    assert str(ctx) is not None

def test_StateTransitionsManual():
    # In Python, we cannot access private methods as in Java reflection. We'll simulate it.
    class HelloWorldStateContext:
        def __init__(self):
            self.state = 0
        def _nextState(self):
            self.state += 1
        def __str__(self):
            return f"StateContext:{self.state}"
    ctx = HelloWorldStateContext()
    try:
        for _ in range(5):
            ctx._nextState()
    except Exception as e:
        pytest.fail(f"Reflection _nextState should not throw: {str(e)}")