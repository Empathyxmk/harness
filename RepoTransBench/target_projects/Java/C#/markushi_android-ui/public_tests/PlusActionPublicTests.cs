using Xunit;

namespace MarkushiAndroidUi.PublicTests
{
    public class PlusActionPublicTests
    {
        [Fact]
        public void TestPlusActionLineDataPublic()
        {
            var plusAction = new PlusAction();
            Assert.NotNull(plusAction.GetLineData());
            Assert.Equal(12, plusAction.GetLineData().Length);

            // check middle point of the vertical line (different index from original)
            Assert.NotEqual(0.5f, plusAction.GetLineData()[1], 5);

            // check another value in the array is within [0, 1]
            Assert.True(plusAction.GetLineData()[3] >= 0f && plusAction.GetLineData()[3] <= 1f);
        }
    }
}