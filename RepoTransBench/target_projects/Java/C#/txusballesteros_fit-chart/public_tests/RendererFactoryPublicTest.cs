using Xunit;
using FitChart;

namespace FitChartTests.Public
{
    public class RendererFactoryPublicTest
    {
        [Fact]
        public void TestCreateRenderer_ReturnsLinearValueRendererWithDifferentArea()
        {
            var value = new FitChartValue(0, 0);
            var area = new RectF(1, 2, 80, 60);

            var renderer = RendererFactory.Create(area, value, AnimationMode.LINEAR);

            Assert.IsType<LinearValueRenderer>(renderer);
        }

        [Fact]
        public void TestCreateRenderer_ReturnsOverdrawValueRendererWithDifferentArea()
        {
            var value = new FitChartValue(0, 0);
            var area = new RectF(3, 4, 70, 30);

            var renderer = RendererFactory.Create(area, value, AnimationMode.OVERDRAW);

            Assert.IsType<OverdrawValueRenderer>(renderer);
        }
    }
}