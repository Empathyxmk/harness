from tests.original.common import AbstractJetxTest

class TestOptionLoadmacro(AbstractJetxTest):

    def test_include(self):
        s = "#options(loadmacro='/macros.jetx')#call size('abc')#call isOdd(123)"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        macro = "#macro size(String s)${s.length()}#end#macro isOdd(int n)${n % 2 == 1}#end"
        self.engine.set("/macros.jetx", macro)
        assert self.eval() == "3true"