import pytest
import rx
from rx import operators as ops
from rx.subject import Subject

def unsubscribe(disposable):
    if disposable is not None:
        try:
            disposable.dispose()
        except Exception:
            pass

def apply_schedulers():
    def _apply(source):
        return source.pipe(ops.observe_on(rx.scheduler.CurrentThreadScheduler()))
    return _apply

def apply_maybe_schedulers():
    return apply_schedulers()

def apply_single_schedulers():
    return apply_schedulers()

def apply_flowable_schedulers():
    return apply_schedulers()

def to_main_thread22222222():
    return apply_schedulers()

def to_io_thread2222222222():
    return apply_schedulers()

class DummyDisposable:
    def __init__(self):
        self.disposed = False
    def dispose(self):
        self.disposed = True

def test_unsubscribe_with_null():
    unsubscribe(None)  # should not throw

def test_unsubscribe_with_disposed():
    class DummyDisposed:
        def dispose(self): pass
        def is_disposed(self): return True
    unsubscribe(DummyDisposed())

def test_unsubscribe_with_active():
    d = DummyDisposable()
    unsubscribe(d)
    assert d.disposed

def test_apply_schedulers():
    result = []
    rx.of(1).pipe(apply_schedulers()).subscribe(lambda v: result.append(v))
    assert result == [1]

def test_apply_maybe_schedulers():
    result = []
    rx.of(2).pipe(apply_maybe_schedulers()).subscribe(lambda v: result.append(v))
    assert result == [2]

def test_apply_single_schedulers():
    result = []
    rx.of(3).pipe(apply_single_schedulers()).subscribe(lambda v: result.append(v))
    assert result == [3]

def test_apply_flowable_schedulers():
    result = []
    rx.of(4).pipe(apply_flowable_schedulers()).subscribe(lambda v: result.append(v))
    assert result == [4]

def test_to_main_thread22222222():
    result = []
    rx.of(5).pipe(to_main_thread22222222()).subscribe(lambda v: result.append(v))
    assert result == [5]

def test_to_io_thread2222222222():
    result = []
    rx.of(6).pipe(to_io_thread2222222222()).subscribe(lambda v: result.append(v))
    assert result == [6]