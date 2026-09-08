import pytest

from tests.original.common import AbstractJetxTest

class TestInvokeIndexGet(AbstractJetxTest):

    @classmethod
    def setup_class(cls):
        cls.ctx = {
            "index": 1,
            "key": "bb",
            "array": ["aa", 12],
            "list": ["aa", "bb"],
            "map": {"aa": "aa", "bb": 12}
        }

    def test_array(self):
        assert self.eval("${array[0]}", self.ctx) == "aa"
        assert self.eval("${array[index]}", self.ctx) == "12"

    def test_array_args_error(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${array['a']}", self.ctx)
        assert "undefined for the argument type(s)" in str(e.value)

    def test_list(self):
        assert self.eval("${list[0]}", self.ctx) == "aa"
        assert self.eval("${list[index]}", self.ctx) == "bb"

    def test_list_args_error(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${list['a']}", self.ctx)
        assert "undefined for the argument type(s)" in str(e.value)

    def test_map(self):
        assert self.eval("${map['aa']}", self.ctx) == "aa"
        assert self.eval("${map[key]}", self.ctx) == "12"

    def test_map_args_error(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("${map[1]}", self.ctx)
        assert "undefined for the argument type(s)" in str(e.value)