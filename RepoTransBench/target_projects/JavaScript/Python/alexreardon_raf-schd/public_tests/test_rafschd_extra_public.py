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

def test_should_do_nothing_if_cancel_called_with_no_frame_scheduled_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    scheduled.cancel()
    assert fn.call_count == 0

def test_should_still_work_if_passed_undefined_no_arguments_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    scheduled()
    requestAnimationFrame.step()
    assert fn.call_count == 1
    assert len(fn.calls[0]) == 0

def test_should_queue_new_value_after_cancel_and_reinvoke_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    scheduled('foo1')
    scheduled.cancel()
    # Schedule again after cancel
    scheduled('foo2')
    requestAnimationFrame.step()
    assert fn.call_count == 1
    assert fn.calls[0][0] == 'foo2'

def test_should_not_call_callback_if_raf_cancelled_immediately_in_same_tick_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    scheduled('baz')
    scheduled.cancel()
    requestAnimationFrame.step()
    assert fn.call_count == 0

def test_should_pass_multiple_argument_types_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    value = {'test': True}
    scheduled(False, [1,2,3], value)
    requestAnimationFrame.step()
    assert fn.calls[0] == (False, [1,2,3], value)

def test_should_allow_cancel_to_be_called_multiple_times_safely_public():
    fn = MockFn()
    scheduled = raf_schd(fn)
    scheduled('repeat')
    scheduled.cancel()
    scheduled.cancel()
    requestAnimationFrame.step()
    assert fn.call_count == 0

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