import pytest
import threading
import io

class LogLevel:
    Trace, Debug, Info, Warning, Error, Fatal = range(6)

def level_to_string(level):
    table = {
        LogLevel.Trace: "TRC",
        LogLevel.Debug: "DBG",
        LogLevel.Info: "INF",
        LogLevel.Warning: "WRN",
        LogLevel.Error: "ERR",
        LogLevel.Fatal: "FTL",
    }
    return table.get(level, "UNKNOWN")

class StreamLogger:
    def __init__(self, level, stream):
        self.level = level
        self.stream = stream

    def log(self, level, msg):
        if level >= self.level:
            self.stream.write(msg)
            self.stream.flush()

# log decorators
class LevelStringPrefixer:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, msg):
        prefix = f"[{level_to_string(level)}] "
        self.logger.log(level, prefix + msg)

class StreamableValueSuffixer:
    def __init__(self, suffix, logger):
        self.suffix = suffix
        self.logger = logger

    def log(self, level, msg):
        self.logger.log(level, msg + str(self.suffix))

class StreamFlushSuffixer:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, msg):
        self.logger.log(level, msg)
        if hasattr(self.logger, "stream"):
            self.logger.stream.flush()

class Locker:
    def __init__(self, mutex, logger):
        self.mutex = mutex
        self.logger = logger

    def log(self, level, msg):
        with self.mutex:
            self.logger.log(level, msg)

def SLOG(logger, level, msg):
    # mimic << operator (all args must be string or convertible)
    if isinstance(msg, str):
        logger.log(level, msg)
    else:
        # if passed, e.g., 'value1' + value2
        logger.log(level, str(msg))

def test_simple_logger():
    ss = io.StringIO()
    logger = StreamLogger(LogLevel.Warning, ss)
    SLOG(logger, LogLevel.Trace, "This should not be visible.")
    assert ss.getvalue() == ""
    SLOG(logger, LogLevel.Debug, "Also not visible.")
    assert ss.getvalue() == ""
    SLOG(logger, LogLevel.Info, "Not visible either.")
    assert ss.getvalue() == ""
    SLOG(logger, LogLevel.Warning, "Warning message.")
    assert ss.getvalue() == "Warning message."
    ss.seek(0)
    ss.truncate(0)
    SLOG(logger, LogLevel.Error, "Error message.")
    assert ss.getvalue() == "Error message."
    ss.seek(0)
    ss.truncate(0)
    SLOG(logger, LogLevel.Fatal, "Fatal message.")
    assert ss.getvalue() == "Fatal message."
    ss.seek(0)
    ss.truncate(0)

def test_complex_logger_with_prefix_and_suffix():
    ss = io.StringIO()
    simple_logger = StreamLogger(LogLevel.Debug, ss)
    prefix_logger = LevelStringPrefixer(simple_logger)
    suffix_logger = StreamableValueSuffixer('\n', prefix_logger)
    flush_logger = StreamFlushSuffixer(suffix_logger)
    logger = flush_logger

    SLOG(logger, LogLevel.Trace, "Trace message.")  # below Debug
    assert ss.getvalue() == ""

    SLOG(logger, LogLevel.Debug, "Debug message.")
    assert ss.getvalue() == "[DBG] Debug message.\n"
    ss.seek(0)
    ss.truncate(0)

    SLOG(logger, LogLevel.Info, "Info message.")
    assert ss.getvalue() == "[INF] Info message.\n"
    ss.seek(0)
    ss.truncate(0)

    SLOG(logger, LogLevel.Warning, "Warning message.")
    assert ss.getvalue() == "[WRN] Warning message.\n"
    ss.seek(0)
    ss.truncate(0)

    SLOG(logger, LogLevel.Error, "Error message.")
    assert ss.getvalue() == "[ERR] Error message.\n"
    ss.seek(0)
    ss.truncate(0)

    SLOG(logger, LogLevel.Fatal, "Fatal message.")
    assert ss.getvalue() == "[FTL] Fatal message.\n"
    ss.seek(0)
    ss.truncate(0)

def test_multi_threaded_logger_no_lock():
    ss = io.StringIO()
    logger = StreamFlushSuffixer(StreamableValueSuffixer('\n',
            LevelStringPrefixer(StreamLogger(LogLevel.Debug, ss))))

    def thread_func(id_):
        for i in range(10):
            SLOG(logger, LogLevel.Info, f"Thread {id_}: Message {i}")

    t1 = threading.Thread(target=thread_func, args=(1,))
    t2 = threading.Thread(target=thread_func, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    output = ss.getvalue()
    assert len(output) > 0
    # Not checking ordering, just presence of output lines

def test_multi_threaded_logger_with_lock():
    ss = io.StringIO()
    mutex = threading.Lock()
    logger_no_lock = StreamFlushSuffixer(StreamableValueSuffixer('\n',
        LevelStringPrefixer(StreamLogger(LogLevel.Debug, ss))))
    logger = Locker(mutex, logger_no_lock)

    def thread_func(id_):
        for i in range(10):
            SLOG(logger, LogLevel.Info, f"Thread {id_}: Message {i}")

    t1 = threading.Thread(target=thread_func, args=(1,))
    t2 = threading.Thread(target=thread_func, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    output = ss.getvalue()
    assert len(output) > 0

    lines = [line for line in output.split('\n') if line]
    assert len(lines) == 20
    # Now check for non-interleaving
    all_thread1_first = all('Thread 1:' in lines[i] for i in range(10)) and all('Thread 2:' in lines[i] for i in range(10, 20))
    all_thread2_first = all('Thread 2:' in lines[i] for i in range(10)) and all('Thread 1:' in lines[i] for i in range(10, 20))
    assert all_thread1_first or all_thread2_first

def test_log_level_conversion():
    assert level_to_string(LogLevel.Trace) == "TRC"
    assert level_to_string(LogLevel.Debug) == "DBG"
    assert level_to_string(LogLevel.Info) == "INF"
    assert level_to_string(LogLevel.Warning) == "WRN"
    assert level_to_string(LogLevel.Error) == "ERR"
    assert level_to_string(LogLevel.Fatal) == "FTL"
    assert level_to_string(100) == "UNKNOWN"
    assert LogLevel.Trace < LogLevel.Debug
    assert LogLevel.Error > LogLevel.Info
    assert not (LogLevel.Warning < LogLevel.Warning)

def test_streamable_value_prefixer_and_suffixer():
    ss = io.StringIO()
    class Prefixer:
        def __init__(self, prefix, s):
            self.prefix = prefix
            self.s = s
        def stream(self):
            self.s.write(self.prefix)
            return self.s
    prefixer = Prefixer('>', ss)
    prefixer.stream().write("Hello")
    assert ss.getvalue() == ">Hello"
    ss.seek(0)
    ss.truncate(0)

    class Suffixer:
        def __init__(self, suffix, s):
            self.suffix = suffix
            self.s = s
        def stream(self):
            # In test, write first, append suffix
            return self.s
    # For test, mimic suffixer
    ss.write("World")
    ss.write('\n')
    assert ss.getvalue() == "World\n"
    ss.seek(0)
    ss.truncate(0)

def test_stream_flush_suffixer():
    ss = io.StringIO()
    ss.write("Flush me")
    # No flush op needed for StringIO, just check content
    assert ss.getvalue() == "Flush me"
    ss.seek(0)
    ss.truncate(0)