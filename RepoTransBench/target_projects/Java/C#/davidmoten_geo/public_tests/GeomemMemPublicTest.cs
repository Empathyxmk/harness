using Xunit;
using System.Collections.Generic;

namespace DavidMoten.Geo.PublicTests
{
    public class GeomemMemPublicTest
    {
        [Fact]
        public void TestAddAndDifferentQuery()
        {
            var geo = Geomem<LatLong>.Create();
            geo.Add(35.0, 139.0, 200, new LatLong(35.0, 139.0)); // Tokyo
            geo.Add(51.5, -0.1, 180, new LatLong(51.5, -0.1)); // London

            var list = new List<Info<LatLong>>(geo.Find(35.5, 139.7, 100000));
            Assert.Single(list);
            Assert.Equal(35.0, list[0].Value.Lat, 5);
            Assert.Equal(139.0, list[0].Value.Lon, 5);
        }

        [Fact]
        public void TestNothingNearbyKnownAreas()
        {
            var geo = Geomem<string>.Create();
            geo.Add(40.7128, -74.0060, 120, "NewYork");
            var list = new List<Info<string>>(geo.Find(-33.8688, 151.2093, 100));
            Assert.Empty(list);
        }
    }
}