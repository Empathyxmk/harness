from tests.original.common import AbstractJetxTest

class Tags:
    @staticmethod
    def body(ctx):
        ctx.invoke()

class TestTrimDirectiveWhitespaces(AbstractJetxTest):

    def test_basic1(self):
        sb = (
            "#for(int i:range(1,10))\n"
            "    #if(for.odd)  \n"
            "${i}\n"
            "    #end\n"
            "#end"
        )
        assert self.eval(sb) == "1\n3\n5\n7\n9\n"

    def test_basic2(self):
        sb = (
            "#for(int i:range(1,10))\n"
            "    #if(for.odd)  \n"
            " ${i}\n"
            "    #end\n"
            "#end"
        )
        assert self.eval(sb) == " 1\n 3\n 5\n 7\n 9\n"

    def test_inline1(self):
        sb = "===\nOK=#if(true)OK#end  \n==="
        assert self.eval(sb) == "===\nOK=OK\n==="

    def test_inline2(self):
        sb = "===\n#if(true)OK#end  \n==="
        assert self.eval(sb) == "===\nOK\n==="

    def test_inline3(self):
        sb = "===\n#if(true)OK#end X \n==="
        assert self.eval(sb) == "===\nOK X \n==="

    def test_inline4(self):
        sb = "#for(int i: range(0,3))${i}#end\n#for(int i: range(0,3))${i}#end\n"
        assert self.eval(sb) == "0123\n0123\n"

    def test_macro_call(self):
        sb = "#macro hello()\nhello\n#end\n#call hello()\n#call hello()\n"
        assert self.eval(sb) == "hello\nhello\n"

    def test_include_call(self):
        s = "#include('/sub.jetx')\n#include('/sub.jetx')\n"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "123")
        assert self.eval() == "123\n123\n"

    def test_tag_call(self):
        self.engine.get_global_resolver().register_tags(Tags)
        sb = "#tag body()\n123\n#end\n#tag body()\n123\n#end\n"
        assert self.eval(sb) == "123\n123\n"