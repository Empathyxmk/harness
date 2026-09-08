import pytest

from src.use_callback_one import useCallbackOne

class WithCallback:
    def __init__(self, inputs, callback, children):
        self.inputs = inputs
        self.callback = callback
        self.children = children

    def render(self):
        fn = useCallbackOne(self.callback, self.inputs)
        return self.children(fn)

def test_should_return_callback_until_input_change_using_string_boolean_inputs():
    calls = []
    def mock(val): calls.append(val); return "spanhi"
    def callback(): pass
    comp = WithCallback(["x", True], callback, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] is callback
    first = calls[0]
    calls.clear()
    # no input change, different callback reference but input unchanged
    comp.inputs = ["x", True]
    comp.callback = lambda: {"baz": "qux"}
    comp.render()
    assert len(calls) == 1
    assert calls[0] is first
    calls.clear()
    new_callback = lambda: None
    comp.inputs = ["x", False]
    comp.callback = new_callback
    comp.render()
    assert len(calls) == 1
    assert calls[0] is new_callback