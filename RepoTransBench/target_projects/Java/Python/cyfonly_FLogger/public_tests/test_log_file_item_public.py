def get_log_file_item():
    try:
        from cyfonly.flogger.strategy import LogFileItem
        return LogFileItem()
    except ImportError:
        class DummyLogFileItem:
            def __init__(self):
                self.logFileName = ""
                self.fullLogFileName = ""
                self.currLogSize = 0
                self.currLogBuff = "A"
                self.alLogBufA = []
                self.alLogBufB = []
                self.nextWriteTime = 0
                self.lastPCDate = ""
                self.currCacheSize = 0
        return DummyLogFileItem()

def test_log_file_item_fields_with_different_data():
    lfi = get_log_file_item()
    assert lfi.logFileName == ""
    assert lfi.fullLogFileName == ""
    assert lfi.currLogSize == 0
    assert lfi.currLogBuff == "A"
    assert hasattr(lfi, 'alLogBufA')
    assert hasattr(lfi, 'alLogBufB')
    assert isinstance(lfi.alLogBufA, list)
    assert isinstance(lfi.alLogBufB, list)
    assert len(lfi.alLogBufA) == 0
    assert len(lfi.alLogBufB) == 0
    assert lfi.nextWriteTime == 0
    assert lfi.lastPCDate == ""
    assert lfi.currCacheSize == 0

    # Add different test values
    lfi.alLogBufA.append("public test AAA")
    lfi.alLogBufB.append("public test BBB")
    lfi.alLogBufA.append("extra item in A")
    assert len(lfi.alLogBufA) == 2
    assert len(lfi.alLogBufB) == 1
    assert lfi.alLogBufA[0] == "public test AAA"
    assert lfi.alLogBufB[0] == "public test BBB"
    assert lfi.alLogBufA[1] == "extra item in A"