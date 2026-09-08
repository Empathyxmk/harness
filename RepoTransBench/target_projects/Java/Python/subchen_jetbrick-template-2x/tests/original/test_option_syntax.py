import pytest

from tests.original.common import AbstractJetxTest

class TestOptionSyntax(AbstractJetxTest):

    def test_syntax(self):
        self.eval("#options(import='java.io.*')")
        self.eval("#options(strict=true, safecall=false, import='java.io.*', import='java.net.*')")

    def test_invalid_name(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#options(unknown=true)")
        assert self.err(self.Errors.OPTION_NAME_INVALID) in str(e.value)

    def test_invalid_value(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#options(strict=123)")
        assert self.err(self.Errors.OPTION_VALUE_INVALID) in str(e.value)