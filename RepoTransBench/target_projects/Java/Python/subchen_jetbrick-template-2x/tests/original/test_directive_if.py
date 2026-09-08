from tests.original.common import AbstractJetxTest

class TestDirectiveIf(AbstractJetxTest):

    def test_if(self):
        assert self.eval("#if(true)a#end") == "a"
        assert self.eval("#if(false)a#end") == ""

    def test_elseif(self):
        assert self.eval("#set(i=1)#if(i==0)0#elseif(i==1)1#elseif(i==2)2#end") == "1"
        assert self.eval("#set(i=3)#if(i==0)0#elseif(i==1)1#else()9#end") == "9"

    def test_else(self):
        assert self.eval("#if(true)a#else()b#end") == "a"
        assert self.eval("#if(false)a#else()b#end") == "b"