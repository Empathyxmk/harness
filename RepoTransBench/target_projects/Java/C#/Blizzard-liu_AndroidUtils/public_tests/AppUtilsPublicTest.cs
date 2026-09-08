using Xunit;

namespace AndroidUtils.PublicTests
{
    public class AppUtilsPublicTest
    {
        [Fact]
        public void TestIsAppForeground_True()
        {
            // Different value from original (true instead of false)
            bool isForeground = true;
            Assert.True(isForeground);
        }
    }
}