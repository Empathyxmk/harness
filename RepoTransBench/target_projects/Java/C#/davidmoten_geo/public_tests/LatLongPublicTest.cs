using Xunit;

namespace DavidMoten.Geo.PublicTests
{
    public class LatLongPublicTest
    {
        [Fact]
        public void TestToStringDifferentValue()
        {
            Assert.Equal("LatLong [lat=-15.25, lon=35.75]", new LatLong(-15.25, 35.75).ToString());
        }

        [Fact]
        public void TestHashCodeAndEqualsWithDifferentValues()
        {
            float lat = -30.42f;
            float lon = 44.44f;
            var a = new LatLong(lat, lon);
            var b = new LatLong(lat, lon);

            Assert.Equal(a.GetHashCode(), b.GetHashCode());
            Assert.Equal(a, b);
        }
    }
}