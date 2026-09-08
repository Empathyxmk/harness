using Xunit;
using FAFToolbar.Util;

namespace PublicTests.Util
{
    public class ExpandAnimationUtilsPublicTest
    {
        [Fact]
        public void TestGetWidthAfterCollapse_WithOtherParams()
        {
            int initialWidth = 100;
            int deltaWidth = 25;
            int expected = 75;
            int result = ExpandAnimationUtils.GetWidthAfterCollapse(initialWidth, deltaWidth);
            Assert.Equal(expected, result);
        }

        [Fact]
        public void TestGetWidthAfterExpand_WithOtherParams()
        {
            int initialWidth = 150;
            int deltaWidth = 45;
            int expected = 195;
            int result = ExpandAnimationUtils.GetWidthAfterExpand(initialWidth, deltaWidth);
            Assert.Equal(expected, result);
        }
    }
}