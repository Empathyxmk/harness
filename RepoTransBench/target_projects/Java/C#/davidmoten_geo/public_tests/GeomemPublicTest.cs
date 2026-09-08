using Xunit;
using System.Collections.Generic;

namespace DavidMoten.Geo.PublicTests
{
    public class GeomemPublicTest
    {
        [Fact]
        public void TestAddAndQueryDifferentValues()
        {
            var geo = Geomem<LatLong>.Create();
            geo.Add(50.12, 8.68, 700, new LatLong(50.12, 8.68));
            geo.Add(48.85, 2.35, 900, new LatLong(48.85, 2.35));

            var list = new List<Info<LatLong>>(geo.Find(49, 8, 350000));
            Assert.Single(list);
            Assert.Equal(50.12, list[0].Value.Lat, 5);
            Assert.Equal(8.68, list[0].Value.Lon, 5);
        }

        [Fact]
        public void TestEmptyQueryDifferentArea()
        {
            var geo = Geomem<string>.Create();
            geo.Add(37.77, -122.41, 100, "San Francisco");
            var list = new List<Info<string>>(geo.Find(41.89, 12.49, 1000));
            Assert.Empty(list);
        }
    }
}