using System.Collections.Generic;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original
{
    public class MultiLineStringUnitTest
    {
        [Fact]
        public void TestConstructorAndAdd()
        {
            var p1 = new LngLatAlt(1, 2);
            var p2 = new LngLatAlt(3, 4);

            var l1 = new LineString(p1);
            var l2 = new LineString(p2);

            var mls = new MultiLineString();
            mls.Add(l1.GetCoordinates());
            mls.Add(l2.GetCoordinates());

            var coords = mls.GetCoordinates();
            Assert.Equal(2, coords.Count);
            Assert.Equal(l1.GetCoordinates(), coords[0]);
            Assert.Equal(l2.GetCoordinates(), coords[1]);
        }

        [Fact]
        public void TestAccept()
        {
            var mls = new MultiLineString();
            var result = mls.Accept(new Visitor());
            Assert.Equal("yes", result);
        }

        class Visitor : IGeoJsonObjectVisitor<string>
        {
            public string Visit(MultiLineString mls) => "yes";
            public string Visit(FeatureCollection fc) => null;
            public string Visit(Feature f) => null;
            public string Visit(Point p) => null;
            public string Visit(MultiPoint mp) => null;
            public string Visit(LineString ls) => null;
            public string Visit(Polygon p) => null;
            public string Visit(MultiPolygon mp) => null;
            public string Visit(GeometryCollection gc) => null;
        }
    }
}