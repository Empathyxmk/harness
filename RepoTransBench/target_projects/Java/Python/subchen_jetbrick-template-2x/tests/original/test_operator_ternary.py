from tests.original.common import AbstractJetxTest

class TestTernaryOperator(AbstractJetxTest):

    def test_basic(self):
        assert self.eval("${true?1:0}") == "1"
        assert self.eval("${false?1:0}") == "0"
        assert self.eval("${false?1:true?2:3}") == "2"
        assert self.eval("${true?false?1:2:3}") == "2"

    def test_simplify(self):
        assert self.eval("${null?:1}") == "1"
        assert self.eval("${'A'?:2}") == "A"
        assert self.eval("${a?:b?:9}") == "9"