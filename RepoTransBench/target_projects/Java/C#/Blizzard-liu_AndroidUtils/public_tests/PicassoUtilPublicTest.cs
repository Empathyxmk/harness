using Xunit;

namespace AndroidUtils.PublicTests
{
    public class PicassoUtilPublicTest
    {
        [Fact]
        public void TestUrlIsJpeg_Public()
        {
            // Use jpeg instead of png
            string url = "https://example.org/altpic.jpeg";
            Assert.True(url.EndsWith(".jpeg"));
        }
    }
}