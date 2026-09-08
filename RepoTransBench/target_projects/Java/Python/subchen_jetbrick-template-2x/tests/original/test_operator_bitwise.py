from tests.original.common import AbstractJetxTest

class TestBitwiseOperator(AbstractJetxTest):

    def test_basic(self):
        assert self.eval("${0xF & 0x8}") == str(0xF & 0x8)
        assert self.eval("${0xF | 0x8}") == str(0xF | 0x8)
        assert self.eval("${0xF ^ 0x8}") == str(0xF ^ 0x8)
        assert self.eval("${~0xF}") == str(~0xF)
        assert self.eval("${~1 ^ 2 & 3 | 4}") == str(~1 ^ 2 & 3 | 4)

    def test_shift(self):
        assert self.eval("${0xFF << 4}") == str(0xFF << 4)
        assert self.eval("${0xFF >> 4}") == str(0xFF >> 4)
        # Simulate Java's '>>>' (unsigned right shift) in Python for positive numbers
        assert self.eval("${0xFF >>> 4}") == str((0xFF % 0x100000000) >> 4)