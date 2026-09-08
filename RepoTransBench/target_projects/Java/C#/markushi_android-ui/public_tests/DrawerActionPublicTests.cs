using Xunit;

namespace MarkushiAndroidUi.PublicTests
{
    public class DrawerActionPublicTests
    {
        [Fact]
        public void TestDrawerActionLineDataPublic()
        {
            var drawerAction = new DrawerAction();
            Assert.NotNull(drawerAction.GetLineData());
            Assert.Equal(12, drawerAction.GetLineData().Length);

            // check a value not checked in the original (index 7)
            Assert.True(drawerAction.GetLineData()[7] >= 0f && drawerAction.GetLineData()[7] <= 1f);

            // ensure at least one line does NOT have 0.5f value at a new index
            Assert.NotEqual(0.5f, drawerAction.GetLineData()[2], 5);
        }
    }
}