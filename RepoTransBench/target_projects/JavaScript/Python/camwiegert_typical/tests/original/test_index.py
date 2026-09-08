import pytest
from typical import deleter, editor, writer, getOverlap, type as typ_func, edit as edit_func, wait as wait_func, perform as perform_func

def test_deleter_creates_iterable():
    steps = list(deleter('abc'))
    assert steps == ['ab', 'a', '']

def test_deleter_correct_steps():
    steps = list(deleter('ab'))
    assert [type(s) for s in steps] == [str, str]

def test_deleter_empty_string():
    steps = list(deleter(''))
    assert len(steps) == 0

def test_deleter_start_index():
    steps = list(deleter('abc', 1))
    assert len(steps) == 2

def test_deleter_end_index():
    steps = list(deleter('abc', 0, 2))
    assert len(steps) == 2

def test_deleter_emoji():
    steps = list(deleter('😊👍'))
    assert steps == ['😊', '']

def test_editor_creates_iterable():
    result = editor(['a', 'b'])
    assert hasattr(result, '__iter__')

def test_editor_correct_length():
    steps = list(editor(['a', 'b']))
    assert len(steps) > 0

def test_editor_yields_functions():
    steps = list(editor(['a', 'b']))
    assert all(callable(x) for x in steps)

def test_getOverlap_partial():
    assert getOverlap('abc', 'abd') == 2

def test_getOverlap_no_overlap():
    assert getOverlap('abc', 'xyz') == 0

def test_getOverlap_complete():
    assert getOverlap('abc', 'abc') == 3

def test_getOverlap_write_only():
    assert getOverlap('', 'foo') == 0

def test_getOverlap_delete_only():
    assert getOverlap('bar', '') == 0

def test_getOverlap_emoji():
    assert getOverlap('😊😊', '😊😎') == 1

def test_writer_creates_iterable():
    steps = list(writer('ab'))
    assert isinstance(steps, list)

def test_writer_correct_steps():
    steps = list(writer('ab'))
    assert steps == ['a', 'ab']

def test_writer_empty_string():
    steps = list(writer(''))
    assert len(steps) == 0

def test_writer_start_index():
    steps = list(writer('abc', 1))
    assert steps == ['ab', 'abc']

def test_writer_end_index():
    steps = list(writer('abc', 0, 2))
    assert steps == ['a', 'ab']

def test_writer_emoji():
    steps = list(writer('😊👍'))
    assert steps == ['😊', '😊👍']

@pytest.mark.asyncio
async def test_type_string_arg(monkeypatch):
    called = {'val': False}
    def fake_rAF(cb):
        called['val'] = True
        cb()
        return 1
    monkeypatch.setattr('builtins.requestAnimationFrame', fake_rAF, raising=False)
    node = {'textContent': 'foo'}
    await typ_func(node, 'bar')
    assert called['val'] is True
    assert node['textContent'] == 'bar'

@pytest.mark.asyncio
async def test_type_number_arg(monkeypatch):
    node = {'textContent': 'foo'}
    import time
    start = time.time()
    await typ_func(node, 0.01)
    elapsed = time.time() - start
    assert elapsed >= 0.009

@pytest.mark.asyncio
async def test_type_function_arg():
    node = {'textContent': 'x'}
    cb_called = {'val': False}
    async def cb(nd):
        cb_called['val'] = True
        nd['textContent'] = 'y'
    await typ_func(node, cb)
    assert cb_called['val'] is True
    assert node['textContent'] == 'y'

@pytest.mark.asyncio
async def test_type_default_object():
    node = {'textContent': 'z'}
    import asyncio
    obj = asyncio.Future()
    obj.set_result(None)
    await typ_func(node, obj)
    assert node['textContent'] == 'z'

@pytest.mark.asyncio
async def test_edit_edits_text(monkeypatch):
    called = {'val': False}
    def fake_rAF(cb):
        called['val'] = True
        cb()
        return 1
    monkeypatch.setattr('builtins.requestAnimationFrame', fake_rAF, raising=False)
    node = {'textContent': 'foo'}
    await edit_func(node, 'foo', 'bar')
    assert node['textContent'] == 'bar'