from tests.original.common import AbstractJetxTest

class TestEqualsOperator(AbstractJetxTest):

    def test_true(self):
        assert self.eval("${(true)?1:0}") == "1"
        assert self.eval("${(false)?1:0}") == "0"
        assert self.eval("${(null)?1:0}") == "0"
        assert self.eval("${(1)?1:0}") == "1"
        assert self.eval("${(0)?1:0}") == "0"
        assert self.eval("${(1.0D)?1:0}") == "1"
        assert self.eval("${(0.0F)?1:0}") == "0"
        assert self.eval("${('a')?1:0}") == "1"
        assert self.eval("${([])?1:0}") == "0"
        assert self.eval("${({})?1:0}") == "0"
        assert self.eval("${(a)?1:0}") == "0"

    def test_compare(self):
        assert self.eval("${(0==0)?1:0}") == "1"
        assert self.eval("${(0D==0.0F)?1:0}") == "1"
        assert self.eval("${(0D==0L)?1:0}") == "1"
        assert self.eval("${(1!=0)?1:0}") == "1"
        assert self.eval("${(1>0d)?1:0}") == "1"
        assert self.eval("${(1>=1)?1:0}") == "1"
        assert self.eval("${(1f>=0)?1:0}") == "1"
        assert self.eval("${(0<1)?1:0}") == "1"
        assert self.eval("${(0<=1)?1:0}") == "1"
        assert self.eval("${(0<=0)?1:0}") == "1"

    def test_comparable(self):
        assert self.eval("${'b' > 'a'}") == "true"
        assert self.eval("${'a' < 'b'}") == "true"
        assert self.eval("${'b' >= 'a'}") == "true"
        assert self.eval("${'a' >= 'a'}") == "true"
        assert self.eval("${'a' <= 'b'}") == "true"
        assert self.eval("${'a' <= 'a'}") == "true"

    def test_equals(self):
        assert self.eval("${null==null}") == "true"
        assert self.eval("${1==null}") == "false"
        assert self.eval("${null==1}") == "false"

    def test_identically_equals(self):
        assert self.eval("${null===null}") == "true"
        assert self.eval("${'a'==='a'}") == "false"
        assert self.eval("${1===1L}") == "false"

    def test_and_or_not(self):
        assert self.eval("${!true}") == "false"
        assert self.eval("${!false}") == "true"
        assert self.eval("${true && true}") == "true"
        assert self.eval("${true && false}") == "false"
        assert self.eval("${false && false}") == "false"
        assert self.eval("${true || true}") == "true"
        assert self.eval("${true || false}") == "true"
        assert self.eval("${false || false}") == "false"

    def test_and_or_quick_path(self):
        assert self.eval("${false && [].get(0)}") == "false"
        assert self.eval("${true || [].get(0)}") == "true"