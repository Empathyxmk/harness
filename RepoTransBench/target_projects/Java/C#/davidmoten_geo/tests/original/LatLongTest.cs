using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class LatLongTest
    {
        [Fact]
        public void TestToString()
        {
            var val = new LatLong(10, 20).ToString();
            Assert.Equal("LatLong [lat=10.0, lon=20.0]", val);
        }

        [Fact]
        public void TestHashCode()
        {
            float lat = 20.05f;
            float lon = -15.5f;
            var a = new LatLong(lat, lon);
            var b = new LatLong(lat, lon);

            Assert.Equal(a.GetHashCode(), b.GetHashCode());
            Assert.Equal(a, b);
        }
    }
}