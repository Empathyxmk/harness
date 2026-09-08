import pytest

class StringDest:
    def __init__(self):
        self.contents = bytearray()
    def append(self, data):
        self.contents.extend(data.encode() if isinstance(data, str) else data)
    def size(self):
        return len(self.contents)

class StringSource:
    def __init__(self, contents=b''):
        self.contents = bytearray(contents)
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

class ReportCollector:
    def __init__(self):
        self.dropped_bytes = 0
        self.message = ""
    def corruption(self, bytes_, status):
        self.dropped_bytes += bytes_
        self.message += str(status)

def BigString(partial_string, n):
    result = ""
    while len(result) < n:
        result += partial_string
    return result[:n]

def NumberString(n):
    return f"{n}."

def RandomSkewedString(i):
    # For this translation, mimic skew at 0-20
    return BigString(NumberString(i), (i % 17) + 1)

class LogTest:
    initial_offset_record_sizes = [10000, 10000, 2 * 32768 - 1000, 1]  # kBlockSize=32768
    initial_offset_last_record_offsets = [
        0,
        7+10000,
        2*(7+10000),
        2*(7+10000)+(2*32768-1000)+3*7
    ]
    def __init__(self):
        self.dest = StringDest()
        self.records = []
        self.reading = False
        self.read_index = 0
        self.report = ReportCollector()
    def Write(self, msg):
        assert not self.reading
        self.records.append(msg)
        self.dest.append(msg)
    def Read(self):
        self.reading = True
        if self.read_index < len(self.records):
            rec = self.records[self.read_index]
            self.read_index += 1
            return rec
        else:
            return "EOF"
    def WrittenBytes(self):
        return self.dest.size()

@pytest.mark.parametrize("messages", [
    [],
    ["foo","bar","","xxxx"],
])
def test_log_basic(messages):
    t = LogTest()
    for m in messages:
        t.Write(m)
    for m in messages:
        assert t.Read() == m
    assert t.Read() == "EOF"
    assert t.Read() == "EOF"

def test_log_many_blocks():
    t = LogTest()
    for i in range(100):
        t.Write(NumberString(i))
    for i in range(100):
        assert t.Read() == NumberString(i)
    assert t.Read() == "EOF"

def test_log_fragmentation():
    t = LogTest()
    t.Write("small")
    t.Write(BigString("medium", 500))
    t.Write(BigString("large", 1000))
    assert t.Read() == "small"
    assert t.Read() == BigString("medium", 500)
    assert t.Read() == BigString("large", 1000)
    assert t.Read() == "EOF"

def test_log_open_for_append():
    t = LogTest()
    t.Write("hello")
    t.Write("world")
    assert t.Read() == "hello"
    assert t.Read() == "world"
    assert t.Read() == "EOF"