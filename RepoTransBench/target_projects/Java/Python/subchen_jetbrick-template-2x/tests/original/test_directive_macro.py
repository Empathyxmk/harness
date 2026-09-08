import pytest

from tests.original.common import AbstractJetxTest

class TestDirectiveMacro(AbstractJetxTest):

    def test_defination(self):
        sb = "#macro size(String s)${s}, ${x}#end"
        self.eval(sb)

    def test_redefination(self):
        with pytest.raises(self.SyntaxException) as e:
            sb = "#macro size()#end#macro size(int a)#end"
            self.eval(sb)
        assert self.err(self.Errors.DIRECTIVE_MACRO_NAME_DUPLICATED) in str(e.value)

    def test_embed(self):
        sb = "#macro size(String s)size=${s.length()}#end#call size('abc')"
        assert self.eval(sb) == "size=3"