using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class TernaryOperatorTests : AbstractJetxTest
    {
        [Fact]
        public void TestBasic()
        {
            Assert.Equal("1", Eval("${true?1:0}"));
            Assert.Equal("0", Eval("${false?1:0}"));
            Assert.Equal("2", Eval("${false?1:true?2:3}"));
            Assert.Equal("2", Eval("${true?false?1:2:3}"));
        }

        [Fact]
        public void TestSimplify()
        {
            Assert.Equal("1", Eval("${null?:1}"));
            Assert.Equal("A", Eval("${'A'?:2}"));
            Assert.Equal("9", Eval("${a?:b?:9}"));
        }
    }
}