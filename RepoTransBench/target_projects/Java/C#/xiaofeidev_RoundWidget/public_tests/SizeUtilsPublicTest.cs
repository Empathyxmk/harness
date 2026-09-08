using Xunit;
using RoundWidget.utils;

namespace RoundWidget.Tests.Public
{
    public class SizeUtilsPublicTest
    {
        [Fact]
        public void TestDp2PxAndPx2Dp_Public()
        {
            float density = 2.6f;
            float dp = 15f;
            int px = SizeUtils.dp2pxContext(dp, density);
            float expectedPx = 15f * density;
            Assert.Equal((int)(expectedPx + 0.5f), px);

            float dpResult = SizeUtils.px2dpContext(px, density);
            Assert.InRange(dpResult, dp - 0.5f, dp + 0.5f);
        }

        [Fact]
        public void TestSp2PxAndPx2Sp_Public()
        {
            float scaledDensity = 1.8f;
            float sp = 10f;
            int px = SizeUtils.sp2px(sp, scaledDensity);
            float expectedPx = 10f * scaledDensity;
            Assert.Equal((int)(expectedPx + 0.5f), px);

            float spResult = SizeUtils.px2sp(px, scaledDensity);
            Assert.InRange(spResult, sp - 0.5f, sp + 0.5f);
        }
    }
}