from tests.original.common import AbstractJetxTest

class TestUnaryOperator(AbstractJetxTest):

    def test_basic(self):
        assert self.eval("${+2}") == "2"
        assert self.eval("${-2}") == "-2"
        assert self.eval("${+2.1}") == "2.1"
        assert self.eval("${-2.1}") == "-2.1"