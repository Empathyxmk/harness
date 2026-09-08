using Xunit;
using FitChart;

namespace FitChartTests.Original
{
    public class RendererFactoryTest
    {
        [Fact]
        public void TestReturnsLinearRenderer()
        {
            var value = new FitChartValue(0, 0);
            var rect = new RectF(0, 0, 100, 100);
            var renderer = RendererFactory.GetRenderer(AnimationMode.LINEAR, value, rect);
            Assert.IsType<LinearValueRenderer>(renderer);
        }

        [Fact]
        public void TestReturnsOverdrawRenderer()
        {
            var value = new FitChartValue(0, 0);
            var rect = new RectF(0, 0, 100, 100);
            var renderer = RendererFactory.GetRenderer(AnimationMode.OVERDRAW, value, rect);
            Assert.IsType<OverdrawValueRenderer>(renderer);
        }
    }
}