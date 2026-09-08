import pytest

class StringDest:
    def __init__(self):
        self.contents = b''
    def close(self):
        pass
    def flush(self):
        pass
    def sync(self):
        pass
    def append(self, data):
        self.contents += data

class StringSource:
    def __init__(self):
        self.contents = b''
        self.force_error = False
        self.returned_partial = False
    def read(self, n):
        assert not self.returned_partial
        if self.force_error:
            self.force_error = False
            self.returned_partial = True
            raise IOError("read error")
        if len(self.contents) < n:
            n = len(self.contents)
            self.returned_partial = True
        result = self.contents[:n]
        self.contents = self.contents[n:]
        return result
    def skip(self, n):
        if n > len(self.contents):
            self.contents = b''
            raise IOError("skipped past end")
        self.contents = self.contents[n:]

class ReportCollector:
    def __init__(self):
        self.dropped_bytes = 0
        self.message = ""
    def corruption(self, bytes_, status):
        self.dropped_bytes += bytes_
        self.message += str(status)

class LogTest:
    def __init__(self):
        self.dest = StringDest()
        self.source = StringSource()
        self.report = ReportCollector()
        self.reading = False
        self.writer = []
        self.records = []
        self.read_index = 0
    def write(self, msg):
        assert not self.reading
        self.writer.append(msg)
        self.dest.append(msg.encode())
        self.records.append(msg)
    def read(self):
        self.reading = True
        if self.read_index < len(self.records):
            record = self.records[self.read_index]
            self.read_index += 1
            return record
        else:
            return "EOF"

def test_log_empty():
    log = LogTest()
    assert log.read() == "EOF"

def test_log_read_write():
    log = LogTest()
    log.write("foo")
    log.write("bar")
    log.write("")
    log.write("xxxx")
    assert log.read() == "foo"
    assert log.read() == "bar"
    assert log.read() == ""
    assert log.read() == "xxxx"
    assert log.read() == "EOF"

def test_log_many_blocks():
    log = LogTest()
    for i in range(100):
        log.write(str(i))
    for i in range(100):
        assert log.read() == str(i)
    assert log.read() == "EOF"

def test_log_fragmentation():
    log = LogTest()
    log.write("small")
    log.write("medium" * 5)
    log.write("large" * 20)
    assert log.read() == "small"
    assert log.read() == "mediummediummediummediummedium"
    assert log.read() == "largelargelargelargelargelargelargelargelargelargelargelargelargelargelargelargelargelarge"
    assert log.read() == "EOF"

def test_log_open_for_append():
    log = LogTest()
    log.write("hello")
    log.write("world")
    assert log.read() == "hello"
    assert log.read() == "world"
    assert log.read() == "EOF"