import pytest
from src.multispinner import Multispinner

def test_autostart_starts_loop_and_triggers_events_on_success(mocker):
    SPINNERS = ['a', 'b', 'c']
    update = mocker.Mock()
    update.clear = mocker.Mock()
    update.done = mocker.Mock()
    opts = {'interval': 1, 'autoStart': True}
    m = Multispinner(SPINNERS, opts)
    m.update = update
    events = []
    m.on('done', lambda: events.append('done'))
    m.on('success', lambda: events.append('success'))
    m.on('err', lambda: events.append('err'))
    for s in SPINNERS:
        m.success(s)
    # Simulate the event loop tick and loop completion
    m.loop()
    assert events == ['success', 'done'] or events == ['done', 'success']

def test_autostart_triggers_err_events_if_any_error(mocker):
    SPINNERS = ['a', 'b', 'c']
    update = mocker.Mock()
    update.clear = mocker.Mock()
    update.done = mocker.Mock()
    opts = {'interval': 1, 'autoStart': True}
    m = Multispinner(SPINNERS, opts)
    m.update = update
    error_events = []
    m.on('done', lambda: error_events.append('done'))
    m.on('success', lambda: error_events.append('success'))
    m.on('err', lambda spinner=None: error_events.append(f"err:{spinner}" if spinner else 'err'))
    m.success('a')
    m.error('b')
    m.success('c')
    m.loop()
    assert 'done' in error_events and 'err:b' in error_events
    assert 'success' not in error_events

def test_loop_handles_update_clear_undefined_safely(mocker):
    update_called = {'called': False}
    class Dummy:
        def __call__(self, strval):
            update_called['called'] = True
    m = Multispinner(['x'], {'autoStart': False, 'interval': 1})
    m.update = Dummy()
    m.update.done = lambda: None
    m.success('x')
    m.loop()
    assert update_called['called']

def test_constructor_should_support_custom_frames_and_indent():
    spinners = ['foo']
    opts = {'autoStart': False, 'indent': 5, 'frames': ['.','o'],'preText':'', 'postText': ''}
    m = Multispinner(spinners, opts)
    assert len(m.frames) == 2
    assert m.indentStr == '     '

def test_should_allow_spinners_to_be_input_as_object():
    m = Multispinner({'spin1': 'text'}, {'autoStart': False})
    assert isinstance(m.spinners, dict)
    assert 'spin1' in m.spinners