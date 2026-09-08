import pytest

from src.raf_schd import (
    replace_raf,
    requestAnimationFrame,
    raf_schd
)

replace_raf()

@pytest.fixture(autouse=True)
def _reset_raf_before_each():
    requestAnimationFrame.reset()
    yield

def test_should_not_execute_callback_before_animation_frame():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn()
    assert my_mock.call_count == 0

def test_should_execute_callback_after_animation_frame():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn()
    requestAnimationFrame.step()
    assert my_mock.call_count == 1

def test_should_not_execute_multiple_times_if_waiting_for_frame():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn()
    fn()
    fn()
    fn()
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    # Should have no further effect
    requestAnimationFrame.step()
    requestAnimationFrame.flush()
    assert my_mock.call_count == 1

def test_should_execute_callback_with_latest_value():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn(1)
    fn(2)
    fn(3)
    fn(4)
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    # Only last value delivered
    assert my_mock.calls[0][0] == 4

def test_should_execute_callbacks_with_latest_values_when_multiple_args():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn(1,2,3)
    fn(4,5,6)
    fn(7,8,9)
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    assert my_mock.calls[0] == (7,8,9)

def test_should_return_exact_value_that_was_passed_to_callback():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    value = {"hello": "world"}
    fn(value)
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    # Should be the same instance
    assert my_mock.calls[0][0] is value

def test_should_allow_cancelling_of_frame_using_cancel():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn(10)
    fn.cancel()
    requestAnimationFrame.step()
    assert my_mock.call_count == 0

def test_should_permit_future_frames_after_cancelling_a_frame():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn(10)
    fn.cancel()
    requestAnimationFrame.step()
    assert my_mock.call_count == 0
    # Second attempt, not cancelled
    fn(20)
    requestAnimationFrame.step()
    assert my_mock.calls[0][0] == 20

# Context tests
def test_should_respect_new_bindings():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
        def call_mock(self):
            return mock(self.a)
    foo = Foo(10)
    def cb():
        foo.call_mock()
    schedule = raf_schd(cb)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(10,)]

def test_should_respect_explicit_bindings():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
    def call_mock(self):
        mock(self.a)
    foo = Foo(50)
    from functools import partial
    bound = lambda: call_mock(foo)
    schedule = raf_schd(bound)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(50,)]

def test_should_respect_implicit_bindings():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
        def call_mock(self):
            mock(self.a)
    foo = Foo(50)
    def wrapper():
        foo.call_mock()
    schedule = raf_schd(wrapper)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(50,)]

def test_should_respect_ignored_bindings():
    mock = MockFn()
    def call_mock_with_null():
        # Simulate JS: callMock.call(null) => should error
        return mock(getattr(None, 'a'))  # will raise AttributeError
    schedule = raf_schd(lambda: call_mock_with_null())
    schedule()
    with pytest.raises(AttributeError):
        requestAnimationFrame.step()

def test_should_type_result_function_correctly():
    def fake_fn(x: int): pass
    schedule = raf_schd(fake_fn)
    schedule(10)
    schedule.cancel()


class MockFn:
    def __init__(self):
        self.calls = []
        self.call_count = 0
    def __call__(self, *a, **k):
        self.calls.append(a)
        self.call_count += 1
    def reset(self):
        self.calls = []
        self.call_count = 0
    def toHaveBeenCalledTimes(self, n):
        assert self.call_count == n
    def toBeCalledWith(self, *a):
        assert a in self.calls
    def not_to_be_called(self):
        assert self.call_count == 0
    @property
    def mock(self):
        return self