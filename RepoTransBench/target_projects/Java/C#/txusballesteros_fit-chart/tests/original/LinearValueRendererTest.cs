using Xunit;
using FitChart;

namespace FitChartTests.Original
{
    public class LinearValueRendererTest
    {
        [Fact]
        public void TestBuildPath_WithStartAngleLessThanSeek_BuildsArc()
        {
            var area = new RectF(0, 0, 100, 100);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(0f);
            value.SetSweepAngle(100f);

            var renderer = new LinearValueRenderer(area, value);

            var path = renderer.BuildPath(0.5f, 50f);

            Assert.NotNull(path);
        }

        [Fact]
        public void TestBuildPath_WithStartAngleGreaterThanSeek_ReturnsNull()
        {
            var area = new RectF(0, 0, 100, 100);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(100f);
            value.SetSweepAngle(50f);

            var renderer = new LinearValueRenderer(area, value);

            var path = renderer.BuildPath(0.5f, 40f);

            Assert.Null(path);
        }

        [Fact]
        public void TestCalculateSweepAngle_PathBranches()
        {
            var area = new RectF(0, 0, 100, 100);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(20f);
            value.SetSweepAngle(50f);

            var renderer = new LinearValueRenderer(area, value);

            // force totalSizeOfValue > animationSeek
            var path1 = renderer.BuildPath(0.5f, 40f);
            // force totalSizeOfValue <= animationSeek
            var path2 = renderer.BuildPath(0.5f, 80f);
        }
    }
}