from tests.original.common import AbstractJetxTest

class TestInconsistentClass(AbstractJetxTest):

    def test_include(self):
        s = "#for(int i:[0,1,2])${i}#end#include('/sub.jetx')"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "#for(int i:[0,1,2])${i}#end")
        assert self.eval() == "012012"