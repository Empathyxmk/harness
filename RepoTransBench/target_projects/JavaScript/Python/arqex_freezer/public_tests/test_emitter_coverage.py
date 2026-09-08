from src.emitter import Emitter

def test_emit_value_to_handler():
    e = Emitter()
    log = []
    def handler(x):
        log.append(x * 2)
    e.on('event', handler)
    e.trigger('event', 21)
    assert log == [42]

def test_off_handler_and_not_call_after_off():
    e = Emitter()
    v = 0
    def handler(n):
        nonlocal v
        v = n
    e.on('test', handler)
    e.off('test', handler)
    e.trigger('test', 999)
    assert v == 0

def test_support_multiple_events_and_handlers():
    e = Emitter()
    count = 0
    def handler_x():
        nonlocal count
        count += 2
    def handler_y():
        nonlocal count
        count += 3
    e.on('x', handler_x)
    e.on('y', handler_y)
    e.trigger('x')
    e.trigger('y')
    assert count == 5

def test_trigger_with_multiple_arguments():
    e = Emitter()
    args = []
    def handler(a, b, c):
        args[:] = [a, b, c]
    e.on('multi', handler)
    e.trigger('multi', 'alpha', 'beta', 'gamma')
    assert args == ['alpha', 'beta', 'gamma']

def test_off_with_no_arguments_removes_all():
    e = Emitter()
    cnt = 0
    def h1():
        nonlocal cnt
        cnt += 11
    def h2():
        nonlocal cnt
        cnt += 22
    e.on('E', h1)
    e.on('E', h2)
    e.off('E')
    e.trigger('E')
    assert cnt == 0