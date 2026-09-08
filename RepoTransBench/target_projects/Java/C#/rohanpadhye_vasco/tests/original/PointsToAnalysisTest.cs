using Xunit;

namespace Vasco.Tests.Original
{
    public class PointsToAnalysisTest
    {
        [Fact]
        public void Coverage()
        {
            var pta = new PointsToAnalysis<string, string>();
            Assert.NotNull(pta);
        }
    }
}