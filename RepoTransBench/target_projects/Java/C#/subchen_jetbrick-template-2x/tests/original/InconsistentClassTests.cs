using System.Text;
using Xunit;

namespace JetbrickTemplate.Tests.Original
{
    public class InconsistentClassTests : AbstractJetxTest
    {
        [Fact]
        public void TestInclude()
        {
            var s = new StringBuilder();
            s.Append("#for(int i:[0,1,2])${i}#end");
            s.Append("#include('/sub.jetx')");
            engine.Set(DEFAULT_MAIN_FILE, s.ToString());

            s = new StringBuilder();
            s.Append("#for(int i:[0,1,2])${i}#end");
            engine.Set("/sub.jetx", s.ToString());

            Assert.Equal("012012", Eval());
        }
    }
}