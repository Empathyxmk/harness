using Xunit;
using GeoHashLib;
using GeoHashLib.queries;

namespace GeoHashLib.OriginalTests
{
    public class GeoHashCircleQueryTests
    {
        [Fact]
        public void TestIssue3WithCircleQuery()
        {
            var center = new WGS84Point(39.86391280373075, 116.37356590048701);
            var query = new GeoHashCircleQuery(center, 589);

            var test1 = new WGS84Point(39.8648866576058, 116.378465869303);
            var test2 = new WGS84Point(39.8664787092599, 116.378552856158);
            var test3 = new WGS84Point(39.8786787092599, 116.378552856158);

            Assert.True(query.Contains(test1));
            Assert.True(query.Contains(test2));
            Assert.False(query.Contains(test3));
        }

        [Fact]
        public void Test180MeridianCircleQuery()
        {
            var center = new WGS84Point(39.86391280373075, 179.98356590048701);
            var query = new GeoHashCircleQuery(center, 3000);

            var test1 = new WGS84Point(39.8648866576058, 180);
            var test2 = new WGS84Point(39.8664787092599, -180);
            var test3 = new WGS84Point(39.8686787092599, -179.9957861565146);
            var test4 = new WGS84Point(39.8686787092599, 179.0057861565146);
            var test5 = new WGS84Point(39.8686787092599, -179.0);

            Assert.True(query.Contains(test1));
            Assert.True(query.Contains(test2));
            Assert.True(query.Contains(test3));
            Assert.False(query.Contains(test4));
            Assert.False(query.Contains(test5));
        }
    }
}