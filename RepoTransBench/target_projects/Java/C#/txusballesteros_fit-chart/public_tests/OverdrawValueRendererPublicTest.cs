using Xunit;
using FitChart;

namespace FitChartTests.Public
{
    public class OverdrawValueRendererPublicTest
    {
        [Fact]
        public void TestBuildPath_WithOtherAngles()
        {
            var area = new RectF(2, 2, 50, 50);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(30f);
            value.SetSweepAngle(45f);

            var renderer = new OverdrawValueRenderer(area, value);

            var path = renderer.BuildPath(0.6f, 35f);

            Assert.NotNull(path);
        }
    }
}