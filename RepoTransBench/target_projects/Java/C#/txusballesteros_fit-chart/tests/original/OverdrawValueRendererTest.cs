using Xunit;
using FitChart;

namespace FitChartTests.Original
{
    public class OverdrawValueRendererTest
    {
        [Fact]
        public void TestBuildPath()
        {
            var area = new RectF(0, 0, 100, 100);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(10f);
            value.SetSweepAngle(100f);

            var renderer = new OverdrawValueRenderer(area, value);

            var path = renderer.BuildPath(0.5f, 50f);

            Assert.NotNull(path);
        }
    }
}