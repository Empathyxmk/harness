from tests.original.common import AbstractJetxTest

class TestDirectiveStop(AbstractJetxTest):

    def test_for_break(self):
        assert self.eval("#for(i:[1,2,3])${i}#break(i>1)a#end") == "1a2"

    def test_for_continue(self):
        assert self.eval("#for(i:[1,2,3])${i}#continue(i>1)a#end") == "1a23"

    def test_for_stop(self):
        assert self.eval("123#stop()abc") == "123"
        assert self.eval("#for(i:[1,2,3])${i}#stop(i>1)a#end()123") == "1a2"