import pytest
import threading
import time

def test_transition_has_duration_and_apply_method():
    # Equivalent to the fakeDefine logic
    class Transition:
        duration = 700
        def apply(self, el, type_, callback):
            applied_class = 'animated ' + type_
            if el and hasattr(el, "add_class"):
                el.add_class(applied_class)
            timer = threading.Timer(self.duration / 1000.0, callback)
            timer.start()
    transition = Transition()
    assert hasattr(transition, 'duration')
    assert transition.duration == 700
    assert hasattr(transition, 'apply')
    assert callable(transition.apply)

def test_add_class_and_call_callback_after_duration():
    added = {}
    class FakeEl:
        def add_class(self, cls):
            added['cls'] = cls
    done_event = threading.Event()
    def callback():
        assert added.get('cls') == 'animated fadeIn'
        done_event.set()
    class Transition:
        duration = 0.01 * 1000  # 10ms like source (ms)
        def apply(self, el, type_, callback):
            el.add_class('animated ' + type_)
            timer = threading.Timer(self.duration / 1000.0, callback)
            timer.start()
    transition = Transition()
    fake_el = FakeEl()
    transition.apply(fake_el, 'fadeIn', callback)
    # Wait up to 0.5s for callback
    assert done_event.wait(0.5), "Callback was not called"