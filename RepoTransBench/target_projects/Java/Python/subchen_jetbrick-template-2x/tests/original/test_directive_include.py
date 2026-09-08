import pytest

from tests.original.common import AbstractJetxTest

class TestDirectiveInclude(AbstractJetxTest):

    def test_include(self):
        s = "abc#include('/sub.jetx')123"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "xxx")
        assert self.eval() == "abcxxx123"

    def test_include_args(self):
        s = "#set(c='c')${a}#include('/sub.jetx', {b:'b'})${c}"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "<${a}-${b}-${c}>")
        ctx = {"a": "a"}
        assert self.eval(ctx) == "a<a-b-c>c"

    def test_return(self):
        s = "${X}#include('/sub.jetx', 'X')${X}"
        self.engine.set(self.DEFAULT_MAIN_FILE, s)
        self.engine.set("/sub.jetx", "#return(12345)")
        assert self.eval() == "12345"