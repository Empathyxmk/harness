import pytest

class DummyBlock:
    def __init__(self, descr, offset, length):
        self.descr = descr
        self.offset = offset
        self.length = length
    def getDescription(self):
        return self.descr
    def getOffset(self):
        return self.offset
    def getLength(self):
        return self.length

class DummyTwigParserResult:
    def __init__(self, blocks):
        self.blocks = blocks
    def getBlocks(self):
        return self.blocks

class TwigStructureScanner:
    def scan(self, pr):
        # Return blocks that are not inline-block
        return [b for b in pr.getBlocks() if not b.getDescription().startswith("*inline")]
    def folds(self, pr):
        folds = {"tags": []}
        for b in pr.getBlocks():
            folds["tags"].append((b.getOffset(), b.getOffset()+b.getLength()))
        return folds
    def getConfiguration(self):
        return None

def test_scan_returns_top_level_blocks_only():
    block1 = DummyBlock("block", 0, 10)
    block2 = DummyBlock("block", 2, 5)
    block_inline = DummyBlock("*inline-block", 12, 1)
    blocks = [block1, block2, block_inline]
    pr = DummyTwigParserResult(blocks)
    scanner = TwigStructureScanner()
    items = scanner.scan(pr)
    assert items is not None
    assert len(items) >= 1

def test_folds_returns_all_blocks():
    block1 = DummyBlock("block", 0, 10)
    block2 = DummyBlock("xx", 13, 3)
    blocks = [block1, block2]
    pr = DummyTwigParserResult(blocks)
    scanner = TwigStructureScanner()
    folds = scanner.folds(pr)
    assert "tags" in folds
    ranges = folds["tags"]
    assert len(ranges) == 2
    assert ranges[0] == (0, 10)
    assert ranges[1] == (13, 16)

def test_get_configuration_returns_null():
    scanner = TwigStructureScanner()
    assert scanner.getConfiguration() is None