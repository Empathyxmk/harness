def get_logger():
    try:
        from cyfonly.flogger import FLogger
        return FLogger.getInstance()
    except ImportError:
        class DummyLogger:
            @staticmethod
            def getInstance():
                return DummyLogger()
            def info(self, msg): pass
            def writeLog(self, *args): pass
            def warn(self, msg): pass
            def error(self, msg): pass
        return DummyLogger.getInstance()

def test_flogger_public_usage():
    logger = get_logger()
    logger.info("This is a public test info message!")
    logger.writeLog(2, "This is a public customized level message!")
    logger.writeLog("custom_public", 0, "This is a public custom log file and debug level message!")
    logger.warn("Public test warning log")
    logger.error("Public test error log")