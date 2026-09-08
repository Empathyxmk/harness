from tests.original.common import AbstractJetxTest

class TestInvokeFunction(AbstractJetxTest):

    def initialize_engine(self):
        self.engine.get_global_resolver().register_functions(self.StringUtils)

    def test(self):
        assert self.eval("${trim(' 123 ')}") == "123"
        assert self.eval("${repeat('0', 3)}") == "000"
        assert self.eval("${repeat('?', ',', 3)}") == "?,?,?"