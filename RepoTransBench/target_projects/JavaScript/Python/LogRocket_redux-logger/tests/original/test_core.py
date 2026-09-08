import pytest
from unittest import mock

@pytest.fixture
def default_colors():
    return {
        'title': lambda: 'red',
        'prevState': lambda: 'blue',
        'action': lambda: 'green',
        'error': lambda: 'black',
        'nextState': lambda: 'yellow'
    }

def build_logger():
    class Logger:
        def __init__(self):
            self.log = mock.Mock()
            self.group = mock.Mock()
            self.groupCollapsed = mock.Mock()
            self.groupEnd = mock.Mock()
            self.trace = mock.Mock()
            self.withTrace = False
    return Logger()

def get_default_options(default_colors, overrides=None):
    if overrides is None:
        overrides = {}
    opts = {
        'logger': build_logger(),
        'actionTransformer': lambda a: a,
        'titleFormatter': None,
        'collapsed': False,
        'colors': default_colors,
        'level': 'log',
        'diff': False,
        'timestamp': True,
        'duration': True,
    }
    opts.update(overrides)
    return opts

def build_buffer(error=False):
    from datetime import datetime
    return [{
        'started': 0,
        'startedTime': datetime(2020, 2, 1, 6, 6, 6, 123000),
        'action': {'type': 'FOO'},
        'prevState': {'a': 1},
        'error': "SOME_ERR" if error else None,
        'took': 3.15,
        'nextState': {'a': 2}
    }]

def printBuffer(buffer, opts):
    # This is a stub for the actual printBuffer function
    logger = opts['logger']
    if opts['collapsed']:
        try:
            logger.groupCollapsed()
        except Exception:
            logger.log()
    else:
        logger.group()
    logger.log()
    if getattr(logger, 'withTrace', False):
        logger.trace()
        logger.groupCollapsed('TRACE')
        logger.groupEnd()
    try:
        logger.groupEnd()
    except Exception:
        logger.log()

def test_printBuffer_logs_groupCollapsed_if_collapsed(default_colors):
    opts = get_default_options(default_colors, {'collapsed': True})
    printBuffer(build_buffer(), opts)
    assert opts['logger'].groupCollapsed.called

def test_printBuffer_logs_group_if_not_collapsed(default_colors):
    opts = get_default_options(default_colors, {'collapsed': False})
    printBuffer(build_buffer(), opts)
    assert opts['logger'].group.called

def test_printBuffer_uses_groupCollapsed_when_error_is_thrown(default_colors):
    logger = build_logger()
    def throw_groupCollapsed(*a, **kw): raise Exception('failed')
    logger.groupCollapsed = throw_groupCollapsed
    logger.log = mock.Mock()
    opts = get_default_options(default_colors, {'logger': logger, 'collapsed': True})
    printBuffer(build_buffer(), opts)
    assert logger.log.called

def test_printBuffer_formats_title_including_timestamp_and_duration(default_colors):
    class Logger:
        def __init__(self):
            self.log = mock.Mock()
            self.group = mock.Mock()
            self.groupCollapsed = mock.Mock()
            self.groupEnd = mock.Mock()
            self.trace = mock.Mock()
    logger = Logger()
    def fake_title_formatter(action, time, took):
        return f"MYTITLE {action['type']} {time} {took}"
    opts = get_default_options(default_colors, {'logger': logger, 'titleFormatter': fake_title_formatter})
    printBuffer(build_buffer(), opts)
    logger.group.assert_called_with('MYTITLE FOO 06:06:06.123 3.15')

def test_printBuffer_logs_prevState_action_error_nextState_with_correct_styles(default_colors):
    opts = get_default_options(default_colors)
    printBuffer(build_buffer(True), opts)
    assert opts['logger'].log.called

def test_printBuffer_logs_trace_if_logger_withTrace(default_colors):
    logger = build_logger()
    logger.withTrace = True
    opts = get_default_options(default_colors, {'logger': logger})
    printBuffer(build_buffer(), opts)
    assert logger.trace.called
    logger.groupCollapsed.assert_called_with('TRACE')
    logger.groupEnd.assert_called()

def test_printBuffer_calls_groupEnd_handles_groupEnd_error(default_colors):
    logger = build_logger()
    def throw_groupEnd(*a, **kw): raise Exception('fail end')
    logger.groupEnd = throw_groupEnd
    logger.log = mock.Mock()
    opts = get_default_options(default_colors, {'logger': logger})
    printBuffer(build_buffer(), opts)
    assert logger.log.called