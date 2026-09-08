import pytest

from tests.original.common import AbstractJetxTest

class TestOptionStrict(AbstractJetxTest):

    def test_ok(self):
        self.eval("#options(strict=false)${a}")

    def test_fail(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#options(strict=true)${a}")
        assert self.err(self.Errors.VARIABLE_UNDEFINED) in str(e.value)