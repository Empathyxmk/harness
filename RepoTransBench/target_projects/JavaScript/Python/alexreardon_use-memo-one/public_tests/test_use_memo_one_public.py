import pytest

from src.use_memo_one import useMemoOne

class WithMemo:
    def __init__(self, inputs, get_result, children):
        self.inputs = inputs
        self.get_result = get_result
        self.children = children

    def render(self):
        value = useMemoOne(self.get_result, self.inputs)
        return self.children(value)

def test_should_not_break_cache_on_multiple_calls_with_different_inputs():
    calls = []
    def mock(val): calls.append(val); return "spanhello"
    def get_result(): return {"foo": "bar"}
    comp = WithMemo(['a', 5], get_result, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"foo": "bar"}
    initial = calls[0]
    calls.clear()

    comp.inputs = ['a', 5]
    comp.render()
    assert len(calls) == 1
    assert calls[0] == initial
    second = calls[0]
    assert initial is second

def test_should_break_cache_when_inputs_change_to_new_array():
    calls = []
    def mock(val): calls.append(val); return "spanhello"
    def get_result(): return {"foo": "bar"}
    comp = WithMemo(['a', 5], get_result, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"foo": "bar"}
    initial = calls[0]
    calls.clear()

    comp.inputs = ['a', 5, 'new']
    comp.render()
    assert len(calls) == 1
    assert calls[0] == initial
    second = calls[0]
    # should be new reference
    assert initial is not second

def test_should_use_latest_get_result_when_cache_breaks_and_return_new_result():
    calls = []
    def mock(val): calls.append(val); return "spanhello"
    def get_result(): return {"foo": "bar"}
    comp = WithMemo(['a', 5], get_result, mock)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"foo": "bar"}
    initial = calls[0]
    calls.clear()

    def new_get_result(): return {"updated": "thing"}
    comp.inputs = [10, 20, 30]
    comp.get_result = new_get_result
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"updated": "thing"}