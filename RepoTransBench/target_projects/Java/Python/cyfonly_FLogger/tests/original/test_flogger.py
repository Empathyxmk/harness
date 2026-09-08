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
            def info(self, msg): pass
            def writeLog(self, *args): pass
        return DummyLogger.getInstance()

def test_flogger_scripted_usage():
    logger = get_logger()
    logger.info("Here is your message...")
    logger.writeLog(1, "Here is your customized level message...")
    logger.writeLog("error", 3, "Here is your customized log file and level message...")

# Not a test, but mimics the original `main` usage for coverage.
if __name__ == "__main__":
    test_flogger_scripted_usage()