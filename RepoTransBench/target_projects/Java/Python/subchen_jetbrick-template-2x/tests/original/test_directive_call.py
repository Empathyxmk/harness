from tests.original.common import AbstractJetxTest

class TestDirectiveCall(AbstractJetxTest):

    def test(self):
        assert self.eval("#macro inc(int x)${x+1}#end#call inc(1)") == "2"