from qcore import debug

def test_trace_decorator(capsys):
    @debug.trace(enter=True, exit=True)
    def test_fn(x, y=7):
        return x + y
    result = test_fn(2, y=3)
    captured = capsys.readouterr()
    assert result == 5
    assert "test_fn" in captured.out

def test_debug_counter_increment_decrement_and_dump(capsys):
    counter = debug.DebugCounter("test", value=10)
    assert counter.value == 10
    counter.increment(2)
    assert counter.value == 12
    counter.decrement(3)
    assert counter.value == 9
    counter.dump()
    captured = capsys.readouterr()
    assert "DebugCounter('test', value=9)" in captured.out

def test_debug_counter_dump_if_and_break_if(monkeypatch):
    counter = debug.DebugCounter("cond", value=10)
    was_break = {}
    def fake_breakpoint():
        was_break["hit"] = True
    monkeypatch.setattr(debug, "breakpoint", fake_breakpoint)
    counter.dump_if(lambda c: c.value == 10, and_break=True)
    assert was_break["hit"]

    was_break = {}
    counter.break_if(lambda c: True)
    assert was_break["hit"]

def test_counter_singleton():
    c1 = debug.counter("unique1")
    c2 = debug.counter("unique1")
    assert c1 is c2
    c3 = debug.counter("unique2")
    assert c1 is not c3

def test_debug_breakpoint(capsys):
    debug.breakpoint()
    captured = capsys.readouterr()
    assert "Breakpoint reached." in captured.out

def test_debug_hang_me(monkeypatch, capsys):
    called = {}
    monkeypatch.setattr("time.sleep", lambda secs: (_ for _ in ()).throw(KeyboardInterrupt()))
    debug.hang_me(timeout_secs=1)
    captured = capsys.readouterr()
    assert "Sleeping. Press Ctrl-C to continue..." in captured.out
    assert "Done sleeping" in captured.out

def test_format_stack():
    stack = debug.format_stack()
    assert isinstance(stack, str)
    assert "test_format_stack" in stack

def test_get_bool_by_mask_and_set_by_mask():
    class Dummy:
        DEBUG_X = True
        DEBUG_Y = False
        NAME = "test"
        def method(self): pass

    assert debug.get_bool_by_mask(Dummy, "DEBUG_") is False
    obj = Dummy()
    debug.set_by_mask(obj, "DEBUG_", True)
    assert obj.DEBUG_X is True and obj.DEBUG_Y is True
    debug.set_by_mask(obj, "NAME", "replaced")
    assert obj.NAME == "replaced"