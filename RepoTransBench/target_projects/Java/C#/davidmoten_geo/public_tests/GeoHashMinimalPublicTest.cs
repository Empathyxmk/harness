using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class GeoHashMinimalPublicTest
    {
        [Fact]
        public void TestEncodeDecodeRoundTripDifferent()
        {
            double lat = -33.8688;
            double lon = 151.2093;
            string hash = GeoHash.EncodeHash(lat, lon, 7);
            LatLong decoded = GeoHash.DecodeHash(hash);
            Assert.True(System.Math.Abs(decoded.Lat - lat) < 0.01);
            Assert.True(System.Math.Abs(decoded.Lon - lon) < 0.01);
        }

        [Fact]
        public void TestEncodeDecodeWithZeroValues()
        {
            double lat = 0.0;
            double lon = 10.123456;
            string hash = GeoHash.EncodeHash(lat, lon, 8);
            LatLong decoded = GeoHash.DecodeHash(hash);
            Assert.True(System.Math.Abs(decoded.Lat - lat) < 0.01);
            Assert.True(System.Math.Abs(decoded.Lon - lon) < 0.01);
        }
    }
}