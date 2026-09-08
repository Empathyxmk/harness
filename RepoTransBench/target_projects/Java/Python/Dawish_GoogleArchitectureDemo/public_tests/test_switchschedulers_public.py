import rx
from rx import operators as ops

def apply_schedulers():
    def _apply(source):
        # In this context, trampoline means immediate schedule; rx's default works for sync tests.
        return source.pipe(ops.observe_on(rx.scheduler.CurrentThreadScheduler()))
    return _apply

def test_apply_schedulers_different_data():
    result = []
    rx.of("alpha").pipe(apply_schedulers()).subscribe(lambda v: result.append(v))
    assert result == ["alpha"]