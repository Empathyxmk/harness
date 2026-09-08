from tests.original.common import AbstractJetxTest

class TestBinaryOperator(AbstractJetxTest):

    def test_plus(self):
        assert self.eval("${1+2}") == "3"
        assert self.eval("${1+2L}") == "3"
        assert self.eval("${1+2.1f}") == "3.1"
        assert self.eval("${1+2.1d}") == "3.1"

    def test_minus(self):
        assert self.eval("${2-1}") == "1"
        assert self.eval("${2L-1}") == "1"
        assert self.eval("${2-1.1f}") == "0.9"
        assert self.eval("${2-1.1f}") == "0.9"

    def test_mul(self):
        assert self.eval("${2*3}") == "6"
        assert self.eval("${2*3L}") == "6"
        assert self.eval("${2*3.1f}") == "6.2"
        assert self.eval("${2*3.1d}") == "6.2"

    def test_div(self):
        assert self.eval("${6/4}") == "1"
        assert self.eval("${6/4L}") == "1"
        assert self.eval("${6/4f}") == "1.5"
        assert self.eval("${6/4d}") == "1.5"

    def test_mod(self):
        assert self.eval("${3%2}") == "1"
        assert self.eval("${3%2L}") == "1"
        assert self.eval("${3%2f}") == "1.0"
        assert self.eval("${3%2d}") == "1.0"

    def test_arithmetic(self):
        assert self.eval("${1+2*3.1}") == "7.2"
        assert self.eval("${1.1+1.1}") == "2.2"
        assert self.eval("${1+2*(3-4)*5.6}") == "-10.2"

    def test_string_add(self):
        assert self.eval("${'a'+1}") == "a1"
        assert self.eval("${1+'a'}") == "1a"
        assert self.eval("${'1'+'2'}") == "12"
        assert self.eval("${'a'+null}") == "a"
        assert self.eval("${null+'a'}") == "a"

    def test_instanceof(self):
        assert self.eval("${'a' instanceof String}") == "true"
        assert self.eval("${1 instanceof Number}") == "true"
        assert self.eval("${'a' instanceof Number}") == "false"

    def test_null_as_default(self):
        assert self.eval("${a ?! 0}") == "0"
        assert self.eval("${a.b.c ?! 0}") == "0"
        assert self.eval("${a.b() ?! 0}") == "0"
        assert self.eval("${a[0] ?! 0}") == "0"