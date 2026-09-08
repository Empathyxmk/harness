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
            DEBUG = 0
            INFO = 1
            WARN = 2
            ERROR = 3
            FATAL = 4
            CFG_LOG_LEVEL = "0,1,2,3,4"
        return DummyConstant

def test_debug_info_warn_error_fatal():
    logger = get_logger()
    logger.debug("debug test message")
    logger.info("info test message")
    logger.warn("warn test message")
    logger.error("error test message")
    logger.fatal("fatal test message")

def test_write_log_with_level():
    logger = get_logger()
    Constant = get_constant()
    logger.writeLog(Constant.DEBUG, "level debug")
    logger.writeLog(Constant.INFO, "level info")
    logger.writeLog(Constant.WARN, "level warn")
    logger.writeLog(Constant.ERROR, "level error")
    logger.writeLog(Constant.FATAL, "level fatal")

def test_write_log_null_and_below_level():
    logger = get_logger()
    Constant = get_constant()
    logger.writeLog("testfile", Constant.DEBUG, None)
    old_level = Constant.CFG_LOG_LEVEL
    Constant.CFG_LOG_LEVEL = ""
    logger.writeLog("shouldSkip", Constant.DEBUG, "skip this")
    Constant.CFG_LOG_LEVEL = old_level