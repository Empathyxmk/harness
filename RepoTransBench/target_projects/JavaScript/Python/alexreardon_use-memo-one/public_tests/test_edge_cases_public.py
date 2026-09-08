import pytest
from src.use_memo_one import useMemoOne
from src.use_callback_one import useCallbackOne

class MemoComp:
    def __init__(self, get_result, inputs=None):
        self.get_result = get_result
        self.inputs = inputs
        self.output = None

    def render(self):
        value = useMemoOne(self.get_result, self.inputs)
        self.output = value

def test_handles_undefined_inputs_and_different_return_value():
    def get_result(): return 12345
    comp = MemoComp(get_result)
    comp.render()
    assert comp.output == 12345
    def get_result2(): return 67890
    comp.get_result = get_result2
    comp.render()
    assert comp.output == 67890

def test_works_with_objects_and_falsy_values_in_inputs():
    def get_result(): return "otherVal"
    obj = {"z":9}
    comp = MemoComp(get_result, [obj, False, 0])
    comp.render()
    assert comp.output == "otherVal"
    comp.inputs = [obj, False, 1]
    comp.render()
    assert comp.output == "otherVal"

class CallbackComp:
    def __init__(self, callback, inputs=None):
        self.callback = callback
        self.inputs = inputs
        self.out = None

    def render(self):
        fn = useCallbackOne(self.callback, self.inputs)
        self.out = callable(fn)

def test_handles_empty_array_for_inputs():
    def callback(): pass
    comp = CallbackComp(callback, [])
    comp.render()
    assert comp.out == True

def test_returns_new_callback_if_inputs_changes_with_objects():
    def callback(): pass
    comp = CallbackComp(callback, [{"a":1},0])
    comp.render()
    first_out = comp.out
    comp.inputs = [{"a":2},0]
    comp.render()
    after_out = comp.out
    assert after_out == first_out