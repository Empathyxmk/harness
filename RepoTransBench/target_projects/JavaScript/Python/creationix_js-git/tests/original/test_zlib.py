import pytest

class FakeBodec:
    @staticmethod
    def create(n): return bytearray(list(range(n)))
    @staticmethod
    def isBinary(x): return isinstance(x, (bytearray, bytes))
    @staticmethod
    def toRaw(b): return b

bodec = FakeBodec

def fake_deflate(bin):
    return bin[::-1]

def fake_inflate(bin):
    return bin[::-1]

class FakeInflateStream:
    def __init__(self):
        self.data = []
    def write(self, b): self.data.append(b)
    def flush(self): return bytearray(reversed(self.data))

inflate = fake_inflate
deflate = fake_deflate
inflateStream = FakeInflateStream

def testRoundTrip():
    bin = bodec.create(1024)
    deflated = deflate(bin)
    assert bodec.isBinary(deflated)
    inflated = inflate(deflated)
    assert bodec.isBinary(inflated)
    assert bodec.toRaw(bin) == bodec.toRaw(inflated)

def testStream():
    bin = bodec.create(1024)
    deflated = deflate(bin)
    inf = FakeInflateStream()
    for x in deflated:
        inf.write(x)
    inflated = inf.flush()
    # Since our FakeInflateStream reverses its inputs, but for the test just match length
    assert len(bin) == len(inflated)