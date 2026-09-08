import pytest

from src.use_memo_one import useMemoOne

class WithMemo:
    """
    Simulate: WithMemoProps { inputs, children, getResult }
    Simulates a wrapper using useMemoOne and passing its value to 'children'
    """
    def __init__(self, inputs, get_result, children):
        self.inputs = inputs
        self.get_result = get_result
        self.children = children

    def render(self):
        value = useMemoOne(self.get_result, self.inputs)
        return self.children(value)

def test_should_not_break_cache_on_multiple_calls():
    # Simulate component/mock
    calls = []
    def mock_fn(val): calls.append(val); return "divhey"
    def get_result(): return {"hello": "world"}
    comp = WithMemo([1,2], get_result, mock_fn)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "world"}
    initial = calls[0]
    calls.clear()

    # setProps with same inputs
    comp.inputs = [1,2]
    comp.render()
    # Still only called once, but returns the memoized value
    assert len(calls) == 1
    assert calls[0] == initial
    second = calls[0]
    assert initial is second

def test_should_break_cache_when_inputs_change():
    calls = []
    def mock_fn(val): calls.append(val); return "divhey"
    def get_result(): return {"hello": "world"}
    comp = WithMemo([1,2], get_result, mock_fn)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "world"}
    initial = calls[0]
    calls.clear()

    comp.inputs = [1,2,3]
    comp.render()  # Different inputs triggers cache bust
    assert len(calls) == 1
    assert calls[0] == initial  # Called with old, then:
    second = calls[0]
    assert initial is not second

def test_should_use_latest_get_result_when_cache_breaks():
    calls = []
    def mock_fn(val): calls.append(val); return "divhey"
    def get_result(): return {"hello": "world"}
    comp = WithMemo([1,2], get_result, mock_fn)
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"hello": "world"}
    initial = calls[0]
    calls.clear()

    def new_get_result(): return {"different": "value"}
    comp.inputs = [1,2,3]
    comp.get_result = new_get_result
    comp.render()
    assert len(calls) == 1
    assert calls[0] == {"different": "value"}