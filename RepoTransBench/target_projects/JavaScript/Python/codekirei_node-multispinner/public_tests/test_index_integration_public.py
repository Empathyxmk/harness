import pytest
from src.multispinner import Multispinner

def test_autostart_starts_loop_and_triggers_events_on_success_public_spinners(mocker):
    PUB_SPINNERS = ['alpha', 'beta', 'gamma']
    update = mocker.Mock()
    update.clear = mocker.Mock()
    update.done = mocker.Mock()
    opts = {'interval': 2, 'autoStart': True}
    m = Multispinner(PUB_SPINNERS, opts)
    m.update = update
    events = []
    m.on('done', lambda: events.append('done'))
    m.on('success', lambda: events.append('success'))
    m.on('err', lambda: events.append('err'))
    for s in PUB_SPINNERS:
        m.success(s)
    m.loop()
    assert events == ['success', 'done'] or events == ['done', 'success']

def test_autostart_triggers_err_events_if_any_error_public_different_error(mocker):
    PUB_SPINNERS = ['alpha', 'beta', 'gamma']
    update = mocker.Mock()
    update.clear = mocker.Mock()
    update.done = mocker.Mock()
    opts = {'interval': 2, 'autoStart': True}
    m = Multispinner(PUB_SPINNERS, opts)
    m.update = update
    error_events = []
    m.on('done', lambda: error_events.append('done'))
    m.on('success', lambda: error_events.append('success'))
    m.on('err', lambda spinner=None: error_events.append(f"err:{spinner}" if spinner else 'err'))
    m.success('alpha')
    m.error('beta')
    m.success('gamma')
    m.loop()
    assert 'done' in error_events and 'err:beta' in error_events
    assert 'success' not in error_events

def test_loop_handles_update_clear_undefined_safely_public_case(mocker):
    called_flag = {'called': False}
    class Dummy:
        def __call__(self, strval):
            called_flag['called'] = True
    m = Multispinner(['u'], {'autoStart': False, 'interval': 2})
    m.update = Dummy()
    m.update.done = lambda: None
    m.success('u')
    m.loop()
    assert called_flag['called']

def test_constructor_should_support_custom_frames_and_indent_public_different_frames_indent():
    spinners = ['unique']
    opts = {'autoStart': False, 'indent': 3, 'frames': ['*','-','#'], 'preText': '***', 'postText': '###'}
    m = Multispinner(spinners, opts)
    assert len(m.frames) == 3
    assert m.indentStr == '   '

def test_should_allow_spinners_to_be_input_as_object_public_key_value_different():
    m = Multispinner({'pubSpin': 'otherPublic'}, {'autoStart': False})
    assert isinstance(m.spinners, dict)
    assert 'pubSpin' in m.spinners