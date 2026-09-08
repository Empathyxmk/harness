import pytest
from src.use_memo_one import useMemoOne

class WithMemo:
    def __init__(self, get_result, inputs=None, children=None):
        self.get_result = get_result
        self.inputs = inputs
        self.children = children

    def render(self):
        value = useMemoOne(self.get_result, self.inputs)
        if self.children is not None:
            return self.children(value)
        return value

def test_should_not_memoize_with_no_inputs():
    calls = []
    def mock(val): calls.append(val); return "divhey"
    comp = WithMemo(lambda: {"hello": "world"}, None, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "world"}
    initial = calls[0]
    calls.clear()
    # different get_result, still no inputs: should call again
    comp.get_result = lambda: {"hello": "there"}
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "there"}

def test_should_start_memoizing_if_inputs_are_provided():
    calls = []
    def mock(val): calls.append(val); return "divhey"
    comp = WithMemo(lambda: {"hello": "world"}, None, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "world"}
    initial = calls[0]
    calls.clear()
    # no inputs initially, transition to inputs
    comp.inputs = [1,2]
    comp.get_result = lambda: {"hello": "there"}
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "there"}
    second = calls[0]
    calls.clear()
    # memoization, same inputs
    comp.inputs = [1,2]
    comp.get_result = lambda: {"hello": "there"}
    comp.render()
    assert len(calls) == 1
    third = calls[0]
    assert third is second
    calls.clear()
    # memoization lost, inputs gone
    comp.inputs = None
    comp.get_result = lambda: {"hello": "there"}
    comp.render()
    assert len(calls) == 1
    fourth = calls[0]
    assert fourth == {"hello": "there"}
    assert fourth is not third

def test_should_only_call_get_result_once_on_first_pass():
    calls = []
    def get_result():
        calls.append("called")
        return {"hello": "friend"}
    comp = WithMemo(get_result, None, lambda v: None)
    comp.render()
    assert len(calls) == 1