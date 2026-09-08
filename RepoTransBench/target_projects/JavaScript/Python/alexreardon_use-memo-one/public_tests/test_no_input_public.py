import pytest

from src.use_memo_one import useMemoOne
from src.use_callback_one import useCallbackOne

def test_use_memo_one_get_result_returns_number_on_undefined_inputs():
    def get_result(): return 100
    value = useMemoOne(get_result)
    assert value == 100
    # simulate rerender with new get_result
    def get_result2(): return 200
    value2 = useMemoOne(get_result2)
    assert value2 == 200

def test_use_callback_one_callback_returns_function_on_undefined_inputs():
    def callback(): pass
    fn = useCallbackOne(callback)
    assert callable(fn)