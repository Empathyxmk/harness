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
        return DummyLogger.getInstance()

def test_public_throughput_different_loop():
    logger = get_logger()
    cnt = 10
    for i in range(cnt):
        logger.info(f"Public throughput message #{i}")