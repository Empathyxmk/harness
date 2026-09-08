using Xunit;

namespace MarkushiAndroidUi.Tests.Original
{
    public class PlusActionTests
    {
        [Fact]
        public void TestPlusActionLineData()
        {
            var plusAction = new PlusAction();
            Assert.NotNull(plusAction.GetLineData());
            Assert.Equal(12, plusAction.GetLineData().Length);

            // check main vertical line
            Assert.Equal(0.5f, plusAction.GetLineData()[0], 5);

            // check main horizontal line
            Assert.Equal(0.5f, plusAction.GetLineData()[5], 5);
        }
    }
}