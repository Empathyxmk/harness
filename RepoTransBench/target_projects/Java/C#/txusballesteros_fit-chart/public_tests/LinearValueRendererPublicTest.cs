using Xunit;
using FitChart;

namespace FitChartTests.Public
{
    public class LinearValueRendererPublicTest
    {
        [Fact]
        public void TestBuildPath_WithDifferentStartAngleLessThanSeek_BuildsArc()
        {
            var area = new RectF(5, 5, 120, 120);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(10f);
            value.SetSweepAngle(30f);

            var renderer = new LinearValueRenderer(area, value);

            var path = renderer.BuildPath(0.7f, 25f);

            Assert.NotNull(path);
        }

        [Fact]
        public void TestBuildPath_WithDifferentStartAngleGreaterThanSeek_ReturnsNull()
        {
            var area = new RectF(10, 10, 80, 80);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(60f);
            value.SetSweepAngle(15f);

            var renderer = new LinearValueRenderer(area, value);

            var path = renderer.BuildPath(0.3f, 40f);

            Assert.Null(path);
        }

        [Fact]
        public void TestCalculateSweepAngle_BranchesWithDifferentData()
        {
            var area = new RectF(5, 5, 90, 90);
            var value = new FitChartValue(0, 0);
            value.SetStartAngle(5f);
            value.SetSweepAngle(25f);

            var renderer = new LinearValueRenderer(area, value);

            // force totalSizeOfValue > animationSeek
            var path1 = renderer.BuildPath(0.3f, 20f);
            // force totalSizeOfValue <= animationSeek
            var path2 = renderer.BuildPath(0.6f, 40f);
        }
    }
}