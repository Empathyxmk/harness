using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class BitwiseOperatorTests : AbstractJetxTest
    {
        [Fact]
        public void TestBasic()
        {
            Assert.Equal(Str(0xF & 0x8), Eval("${0xF & 0x8}"));
            Assert.Equal(Str(0xF | 0x8), Eval("${0xF | 0x8}"));
            Assert.Equal(Str(0xF ^ 0x8), Eval("${0xF ^ 0x8}"));
            Assert.Equal(Str(~0xF), Eval("${~0xF}"));
            Assert.Equal(Str(~1 ^ 2 & 3 | 4), Eval("${~1 ^ 2 & 3 | 4}"));
        }

        [Fact]
        public void TestShift()
        {
            Assert.Equal(Str(0xFF << 4), Eval("${0xFF << 4}"));
            Assert.Equal(Str(0xFF >> 4), Eval("${0xFF >> 4}"));
            Assert.Equal(Str((int)((uint)0xFF >> 4)), Eval("${0xFF >>> 4}"));
        }
    }
}