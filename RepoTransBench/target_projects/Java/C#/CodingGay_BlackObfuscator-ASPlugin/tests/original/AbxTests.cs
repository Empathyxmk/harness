using Xunit;
using BlackObfuscatorASPlugin;

namespace BlackObfuscatorASPlugin.Tests.Original
{
    public class AbxTests
    {
        [Fact]
        public void TestGoAlwaysTrue()
        {
            Assert.True(Abx.Go());
        }
    }
}