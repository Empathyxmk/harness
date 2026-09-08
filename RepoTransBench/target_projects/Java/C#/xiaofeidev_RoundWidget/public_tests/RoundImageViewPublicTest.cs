using Xunit;
using RoundWidget;

namespace RoundWidget.Tests.Public
{
    public class RoundImageViewPublicTest
    {
        [Fact]
        public void Constructor_And_Init_Minimal_Public()
        {
            var view = new RoundImageView();
            Assert.NotNull(view);
            Assert.Equal(0, RoundImageView.STROKE_MODE_PADDING);
            Assert.Equal(1, RoundImageView.STROKE_MODE_OVERLAY);
            Assert.IsType<RoundImageView>(view);
            Assert.NotNull(view.getRadiusList());
        }

        [Fact]
        public void Constructor_With_Attrs_Public()
        {
            var view = new RoundImageView();
            Assert.NotNull(view);
            Assert.NotNull(view.getRadiusList());
        }

        [Fact]
        public void TestSetAndGetRadius_Public()
        {
            var view = new RoundImageView();
            view.setRadius(12f);
            Assert.Equal(12f, view.getRadius(), 4);
            view.setTopRightRadius(7f);
            Assert.Equal(7f, view.getTopRightRadius(), 4);
        }

        [Fact]
        public void TestFillRadiusReflects_Public()
        {
            var view = new RoundImageView();
            view.setRadius(9f);
            view.setTopLeftRadius(2.2f);
            view.setTopRightRadius(3.3f);
            view.setBottomLeftRadius(4.4f);
            view.setBottomRightRadius(5.5f);
            view.fillRadius();
            float[] list = view.getRadiusList();
            Assert.Equal(2.2f, list[0], 4);
            Assert.Equal(3.3f, list[2], 4);
            Assert.Equal(4.4f, list[6], 4);
            Assert.Equal(5.5f, list[4], 4);
        }
    }
}