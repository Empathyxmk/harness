using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveCallTests : AbstractJetxTest
    {
        [Fact]
        public void Test()
        {
            Assert.Equal("2", Eval("#macro inc(int x)${x+1}#end#call inc(1)"));
        }
    }
}