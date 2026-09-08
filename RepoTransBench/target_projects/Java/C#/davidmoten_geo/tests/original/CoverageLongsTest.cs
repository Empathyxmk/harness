using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class CoverageLongsTest
    {
        [Fact]
        public void TestCoverageLongsHashLength()
        {
            var coverage = new CoverageLongs(new long[] { }, 0, 1.0);
            Assert.Equal(0, coverage.HashLength);
            // Coverage of ToString
            System.Console.WriteLine(coverage.ToString());
        }

        [Fact]
        public void TestCoverageLongsOfAnAreaThatCantBeCoveredWithHashOfLengthOne()
        {
            var coverage = GeoHash.CoverBoundingBoxLongs(-5, 100, -45, 170, 1);
            Assert.Equal(1, coverage.HashLength);
        }
    }
}