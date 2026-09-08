from tests.original.common import AbstractJetxTest

class StrUtils:
    @staticmethod
    def link(title, url, *attributes):
        return f'<a href="{url}">{title}</a>'

class TestInvokeMethodExtension(AbstractJetxTest):

    def initialize_engine(self):
        self.engine.get_global_resolver().register_methods(self.StringUtils)
        self.engine.get_global_resolver().register_methods(StrUtils)
        self.engine.get_global_resolver().register_methods(str)

    def test(self):
        assert self.eval("${' 123 '.trim()}") == "123"
        assert self.eval("${'0'.repeat(3)}") == "000"
        assert self.eval("${'?'.repeat(',', 3)}") == "?,?,?"

    def test_varargs(self):
        assert self.eval("${''.format()}") == ""
        assert self.eval("${'%s'.format(1)}") == "1"
        assert self.eval("${'%s%s'.format(1,2)}") == "12"
        assert self.eval("${'%s%s%s'.format(1,2,3)}") == "123"

    def test_varargs_issue(self):
        assert self.eval("${'?'.link('#')}") == '<a href="#">?</a>'