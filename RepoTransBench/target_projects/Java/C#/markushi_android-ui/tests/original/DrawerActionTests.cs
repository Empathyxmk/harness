using Xunit;

namespace MarkushiAndroidUi.Tests.Original
{
    public class DrawerActionTests
    {
        [Fact]
        public void TestDrawerActionLineData()
        {
            var drawerAction = new DrawerAction();
            Assert.NotNull(drawerAction.GetLineData());
            Assert.Equal(12, drawerAction.GetLineData().Length);

            // check for correct center value
            Assert.Equal(0.5f, drawerAction.GetLineData()[5], 5);
        }
    }
}