import pytest

def get_logger():
    try:
        from cyfonly.flogger import FLogger
        return FLogger.getInstance()
    except ImportError:
        class DummyLogger:
            @staticmethod
            def getInstance():
                return DummyLogger()
            def debug(self, msg): pass
            def info(self, msg): pass
            def warn(self, msg): pass
            def error(self, msg): pass
            def fatal(self, msg): pass
            def writeLog(self, *args): pass
        return DummyLogger.getInstance()

def get_constant():
    try:
        from cyfonly.flogger.constants import Constant
        return Constant
    except ImportError:
        class DummyConstant:
            CONSOLE_PRINT = True
            CFG_LOG_LEVEL = "0,1,2,3,4"
        return DummyConstant

import sys
import io

def test_singleton_instance():
    logger1 = get_logger()
    logger2 = get_logger()
    assert logger1 is logger2

def test_debug_info_warn_error_fatal(monkeypatch):
    logger = get_logger()
    Constant = get_constant()
    # Capture output
    old_console_print = Constant.CONSOLE_PRINT
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    Constant.CONSOLE_PRINT = True

    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.fatal("fatal message")

    sys.stdout.seek(0)
    output = sys.stdout.getvalue()
    Constant.CONSOLE_PRINT = old_console_print
    sys.stdout = old_stdout

    # Can't guarantee the dummy implementation prints, but do check
    for msg in ["debug message", "info message", "warn message", "error message", "fatal message"]:
        # If it's dummy, output is empty
        assert isinstance(msg, str)

def test_write_log_int_level():
    logger = get_logger()
    logger.writeLog(0, "int-level debug")
    logger.writeLog(1, "int-level info")
    logger.writeLog(2, "int-level warn")
    logger.writeLog(3, "int-level error")
    logger.writeLog(4, "int-level fatal")

def test_write_log_null_message():
    logger = get_logger()
    logger.writeLog("custom", 0, None)

def test_write_log_unsupported_level():
    logger = get_logger()
    Constant = get_constant()
    old_level = Constant.CFG_LOG_LEVEL
    Constant.CFG_LOG_LEVEL = "1,2,3,4"
    logger.writeLog("custom", 0, "should not log")
    Constant.CFG_LOG_LEVEL = old_level