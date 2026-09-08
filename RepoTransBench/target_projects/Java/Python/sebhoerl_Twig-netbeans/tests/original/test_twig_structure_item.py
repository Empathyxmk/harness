import pytest

class DummyBlock:
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

class HtmlFormatter:
    def __init__(self):
        self.sb = ""
    def name(self, name, main):
        self.sb += name
    def parameters(self, parameters):
        self.sb += parameters
    def appendText(self, text):
        self.sb += text
    def getText(self):
        return self.sb
    def active(self, start):
        pass
    def reset(self):
        self.sb = ""

class TwigStructureItem:
    def __init__(self, _parent, block, children):
        self._parent = _parent
        self.block = block
        self.children = children
    def getName(self):
        return self.block.getDescription()
    def getKind(self):
        return "METHOD"
    def isLeaf(self):
        return False
    def getOffsetRange(self):
        return (self.block.getOffset(), self.block.getOffset() + self.block.getLength())
    def getHtml(self, formatter):
        formatter.name(self.getName(), True)
        return formatter.getText()
    def getNestedItems(self):
        return self.children
    def getCustomIcon(self):
        return None
    def getSortText(self):
        return None
    def getPosition(self):
        return None

def test_twig_structure_item_methods():
    block = DummyBlock("block", 1, 10)
    blocks = [block]
    item = TwigStructureItem(None, block, blocks)
    assert item.getName() == "block"
    assert item.getKind() == "METHOD"
    assert not item.isLeaf()
    assert item.getOffsetRange() is not None
    formatter = HtmlFormatter()
    assert item.getHtml(formatter) == "block"
    assert item.getNestedItems() is blocks
    assert item.getCustomIcon() is None
    assert item.getSortText() is None
    assert item.getPosition() is None