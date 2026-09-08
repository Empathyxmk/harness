using Xunit;
using RoundWidget;

namespace RoundWidget.Tests.Public
{
    public class RoundFrameLayoutPublicTest
    {
        [Fact]
        public void Constructor_And_Init_Minimal_Public()
        {
            var layout = new RoundFrameLayout();
            Assert.NotNull(layout);
            Assert.IsType<RoundFrameLayout>(layout);
            Assert.NotNull(layout.getRadiusList());
        }

        [Fact]
        public void Constructor_With_Attrs_Public()
        {
            var layout = new RoundFrameLayout();
            Assert.NotNull(layout);
            Assert.NotNull(layout.getRadiusList());
        }

        [Fact]
        public void TestSetAndGetRadius_Public()
        {
            var layout = new RoundFrameLayout();
            layout.setRadius(13f);
            Assert.Equal(13f, layout.getRadius(), 4);
            layout.setTopRightRadius(8f);
            Assert.Equal(8f, layout.getTopRightRadius(), 4);
        }

        [Fact]
        public void TestFillRadiusReflects_Public()
        {
            var layout = new RoundFrameLayout();
            layout.setRadius(11f);
            layout.setTopLeftRadius(2.4f);
            layout.setTopRightRadius(4.3f);
            layout.setBottomLeftRadius(6.1f);
            layout.setBottomRightRadius(8.7f);
            layout.fillRadius();
            float[] list = layout.getRadiusList();
            Assert.Equal(2.4f, list[0], 4);
            Assert.Equal(4.3f, list[2], 4);
            Assert.Equal(6.1f, list[6], 4);
            Assert.Equal(8.7f, list[4], 4);
        }
    }
}