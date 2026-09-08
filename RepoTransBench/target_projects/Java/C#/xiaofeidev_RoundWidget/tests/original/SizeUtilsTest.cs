using Xunit;
using RoundWidget.utils;

namespace RoundWidget.Tests.Original
{
    public class SizeUtilsTest
    {
        [Fact]
        public void TestDp2PxAndPx2DpConsistency()
        {
            float density = 2.0f;
            float dp = 10f;
            float px = SizeUtils.dp2px(dp, density);
            float dpResult = SizeUtils.px2dp(px, density);
            Assert.InRange(dpResult, dp - 0.5f, dp + 0.5f);
        }

        [Fact]
        public void TestZero()
        {
            float density = 2.0f;
            Assert.Equal(0f, SizeUtils.dp2px(0f, density), 4);
            Assert.Equal(0, SizeUtils.px2dpContext(0f, density));
        }

        [Fact]
        public void TestDp2PxKnownValue()
        {
            float density = 3.5f;
            Assert.Equal(20f * density, SizeUtils.dp2px(20f, density), 4);
        }

        [Fact]
        public void TestPx2DpKnownValue()
        {
            float density = 2.5f;
            float px = 50f;
            int expectedDp = (int)(px / density + 0.5f);
            Assert.Equal(expectedDp, SizeUtils.px2dpContext(px, density));
        }
    }
}