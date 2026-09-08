import pytest

from tests.original.common import AbstractJetxTest

class TestOptionSafecall(AbstractJetxTest):

    def test_ok(self):
        self.eval("#options(safecall=true)${a.toString()}")

    def test_fail(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("#options(safecall=false)${a.toString()}")
        assert self.Errors.EXPRESSION_OBJECT_IS_NULL in str(e.value)