import pytest

from tests.original.common import AbstractJetxTest

class TestDirectiveInvalid(AbstractJetxTest):

    def test_invalid_define(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#define")
        assert self.err(self.Errors.ARGUMENTS_MISSING) in str(e.value)

    def test_invalid_if(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#if")
        assert self.err(self.Errors.ARGUMENTS_MISSING) in str(e.value)

    def test_invalid_missing_end(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#if(true)123")
        assert "mismatched input '<EOF>'" in str(e.value) or "DIRECTIVE_END" in str(e.value)

    def test_invalid_break(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#break")
        assert "cannot be used outside of" in str(e.value)

    def test_invalid_continue(self):
        with pytest.raises(self.SyntaxException) as e:
            self.eval("#continue")
        assert "cannot be used outside of" in str(e.value)