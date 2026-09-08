using Xunit;
using GeoHashLib;

namespace GeoHashLib.PublicTests
{
    public class BoundingBoxPublicTests
    {
        [Fact]
        public void BoundingBoxConstructCorners_Public()
        {
            var sw = new WGS84Point(-55, 110);
            var ne = new WGS84Point(-15, 150);
            var box = new BoundingBox(sw, ne);

            Assert.Equal(-55, box.SouthWestCorner.Latitude, 5);
            Assert.Equal(110, box.SouthWestCorner.Longitude, 5);
            Assert.Equal(-15, box.NorthEastCorner.Latitude, 5);
            Assert.Equal(150, box.NorthEastCorner.Longitude, 5);

            Assert.Equal(-55, box.SouthLatitude, 5);
            Assert.Equal(-15, box.NorthLatitude, 5);
            Assert.Equal(110, box.WestLongitude, 5);
            Assert.Equal(150, box.EastLongitude, 5);
        }

        [Fact]
        public void LatitudeLongitudeSize_Public()
        {
            var box = new BoundingBox(22, 44, -45, -33);
            Assert.Equal(22.0, box.LatitudeSize, 5);
            Assert.Equal(12.0, box.LongitudeSize, 5);
        }

        [Fact]
        public void LongitudeWrapAroundMeridian_Public()
        {
            var box = new BoundingBox(-40, 40, 179, -179);
            Assert.True(box.LongitudeSize > 0);
        }

        [Fact]
        public void LongitudeEdgeCaseFullGlobe_Public()
        {
            var box = new BoundingBox(0, 90, -180, 180);
            Assert.Equal(360.0, box.LongitudeSize, 4);
        }

        [Fact]
        public void EqualsAndHashCode_Public()
        {
            var b1 = new BoundingBox(-10, 10, 50, 100);
            var b2 = new BoundingBox(-10, 10, 50, 100);
            var b3 = new BoundingBox(-11, 10, 50, 100);

            Assert.Equal(b1, b2);
            Assert.Equal(b1.GetHashCode(), b2.GetHashCode());
            Assert.NotEqual(b1, b3);
            Assert.False(b1.Equals(null));
            Assert.False(b1.Equals("something else"));
        }

        [Fact]
        public void ThrowsOnSouthGreaterThanNorth_Public()
        {
            Assert.Throws<ArgumentException>(() => new BoundingBox(20, 10, 0, 0));
        }

        [Fact]
        public void ThrowsOnOutOfRange_Public()
        {
            Assert.Throws<ArgumentException>(() => new BoundingBox(-100, 10, 0, 0));
            Assert.Throws<ArgumentException>(() => new BoundingBox(-10, 95.5, 0, 0));
            Assert.Throws<ArgumentException>(() => new BoundingBox(-10, 10, 0, 200));
            Assert.Throws<ArgumentException>(() => new BoundingBox(-10, 10, -200, 0));
        }
    }
}