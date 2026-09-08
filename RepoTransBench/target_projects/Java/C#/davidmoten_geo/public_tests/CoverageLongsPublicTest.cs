using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class CoverageLongsPublicTest
    {
        [Fact]
        public void TestCoverageLongsForDifferentRegion()
        {
            double lat1 = 52.5, lon1 = 13.4, lat2 = 52.6, lon2 = 13.5;
            var hashes = CoverageLongs.CoverBoundingBoxLongs(lat1, lon1, lat2, lon2, 5).Hashes;
            Assert.NotNull(hashes);
            Assert.NotEmpty(hashes);
        }

        [Fact]
        public void TestCoverageLongsMaxHashesDifferent()
        {
            double lat1 = 48.8566, lon1 = 2.3522, lat2 = 48.8567, lon2 = 2.3523;
            var result = CoverageLongs.CoverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 1);
            Assert.NotNull(result);
            Assert.True(result.HashLength > 0);
        }

        [Fact]
        public void TestCoverageLongsNullIfTooManyHashesDifferent()
        {
            double lat1 = 50.0, lon1 = -0.01, lat2 = 50.0, lon2 = 0.01;
            var result = CoverageLongs.CoverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 0);
            Assert.Null(result);
        }
    }
}