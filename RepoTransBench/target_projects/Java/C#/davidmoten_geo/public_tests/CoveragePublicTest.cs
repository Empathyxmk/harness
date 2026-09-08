using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class CoveragePublicTest
    {
        [Fact]
        public void TestCoverageOfBoundingBoxWithDifferentData()
        {
            double lat1 = -10.0;
            double lon1 = 120.0;
            double lat2 = -9.5;
            double lon2 = 120.5;
            int hashLen = 4;
            var coverage = GeoHash.CoverBoundingBox(lat1, lon1, lat2, lon2, hashLen);
            Assert.NotNull(coverage);
            Assert.Equal(hashLen, coverage.HashLength);
            Assert.NotEmpty(coverage.Hashes);
        }

        [Fact]
        public void TestCoverageOptimalLengthDifferent()
        {
            double lat1 = 35.0, lon1 = 135.0, lat2 = 35.1, lon2 = 135.1;
            var coverage = GeoHash.CoverBoundingBox(lat1, lon1, lat2, lon2);
            Assert.NotNull(coverage);
            Assert.True(coverage.HashLength > 0);
            Assert.NotEmpty(coverage.Hashes);
        }

        [Fact]
        public void TestCoverageMaxHashesNullDifferent()
        {
            double lat1 = -5.0, lon1 = 140.0, lat2 = -5.0, lon2 = 141.0;
            var coverage = GeoHash.CoverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 0);
            Assert.Null(coverage);
        }
    }
}