from tests.original.common import AbstractJetxTest

class TestOptionTrimLeadingWhitespaces(AbstractJetxTest):

    def test(self):
        assert self.eval("#options(trimLeadingWhitespaces=true)") == ""
        assert self.eval("#options(trimLeadingWhitespaces=true)\r\n") == ""
        assert self.eval("#options(trimLeadingWhitespaces=true)\r\nabc\n") == "abc\n"