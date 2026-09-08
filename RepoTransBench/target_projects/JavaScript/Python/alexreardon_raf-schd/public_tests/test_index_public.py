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

def test_should_not_execute_callback_before_animation_frame_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn()
    assert my_mock.call_count == 0

def test_should_execute_callback_after_animation_frame_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('run!')
    requestAnimationFrame.step()
    assert my_mock.call_count == 1

def test_should_not_execute_multiple_times_if_waiting_for_frame_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('a')
    fn('b')
    fn('c')
    fn('d')
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    requestAnimationFrame.step()
    requestAnimationFrame.flush()
    assert my_mock.call_count == 1

def test_should_execute_callback_with_latest_value_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('x')
    fn('y')
    fn('z')
    fn('final')
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    assert my_mock.calls[0][0] == 'final'

def test_should_execute_callbacks_with_latest_value_when_multiple_args_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('one','two','three')
    fn(10,20,30)
    fn('foo', 99, {'value': 'bar'})
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    assert my_mock.calls[0] == ('foo',99,{'value': 'bar'})

def test_should_return_exact_value_that_was_passed_to_callback_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    obj = {"greet": "hi"}
    fn(obj)
    requestAnimationFrame.step()
    assert my_mock.call_count == 1
    assert my_mock.calls[0][0] is obj

def test_should_allow_cancelling_of_frame_using_cancel_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('cancel-me')
    fn.cancel()
    requestAnimationFrame.step()
    assert my_mock.call_count == 0

def test_should_permit_future_frames_after_cancelling_a_frame_public():
    my_mock = MockFn()
    fn = raf_schd(my_mock)
    fn('do-cancel')
    fn.cancel()
    requestAnimationFrame.step()
    assert my_mock.call_count == 0
    fn('after-cancel')
    requestAnimationFrame.step()
    assert any(call[0] == 'after-cancel' for call in my_mock.calls)


def test_should_respect_new_bindings_public():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
        def call_mock(self):
            return mock(self.a)
    foo = Foo(25)
    def cb():
        foo.call_mock()
    schedule = raf_schd(cb)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(25,)]

def test_should_respect_explicit_bindings_public():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
    def call_mock(self):
        mock(self.a)
    foo = Foo(99)
    from functools import partial
    bound = lambda: call_mock(foo)
    schedule = raf_schd(bound)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(99,)]

def test_should_respect_implicit_bindings_public():
    mock = MockFn()
    class Foo:
        def __init__(self, a):
            self.a = a
        def call_mock(self):
            mock(self.a)
    foo = Foo(-15)
    def wrapper():
        foo.call_mock()
    schedule = raf_schd(wrapper)
    schedule()
    requestAnimationFrame.step()
    assert mock.calls == [(-15,)]

def test_should_respect_ignored_bindings_public():
    mock = MockFn()
    def call_mock_with_null():
        return mock(getattr(None, 'a'))
    schedule = raf_schd(lambda: call_mock_with_null())
    schedule()
    with pytest.raises(AttributeError):
        requestAnimationFrame.step()

def test_should_type_result_function_correctly_public():
    def fake_fn(y: int): pass
    schedule = raf_schd(fake_fn)
    schedule(123)
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
    def not_to_be_called(self):
        assert self.call_count == 0
    @property
    def mock(self):
        return self