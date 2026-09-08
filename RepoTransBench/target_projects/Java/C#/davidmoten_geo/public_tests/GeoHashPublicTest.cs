using Xunit;
using System.Collections.Generic;

namespace DavidMoten.Geo.PublicTests
{
    public class GeoHashPublicTest
    {
        private const double TOKYO_LON = 139.6917;
        private const double TOKYO_LAT = 35.6895;
        private const double LONDON_LON = -0.1278;
        private const double LONDON_LAT = 51.5074;
        private const double PRECISION = 0.000000001;

        [Fact]
        public void EncodeHashToLongDifferentData()
        {
            Assert.Equal(0xc819000000000002L, GeoHash.EncodeHashToLong(35.6895, 139.6917, 2));
        }

        [Fact]
        public void FromLongToStringInvalidDifferent()
        {
            Assert.Throws<System.ArgumentException>(() => GeoHash.FromLongToString(0x1ee));
        }

        [Fact]
        public void FromLongToStringZeroDifferent()
        {
            Assert.Throws<System.ArgumentException>(() => GeoHash.FromLongToString(0));
        }

        [Fact]
        public void TestDifferentLandmarkHashEncode()
        {
            Assert.Equal("xn774c06kdt4", GeoHash.EncodeHash(35.6895, 139.6917));
        }

        [Fact]
        public void TestLandmarkHashEncodeUsingLatLongObject()
        {
            Assert.Equal("xn774c06kdt4", GeoHash.EncodeHash(new LatLong(35.6895, 139.6917)));
        }

        [Fact]
        public void TestLandmarkHashDecode()
        {
            LatLong point = GeoHash.DecodeHash("xn774c06kdt4");
            Assert.Equal(point.Lat, 35.6895, 9);
            Assert.Equal(point.Lon, 139.6917, 9);
        }

        [Fact]
        public void TestFromGeoHashDotOrgDifferentPoint()
        {
            Assert.Equal("gcpuvnjdgn85", GeoHash.EncodeHash(51.5074, -0.1278));
        }

        [Fact]
        public void TestHashOfNonDefaultLengthDifferent()
        {
            Assert.Equal("gcpuvn", GeoHash.EncodeHash(51.5074, -0.1278, 6));
        }

        [Fact]
        public void TestAdjacentTopDifferent()
        {
            Assert.Equal("xn774c06kdt7", GeoHash.AdjacentHash("xn774c06kdt4", Direction.TOP));
        }

        [Fact]
        public void TestAdjacentBottomDifferent()
        {
            Assert.Equal("xn774c06kdt1", GeoHash.AdjacentHash("xn774c06kdt4", Direction.BOTTOM));
        }

        [Fact]
        public void TestAdjacentLeftDifferent()
        {
            Assert.Equal("xn774c06kdt3", GeoHash.AdjacentHash("xn774c06kdt4", Direction.LEFT));
        }

        [Fact]
        public void TestAdjacentRightDifferent()
        {
            Assert.Equal("xn774c06kdt5", GeoHash.AdjacentHash("xn774c06kdt4", Direction.RIGHT));
        }

        [Fact]
        public void TestNeighbouringHashesDifferent()
        {
            string center = "gcpuvn";
            var neighbours = new HashSet<string> { "gcpuvm", "gcpuvp", "gcpuvj", "gcpuvs", "gcpuvh", "gcpuvt", "gcpuvk", "gcpuvq" };
            var actual = new HashSet<string>(GeoHash.Neighbours(center));
            Assert.Equal(neighbours, actual);
        }

        [Fact]
        public void TestHashDecodeOnBlankStringDifferent()
        {
            LatLong point = GeoHash.DecodeHash("");
            Assert.Equal(0, point.Lat, 9);
            Assert.Equal(0, point.Lon, 9);
        }

        [Fact]
        public void TestCoverBoundingBoxWithHashLength4AroundLondonAndTokyo()
        {
            var hashes = GeoHash.CoverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 4).Hashes;
            Assert.Equal("gcpu", GeoHash.EncodeHash(LONDON_LAT, LONDON_LON, 4));
            Assert.Equal("xn76", GeoHash.EncodeHash(TOKYO_LAT, TOKYO_LON, 4));
            Assert.Contains("gcpu", hashes);
            Assert.Contains("xn76", hashes);
        }

        [Fact]
        public void TestCoverBoundingBoxWithHashLengthOneAroundLondonAndTokyo()
        {
            var coverage = GeoHash.CoverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 1);
            var expectedHashes = new HashSet<string> { "g", "x" };
            Assert.Equal(expectedHashes, new HashSet<string>(coverage.Hashes));
            Assert.Equal(1, coverage.HashLength);
        }

        [Fact]
        public void TestCoverBoundingBoxWithOptimalHashLengthAroundLondonAndTokyo()
        {
            var coverage = GeoHash.CoverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON);
            Assert.True(coverage.Hashes.Count >= 1);
            Assert.True(coverage.HashLength >= 1);
        }

        [Fact]
        public void TestCoverBoundingBoxWithHashLength3AroundLondonAndTokyo()
        {
            var hashes = GeoHash.CoverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 3).Hashes;
            Assert.Contains("gcp", hashes);
            Assert.Contains("xn7", hashes);
        }

        [Fact]
        public void TestCoverBoundingBoxWithZeroLengthThrowsExceptionPublic()
        {
            Assert.Throws<System.ArgumentException>(() =>
                GeoHash.CoverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 0)
            );
        }
    }
}