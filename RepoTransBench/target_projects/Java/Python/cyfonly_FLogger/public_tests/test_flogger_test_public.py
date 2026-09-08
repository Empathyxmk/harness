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
            def warn(self, msg): pass
        return DummyLogger.getInstance()

def test_logger_info_and_warn_public():
    logger = get_logger()
    logger.info("Public INFO message for FLoggerTestPublic")
    logger.warn("Public WARN message for FLoggerTestPublic")