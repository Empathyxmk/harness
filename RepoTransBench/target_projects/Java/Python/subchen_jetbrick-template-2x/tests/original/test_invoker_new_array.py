from tests.original.common import AbstractJetxTest

class TestInvokeNewArray(AbstractJetxTest):

    def test(self):
        assert self.eval("${new int[1]}").startswith("[I")
        assert self.eval("${new String[1][2]}").startswith("[[Ljava.lang.String;")