using Xunit;
using RoundWidget;

namespace RoundWidget.Tests.Original
{
    public class RoundFrameLayoutTest
    {
        [Fact]
        public void Constructor_And_Init_Minimal()
        {
            var layout = new RoundFrameLayout();
            Assert.NotNull(layout);
            Assert.IsType<RoundFrameLayout>(layout);
            Assert.NotNull(layout.getRadiusList());
        }

        [Fact]
        public void Constructor_With_Attrs()
        {
            var layout = new RoundFrameLayout();
            Assert.NotNull(layout);
            Assert.NotNull(layout.getRadiusList());
        }

        [Fact]
        public void TestSetAndGetRadius()
        {
            var layout = new RoundFrameLayout();
            layout.setRadius(5f);
            Assert.Equal(5f, layout.getRadius(), 4);
            layout.setTopRightRadius(2f);
            Assert.Equal(2f, layout.getTopRightRadius(), 4);
        }

        [Fact]
        public void TestFillRadiusReflects()
        {
            var layout = new RoundFrameLayout();
            layout.setRadius(7f);
            layout.setTopLeftRadius(1.2f);
            layout.setTopRightRadius(2.3f);
            layout.setBottomLeftRadius(3.4f);
            layout.setBottomRightRadius(4.5f);
            layout.fillRadius();
            float[] list = layout.getRadiusList();
            Assert.Equal(1.2f, list[0], 4);
            Assert.Equal(2.3f, list[2], 4);
            Assert.Equal(3.4f, list[6], 4);
            Assert.Equal(4.5f, list[4], 4);
        }
    }
}