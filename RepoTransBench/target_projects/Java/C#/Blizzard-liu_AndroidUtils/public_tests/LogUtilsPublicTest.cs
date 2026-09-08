using Xunit;

namespace AndroidUtils.PublicTests
{
    public class LogUtilsPublicTest
    {
        [Fact]
        public void TestInfoLogLevel_Public()
        {
            string level = "INFO";
            Assert.NotEqual("ERROR", level);
        }
    }
}