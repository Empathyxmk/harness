import threading

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

def test_flogger_throughput_benchmark():
    logger = get_logger()
    record_400_byte = (
        "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
        "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
        "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
        "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
    )
    count = 1000
    thread_num = 1

    # This is highly reduced from Java's mega-benchmark to keep test lightweight
    message_count = [0]

    def worker():
        for _ in range(count):
            logger.info(record_400_byte)
            message_count[0] += 1

    threads = [threading.Thread(target=worker) for _ in range(thread_num)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert message_count[0] == count * thread_num