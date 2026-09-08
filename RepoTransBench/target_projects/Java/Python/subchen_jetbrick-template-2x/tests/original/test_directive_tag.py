import pytest

from tests.original.common import AbstractJetxTest

class Tags:
    @staticmethod
    def hello(ctx):
        ctx.get_writer().print_("hello")

    @staticmethod
    def hello_with_body(ctx):
        ctx.get_writer().print_("hello:" + ctx.get_body_content())

    @staticmethod
    def hello_with_param(ctx, name):
        ctx.get_writer().print_("hello:" + name + ":")
        ctx.invoke()

class TestDirectiveTag(AbstractJetxTest):

    def initialize_engine(self):
        self.engine.get_global_resolver().register_tags(Tags)

    def test(self):
        assert self.eval("#tag hello()#end") == "hello"
        assert self.eval("#tag hello()XXX#end") == "hello"
        assert self.eval("#tag helloWithBody()XXX#end") == "hello:XXX"
        assert self.eval("#tag helloWithParam('jetbrick')XXX#end") == "hello:jetbrick:XXX"

    def test_closure(self):
        assert self.eval("#set(i=1)#tag helloWithBody()${i}#end") == "hello:1"
        assert self.eval("#set(i=1)#tag helloWithBody()${i}#set(x=9)#end${x}") == "hello:19"

    def test_not_found(self):
        with pytest.raises(self.InterpretException) as e:
            self.eval("#tag hello(1)#end")
        assert self.err(self.Errors.TAG_NOT_FOUND) in str(e.value)