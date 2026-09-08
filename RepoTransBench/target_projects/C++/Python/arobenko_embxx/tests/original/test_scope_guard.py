import pytest

class ScopeGuard:
    def __init__(self, func):
        self.func = func
        self.active = True

    def release(self):
        self.active = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.func()
        return False

    def __del__(self):
        # Only execute if not called from within context manager
        if getattr(self, "active", False):
            self.__exit__(None, None, None)

def make_scope_guard(func):
    return ScopeGuard(func)


def test_basic_execution():
    executed = {"val": False}
    def cb():
        executed["val"] = True
    guard = make_scope_guard(cb)
    del guard
    # __del__ executes after deletion for direct construction (otherwise with 'with' it's on context exit)
    assert executed["val"]

def test_release_prevents_execution():
    executed = {"val": False}
    guard = make_scope_guard(lambda: executed.update(val=True))
    guard.release()
    del guard
    assert not executed["val"]

def test_multiple_guards_execution_order():
    execution_order = []
    guard1 = make_scope_guard(lambda: execution_order.append(1))
    guard2 = make_scope_guard(lambda: execution_order.append(2))
    guard3 = make_scope_guard(lambda: execution_order.append(3))
    del guard3
    del guard2
    del guard1
    assert execution_order == [3, 2, 1]

def test_multiple_guards_with_release():
    execution_order = []
    guard1 = make_scope_guard(lambda: execution_order.append(1))
    guard2 = make_scope_guard(lambda: execution_order.append(2))
    guard3 = make_scope_guard(lambda: execution_order.append(3))
    guard2.release()
    del guard3
    del guard2
    del guard1
    assert execution_order == [3, 1]

def func_pointer_callback_state():
    if not hasattr(func_pointer_callback_state, 'value'):
        func_pointer_callback_state.value = False
    return func_pointer_callback_state

def func_pointer_callback():
    func_pointer_callback_state().value = True

def test_function_pointer_callback():
    func_pointer_callback_state().value = False
    guard = make_scope_guard(func_pointer_callback)
    del guard
    assert func_pointer_callback_state().value

def param_func_state():
    if not hasattr(param_func_state, 'value'):
        param_func_state.value = 0
    return param_func_state

def param_func(val):
    param_func_state().value = val

def test_function_with_parameter_callback():
    param_func_state().value = 0
    from functools import partial
    guard = make_scope_guard(partial(param_func, 123))
    del guard
    assert param_func_state().value == 123

def test_noexcept_safety():
    # In Python, all functions are essentially noexcept unless they throw
    try:
        guard = make_scope_guard(lambda: None)  # No error expected
        del guard
    except Exception:
        pytest.fail("make_scope_guard threw an exception unexpectedly")