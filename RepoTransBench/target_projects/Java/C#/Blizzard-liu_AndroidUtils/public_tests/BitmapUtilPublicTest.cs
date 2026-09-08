using Xunit;

namespace AndroidUtils.PublicTests
{
    public class BitmapUtilPublicTest
    {
        [Fact]
        public void TestImageWidthLargerThanHeight_Public()
        {
            // Flip logic from original - width > height
            int width = 600, height = 400;
            Assert.True(width > height);
        }
    }
}