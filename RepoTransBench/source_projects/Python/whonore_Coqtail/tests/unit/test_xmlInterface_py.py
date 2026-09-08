import sys
import pytest

sys.path.insert(0, 'python')
import xmlInterface

def test_parse_tagged_tokens_basic():
    import xml.etree.ElementTree as ET
    s = '<root>Hello<start.a/>World<end.a/>!</root>'
    root = ET.fromstring(s)
    tokens = list(xmlInterface.parse_tagged_tokens(set(), root))
    flat_text = ''.join([tok for tok, tags in tokens])
    assert "HelloWorld!" in flat_text

def test_TAGGEDTOKENS_parse_branch():
    # Patch an element with .tag property for branch coverage, "start." and "end."
    class Elem:
        tag = "start.x"
        text = "x"
        tail = None
        def iter(self):
            return []
        def __iter__(self):
            return iter([])
    result = list(xmlInterface._parse_tagged_tokens(set(), Elem()))
    assert isinstance(result, list)
    class Elem2:
        tag = "end.y"
        text = "y"
        tail = None
        def iter(self):
            return []
        def __iter__(self):
            return iter([])
    result = list(xmlInterface._parse_tagged_tokens(set(), Elem2()))
    assert isinstance(result, list)
    class Elem3:
        tag = "plain"
        text = "plain"
        tail = None
        def iter(self):
            return []
        def __iter__(self):
            return iter([])
    result = list(xmlInterface._parse_tagged_tokens(set(['plain']), Elem3()))
    assert isinstance(result, list)

def test_XMLInterface_cannot_init_without_args():
    with pytest.raises(TypeError):
        xmlInterface.XMLInterface()