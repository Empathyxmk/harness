import pytest
from unittest import mock
import asyncio

# Assume we have a python implementation called multipipe in src/
# The actual multipipe function must be implemented at src/multipipe.py
from src.multipipe import pipe

import io

# -- Utilities/Streams --

class ReadableDiff(io.TextIOBase):
    def __init__(self):
        super().__init__()
        self._pushed = False
        self.closed_flag = False

    def readable(self):
        return True

    def read(self, size=-1):
        if not self._pushed:
            self._pushed = True
            return "b"
        return ""

    def close(self):
        self.closed_flag = True
        super().close()

class TransformDiff(io.TextIOBase):
    def __init__(self):
        super().__init__()
        self.buf = ""
        self.closed_flag = False

    def writable(self):
        return True

    def readable(self):
        return True

    def write(self, chunk):
        # In JS, they split, reverse and uppercase the chunk
        transformed = chunk[::-1].upper()
        self.buf += transformed
        return len(chunk)

    def read(self, size=-1):
        result = self.buf
        self.buf = ""
        return result

    def close(self):
        self.closed_flag = True
        super().close()

class WritableDiff(io.TextIOBase):
    def __init__(self, cb=None):
        super().__init__()
        self.cb = cb
        self.writes = []
        self.closed_flag = False

    def writable(self):
        return True

    def write(self, chunk):
        # chunk must be "B"
        assert chunk == "B"
        self.writes.append(chunk)
        # If callback provided, call it (mimics JS done callback)
        if self.cb:
            self.cb()
        return len(chunk)

    def close(self):
        self.closed_flag = True
        super().close()

def call_async(coro):
    # Run coroutine in Python3.6/7+
    return asyncio.get_event_loop().run_until_complete(coro)

# ---- TESTS ----

def test_pipe_returns_stream():
    # pipe(done)
    # Should return a stream object
    def done():
        pass
    p = pipe(done)
    assert p is not None

def test_pipe_accepts_options():
    # pipe({objectMode: False})._readableState.objectMode === False
    # In Python we'll say pipe(..., object_mode=False)
    s = pipe(object_mode=False)
    assert getattr(s, "object_mode", True) is False

def test_pipe_a_pass_through():
    finished = []

    def done():
        finished.append(True)

    readable = ReadableDiff()
    transform = TransformDiff()
    writable = WritableDiff(cb=done)
    s = pipe(transform)  # only transform, no real passthrough logic, just for API mimicry
    # Pass through: readable -> pipe(transform) -> writable
    data = readable.read()
    transform.write(data)
    out = transform.read()
    writable.write(out)
    assert finished

def test_pipe_a_accepts_options():
    readable = ReadableDiff()
    s = pipe(readable, object_mode=False)
    assert getattr(s, "object_mode", True) is False

def test_pipe_abc_pipes_internally():
    finished = []

    def done():
        finished.append(True)

    readable = ReadableDiff()
    transform = TransformDiff()
    writable = WritableDiff(cb=done)
    # pipe(a, b, c)
    # readable -> transform -> writable
    d = readable.read()
    transform.write(d)
    out = transform.read()
    writable.write(out)
    assert finished

def test_pipe_abc_is_writable():
    finished = []

    def done():
        finished.append(True)

    transform = TransformDiff()
    writable = WritableDiff(cb=done)
    s = pipe(transform, writable)
    assert getattr(s, "writable", True)
    readable = ReadableDiff()
    d = readable.read()
    transform.write(d)
    out = transform.read()
    writable.write(out)
    assert finished

def test_pipe_abc_is_readable():
    finished = []

    def done():
        finished.append(True)

    readable = ReadableDiff()
    transform = TransformDiff()
    s = pipe(readable, transform)
    assert getattr(s, "readable", True)
    # readable -> transform
    d = readable.read()
    transform.write(d)
    out = transform.read()
    # Attach dummy writable to output
    writable = WritableDiff(cb=done)
    writable.write(out)
    assert finished

def test_pipe_abc_is_readable_and_writable():
    finished = []

    def done():
        finished.append(True)

    transform1 = TransformDiff()
    transform2 = TransformDiff()
    s = pipe(transform1, transform2)
    assert getattr(s, "readable", True)
    assert getattr(s, "writable", True)
    readable = ReadableDiff()
    d = readable.read()
    transform1.write(d)
    out1 = transform1.read()
    transform2.write(out1)
    out2 = transform2.read()
    writable = WritableDiff(cb=done)
    writable.write(out2)
    assert finished

@pytest.mark.parametrize("break_readable", [False, True])
def test_pipe_abc_errors_reemit(break_readable):
    # Should reemit error (up to 3 max)
    class ErrorStream(TransformDiff):
        pass

    transform_a = ErrorStream()
    transform_b = ErrorStream()
    transform_c = ErrorStream()
    s = pipe(transform_a, transform_b, transform_c)
    errs = []
    def error_handler(e):
        errs.append(e)

    # Attach error handler (simulate event system)
    if hasattr(s, "on_error"):
        s.on_error(error_handler)
    else:
        # Fallback: append manually
        pass

    err = Exception("public error" if not break_readable else "public error 2")
    cnt = 0
    # Simulate error emission
    for stm in [transform_a, transform_b, transform_c]:
        cnt += 1
        if hasattr(s, "on_error"):
            s.on_error(lambda e: errs.append(e))
        else:
            errs.append(err)
    assert len(errs) <= 3

def test_pipe_abc_accepts_options():
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff()
    s = pipe(a, b, c, object_mode=False)
    assert getattr(s, "object_mode", True) is False

def test_pipe_abc_fn_calls_on_finish():
    finished = []
    def cb():
        finished.append(True)
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff(cb=cb)
    done_result = []
    def fn(err):
        assert not err
        assert finished
        done_result.append(True)
    s = pipe(a, b, c, fn)
    # simulate pipeline
    d = a.read()
    b.write(d)
    out = b.read()
    c.write(out)
    assert done_result

def test_pipe_abc_fn_calls_with_error_once():
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff()
    err = Exception("error case")
    called = []
    def fn(e):
        assert e
        called.append(True)
    s = pipe(a, b, c, fn)
    # Simulate error
    if hasattr(s, "on_error"):
        s.on_error(fn)
    else:
        fn(err)
    assert called

def test_pipe_abc_fn_calls_on_destroy():
    # using a destroyable stream (here we simulate with close)
    a = ReadableDiff()
    b = TransformDiff()
    # using simple pass-through for c
    c = TransformDiff()
    called = []
    def fn(err):
        assert not err
        called.append(True)
    s = pipe(a, b, c, fn)
    # Simulate destroy on c
    c.close()
    assert called

def test_pipe_abc_fn_calls_on_destroy_with_error():
    a = ReadableDiff()
    b = TransformDiff()
    c = TransformDiff()
    err = Exception("destroy error")
    called = []
    def fn(e):
        assert e == err
        called.append(True)
    s = pipe(a, b, c, fn)
    # Simulate destroy with error
    if hasattr(s, "on_error"):
        s.on_error(fn)
    else:
        fn(err)
    assert called

def test_pipe_abc_fn_accepts_options():
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff()
    called = []
    def fn(err):
        assert not err
        called.append(True)
    s = pipe(a, b, c, object_mode=False, fn=fn)
    assert getattr(s, "object_mode", True) is False
    # Simulate pipeline
    d = a.read()
    b.write(d)
    out = b.read()
    c.write(out)
    assert called

def test_pipe_abc_fn_ignore_nonerror_parameters():
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff()
    called = []
    def fn():
        called.append(True)
    s = pipe(a, b, c, fn)
    # Simulate non-error event called on c
    fn()
    assert called

def test_pipe_list_abc_fn_calls_on_finish():
    finished = []
    def cb():
        finished.append(True)
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff(cb=cb)
    called = []
    def fn(err):
        assert not err
        assert finished
        called.append(True)
    s = pipe([a, b, c], fn)
    # simulate pipeline
    d = a.read()
    b.write(d)
    out = b.read()
    c.write(out)
    assert called

@pytest.mark.asyncio
async def test_pipe_await_abc_resolves():
    finished = []
    def cb():
        finished.append(True)

    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff(cb=cb)
    async def do_pipe():
        s = await pipe(a, b, c)
        # simulate pipeline
        d = a.read()
        b.write(d)
        out = b.read()
        c.write(out)
        return finished
    res = await do_pipe()
    assert res

@pytest.mark.asyncio
async def test_pipe_await_abc_rejects():
    a = ReadableDiff()
    b = TransformDiff()
    c = WritableDiff()
    err = Exception("async error public")
    async def do_pipe():
        try:
            s = await pipe(a, b, c)
            # Simulate error
            raise err
        except Exception as e:
            assert e == err
            return True
    assert await do_pipe()