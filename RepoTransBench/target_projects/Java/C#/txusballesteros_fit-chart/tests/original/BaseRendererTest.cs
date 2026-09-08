using Xunit;
using FitChart;

namespace FitChartTests.Original
{
    public class BaseRendererTest
    {
        private class ConcreteRenderer : BaseRenderer
        {
            public ConcreteRenderer(RectF drawingArea, FitChartValue value)
                : base(drawingArea, value) { }

            public override Path BuildPath(float animationProgress, float animationSeek)
            {
                return null;
            }
        }

        [Fact]
        public void TestGetters()
        {
            var area = new RectF(1, 2, 3, 4);
            var val = new FitChartValue(0, 0);
            var renderer = new ConcreteRenderer(area, val);
            Assert.Equal(area, renderer.GetDrawingArea());
            Assert.Equal(val, renderer.GetValue());
        }
    }
}