import io

class LogLevel:
    Trace, Debug, Info, Warning, Error, Fatal = range(6)

class StreamLogger:
    def __init__(self, level, stream):
        self.level = level
        self.stream = stream

    def log(self, level, msg):
        if level >= self.level:
            self.stream.write(str(msg))
            self.stream.flush()

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

class LevelStringPrefixer:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, msg):
        prefix = f"[{level_to_string(level)}] "
        self.logger.log(level, prefix + str(msg))

def SLOG(logger, level, msg):
    logger.log(level, msg)

def test_public_log_info():
    ss = io.StringIO()
    logger = StreamLogger(LogLevel.Info, ss)
    SLOG(logger, LogLevel.Info, "Public info log test " + str(2024))
    str_value = ss.getvalue()
    assert "Public info log test 2024" in str_value

def test_public_log_debug_prefix():
    ss = io.StringIO()
    logger = LevelStringPrefixer(StreamLogger(LogLevel.Debug, ss))
    SLOG(logger, LogLevel.Debug, "Different debug output " + str(-111))
    str_value = ss.getvalue()
    assert "Different debug output -111" in str_value

def test_public_no_output_for_low_level():
    ss = io.StringIO()
    logger = StreamLogger(LogLevel.Error, ss)
    SLOG(logger, LogLevel.Warning, "Should be shown")
    SLOG(logger, LogLevel.Trace, "Should NOT be shown (public)")
    str_value = ss.getvalue()
    # Only 'Should be shown' should appear
    assert "Should be shown" in str_value
    assert "Should NOT be shown (public)" not in str_value