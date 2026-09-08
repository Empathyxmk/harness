using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class UnaryOperatorTests : AbstractJetxTest
    {
        [Fact]
        public void TestBasic()
        {
            Assert.Equal("2", Eval("${+2}"));
            Assert.Equal("-2", Eval("${-2}"));
            Assert.Equal("2.1", Eval("${+2.1}"));
            Assert.Equal("-2.1", Eval("${-2.1}"));
        }
    }
}