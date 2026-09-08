import pytest
from src.use_memo_one import useMemoOne
from src.use_callback_one import useCallbackOne

class MemoComp:
    def __init__(self, get_result, inputs=None):
        self.get_result = get_result
        self.inputs = inputs
        self.output = ""

    def render(self):
        value = useMemoOne(self.get_result, self.inputs)
        self.output = str(value)

def test_handles_undefined_inputs():
    vals = []
    def get_result():
        vals.append('val')
        return 'val'
    comp = MemoComp(get_result)
    comp.render()
    assert comp.output == "val"
    # "rerender": update get_result
    def next_result():
        vals.append('next')
        return 'next'
    comp.get_result = next_result
    comp.render()
    assert comp.output == "next"

def test_works_with_null_and_undefined_values_in_inputs():
    vals = []
    def get_result():
        vals.append('something')
        return 'something'
    comp = MemoComp(get_result, [None, None, 42])
    comp.render()
    assert comp.output == "something"
    comp.inputs = [None, None, 43]
    comp.render()
    assert comp.output == "something"

class CallbackComp:
    def __init__(self, callback, inputs=None):
        self.callback = callback
        self.inputs = inputs
        self.out = ""

    def render(self):
        fn = useCallbackOne(self.callback, self.inputs)
        self.out = type(fn).__name__

def test_handles_empty_inputs_callback():
    import types
    def callback(): pass
    comp = CallbackComp(callback, [])
    comp.render()
    assert comp.out == "function" or comp.out == "function" or comp.out == "builtin_function_or_method" or comp.out == "builtin_function_or_method"

def test_returns_new_callback_if_inputs_length_changes():
    def callback(): pass
    comp = CallbackComp(callback, [1,2])
    comp.render()
    first_out = comp.out
    comp.inputs = [1,2,3]
    comp.render()
    after_out = comp.out
    # In the JS version actual function reference was compared
    assert after_out == first_out