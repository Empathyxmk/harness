using Xunit;
using FitChart;

namespace FitChartTests.Public
{
    public class BaseRendererPublicTest
    {
        private class TestRenderer : BaseRenderer
        {
            public TestRenderer(RectF drawingArea, FitChartValue value)
                : base(drawingArea, value) { }

            public override Path BuildPath(float animationProgress, float animationSeek)
            {
                return null;
            }
        }

        [Fact]
        public void TestGetDrawingArea_AndGetValue_WithDifferentAreaAndValue()
        {
            var area = new RectF(10, 12, 34, 56);
            var value = new FitChartValue(55, 0xABCDEF);
            var renderer = new TestRenderer(area, value);

            Assert.Same(area, renderer.GetDrawingArea());
            Assert.Same(value, renderer.GetValue());
        }
    }
}