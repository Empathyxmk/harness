using System.Collections.Generic;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original
{
    public class LineStringUnitTest
    {
        [Fact]
        public void TestConstructorAndAdd()
        {
            var p1 = new LngLatAlt(1, 2);
            var p2 = new LngLatAlt(2, 3);
            var line = new LineString(p1);
            line.Add(p2);
            var coords = line.GetCoordinates();
            Assert.Equal(2, coords.Count);
            Assert.Equal(p1, coords[0]);
            Assert.Equal(p2, coords[1]);
        }

        [Fact]
        public void TestAccept()
        {
            var line = new LineString();
            var result = line.Accept(new Visitor());
            Assert.Equal("ok", result);
        }

        class Visitor : IGeoJsonObjectVisitor<string>
        {
            public string Visit(LineString ls) => "ok";
            public string Visit(FeatureCollection fc) => null;
            public string Visit(Feature f) => null;
            public string Visit(Point p) => null;
            public string Visit(MultiPoint mp) => null;
            public string Visit(MultiLineString mls) => null;
            public string Visit(Polygon p) => null;
            public string Visit(MultiPolygon mp) => null;
            public string Visit(GeometryCollection gc) => null;
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var l1 = new LineString(new LngLatAlt(1, 2));
            var l2 = new LineString(new LngLatAlt(1, 2));
            Assert.Equal(l1, l2);
            Assert.Equal(l1.GetHashCode(), l2.GetHashCode());
            Assert.False(l1.Equals(null));
            Assert.False(l1.Equals(new object()));
            var l3 = new LineString(new LngLatAlt(2, 2));
            Assert.NotEqual(l1, l3);
        }

        [Fact]
        public void TestToString()
        {
            var l = new LineString();
            Assert.Contains("coordinates", l.ToString());
        }
    }
}