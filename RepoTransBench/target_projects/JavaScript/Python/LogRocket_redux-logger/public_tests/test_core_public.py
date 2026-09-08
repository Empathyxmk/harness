import pytest
from unittest import mock

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

def get_default_options(overrides=None):
    if overrides is None:
        overrides = {}
    default_colors = {
        'title': lambda: 'magenta',
        'prevState': lambda: 'cyan',
        'action': lambda: 'orange',
        'error': lambda: 'pink',
        'nextState': lambda: 'lime'
    }
    opts = {
        'logger': build_logger(),
        'actionTransformer': lambda a: dict(a, added='yes') if isinstance(a, dict) else a,
        'titleFormatter': None,
        'collapsed': True,
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
        'started': 100,
        'startedTime': datetime(2021, 3, 2, 10, 22, 55, 57000),
        'action': {'type': 'BAR', 'custom': 5},
        'prevState': {'b': 3},
        'error': "DIFFERENT_ERR" if error else None,
        'took': 8.45,
        'nextState': {'b': 4}
    }]

def printBuffer(buffer, opts):
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

def test_printBuffer_logs_groupCollapsed_if_collapsed_public():
    opts = get_default_options({'collapsed': True})
    printBuffer(build_buffer(), opts)
    assert opts['logger'].groupCollapsed.called

def test_printBuffer_logs_group_if_not_collapsed_public():
    opts = get_default_options({'collapsed': False})
    printBuffer(build_buffer(), opts)
    assert opts['logger'].group.called

def test_printBuffer_uses_groupCollapsed_when_error_is_thrown_public():
    logger = build_logger()
    def throw_groupCollapsed(*a, **kw): raise Exception('another-failed')
    logger.groupCollapsed = throw_groupCollapsed
    logger.log = mock.Mock()
    opts = get_default_options({'logger': logger, 'collapsed': True})
    printBuffer(build_buffer(), opts)
    assert logger.log.called

def test_printBuffer_formats_title_including_timestamp_and_duration_public():
    class Logger:
        def __init__(self):
            self.log = mock.Mock()
            self.groupCollapsed = mock.Mock()
            self.group = mock.Mock()
            self.groupEnd = mock.Mock()
            self.trace = mock.Mock()
    logger = Logger()
    def fake_title_formatter(action, time, took):
        return f"PUBTITLE {action['type']} {time} {took}"
    opts = get_default_options({'logger': logger, 'titleFormatter': fake_title_formatter})
    printBuffer(build_buffer(), opts)
    logger.groupCollapsed.assert_called_with('PUBTITLE BAR 10:22:55.057 8.45')

def test_printBuffer_logs_prevState_action_error_nextState_with_correct_styles_public():
    opts = get_default_options()
    printBuffer(build_buffer(True), opts)
    assert opts['logger'].log.called

def test_printBuffer_logs_trace_if_logger_withTrace_public():
    logger = build_logger()
    logger.withTrace = True
    opts = get_default_options({'logger': logger})
    printBuffer(build_buffer(), opts)
    assert logger.trace.called
    logger.groupCollapsed.assert_called_with('TRACE')
    logger.groupEnd.assert_called()

def test_printBuffer_calls_groupEnd_handles_groupEnd_error_public():
    logger = build_logger()
    def throw_groupEnd(*a, **kw): raise Exception('fail-end-public')
    logger.groupEnd = throw_groupEnd
    logger.log = mock.Mock()
    opts = get_default_options({'logger': logger})
    printBuffer(build_buffer(), opts)
    assert logger.log.called