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
            def fatal(self, msg): pass
            def writeLog(self, *args): pass
        return DummyLogger.getInstance()

def test_various_levels_public():
    logger = get_logger()
    logger.debug("Debugging - public core test!")
    logger.fatal("This is a public fatal log!")
    logger.writeLog("public_logfile", 2, "This is a public WARN log in a special file!")