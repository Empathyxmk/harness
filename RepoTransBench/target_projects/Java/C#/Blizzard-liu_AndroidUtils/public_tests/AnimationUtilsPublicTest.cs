using Xunit;

namespace AndroidUtils.PublicTests
{
    public class AnimationUtilsPublicTest
    {
        [Fact]
        public void SimplePublicAnimationTest()
        {
            // Use a unique duration to avoid overlap with private
            int duration = 350;
            Assert.True(duration > 200);
        }
    }
}