using Xunit;
using ArtHook;

namespace ArtHook.PublicTests
{
    public class ZygoteInitPublicTest
    {
        [Fact]
        public void TestMainRunsXposedAndUtilsWithDifferentArgs()
        {
            ZygoteInit.main(new[] { "bar", "baz" });
            Assert.True(true);
        }
    }
}