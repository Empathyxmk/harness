import pytest

class TwigTopTokenId:
    _values = ["TWIG_CONTENT", "TWIG_TAG", "TWIG_VARIABLE"]
    @staticmethod
    def values():
        # Mimic Java-style enum values as class instances with name field
        class EnumObj:
            def __init__(self, name): self._name = name
            def name(self): return self._name
        return [EnumObj(name) for name in TwigTopTokenId._values]
    @staticmethod
    def valueOf(name):
        for enum in TwigTopTokenId.values():
            if enum.name() == name:
                return enum
        raise ValueError("Not found: " + name)

def test_token_id_of_content():
    values = TwigTopTokenId.values()
    found = False
    for id in values:
        if id.name() == "TWIG_CONTENT":
            found = True
            break
    assert len(values) > 0
    assert found

def test_value_of_with_all_enums():
    for id in TwigTopTokenId.values():
        assert id == TwigTopTokenId.valueOf(id.name())