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

def test_should_return_callback_until_input_change():
    calls = []
    def mock_fn(cb): calls.append(cb); return "divhey"
    def callback(): pass
    comp = WithCallback([1,2], callback, mock_fn)
    comp.render()
    assert len(calls) == 1
    assert calls[0] is callback
    first = calls[0]
    calls.clear()
    # no input change, different callback reference (should still memoize and return same)
    comp.inputs = [1,2]
    comp.callback = lambda: {"hello": "world"}
    comp.render()
    assert len(calls) == 1
    second = calls[0]
    assert second is first
    calls.clear()
    # input change, change callback reference
    new_callback = lambda: None
    comp.inputs = [1,2,3]
    comp.callback = new_callback
    comp.render()
    assert len(calls) == 1
    third = calls[0]
    assert third is new_callback