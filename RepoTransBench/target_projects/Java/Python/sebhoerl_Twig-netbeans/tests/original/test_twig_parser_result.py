import pytest

class Block:
    def __init__(self, desc, offset, length):
        self.desc = desc
        self.offset = offset
        self.length = length
    def getDescription(self):
        return self.desc
    def getOffset(self):
        return self.offset
    def getLength(self):
        return self.length

class TwigParserResult:
    def __init__(self, snap):
        self.snap = snap
        self.blocks = []
    def getBlocks(self):
        return self.blocks

class DummyBlock(Block):
    pass

def test_construct_and_get_blocks():
    snap = None
    res = TwigParserResult(snap)
    assert res.getBlocks() is not None
    b = DummyBlock("block", 0, 5)
    res.getBlocks().append(b)
    assert b in res.getBlocks()

def test_block_methods():
    b = DummyBlock("desc", 42, 7)
    assert b.getDescription() == "desc"
    assert b.getOffset() == 42
    assert b.getLength() == 7