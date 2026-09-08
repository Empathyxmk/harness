using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class DirectiveStopTests : AbstractJetxTest
    {
        [Fact]
        public void TestForBreak()
        {
            Assert.Equal("1a2", Eval("#for(i:[1,2,3])${i}#break(i>1)a#end"));
        }

        [Fact]
        public void TestForContinue()
        {
            Assert.Equal("1a23", Eval("#for(i:[1,2,3])${i}#continue(i>1)a#end"));
        }

        [Fact]
        public void TestForStop()
        {
            Assert.Equal("123", Eval("123#stop()abc"));
            Assert.Equal("1a2", Eval("#for(i:[1,2,3])${i}#stop(i>1)a#end()123"));
        }
    }
}