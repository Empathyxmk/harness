using Xunit;
using RoundWidget;

namespace RoundWidget.Tests.Original
{
    public class RoundImageViewTest
    {
        [Fact]
        public void Constructor_And_Init_Minimal()
        {
            var view = new RoundImageView();
            Assert.NotNull(view);
            Assert.IsType<RoundImageView>(view);
            Assert.NotNull(view.getRadiusList());
            Assert.Equal(0, RoundImageView.STROKE_MODE_PADDING);
            Assert.Equal(1, RoundImageView.STROKE_MODE_OVERLAY);
        }

        [Fact]
        public void Constructor_With_Attrs()
        {
            var view = new RoundImageView();
            Assert.NotNull(view);
            Assert.NotNull(view.getRadiusList());
        }

        [Fact]
        public void TestSetAndGetRadius()
        {
            var view = new RoundImageView();
            view.setRadius(6f);
            Assert.Equal(6f, view.getRadius(), 4);
            view.setTopRightRadius(4f);
            Assert.Equal(4f, view.getTopRightRadius(), 4);
        }

        [Fact]
        public void TestFillRadiusReflects()
        {
            var view = new RoundImageView();
            view.setRadius(8f);
            view.setTopLeftRadius(1.1f);
            view.setTopRightRadius(2.2f);
            view.setBottomLeftRadius(3.3f);
            view.setBottomRightRadius(4.4f);
            view.fillRadius();
            float[] list = view.getRadiusList();
            Assert.Equal(1.1f, list[0], 4);
            Assert.Equal(2.2f, list[2], 4);
            Assert.Equal(3.3f, list[6], 4);
            Assert.Equal(4.4f, list[4], 4);
        }
    }
}