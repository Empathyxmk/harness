using Xunit;
using System.Collections.Generic;
using System.Linq;
using ProjectName.Models;

namespace ProjectName.Tests.Original
{
    public class FeatureCollectionTest
    {
        [Fact]
        public void TestAddAndGetFeatures()
        {
            var fc = new FeatureCollection();
            var f1 = new Feature();
            var f2 = new Feature();
            fc.Add(f1);
            fc.Add(f2);

            var features = fc.Features.ToList();
            Assert.Equal(2, features.Count);
            Assert.Contains(f1, features);
            Assert.Contains(f2, features);
        }

        [Fact]
        public void TestSetFeatures()
        {
            var fc = new FeatureCollection();
            var f = new Feature();
            var lst = new List<Feature> { f };
            fc.Features = lst;
            Assert.Equal(lst, fc.Features);
        }

        [Fact]
        public void TestAddAll()
        {
            var fc = new FeatureCollection();
            var f1 = new Feature();
            var f2 = new Feature();
            var lst = new List<Feature> { f1, f2 };
            fc.AddRange(lst);
            Assert.True(fc.Features.All(f => lst.Contains(f)));
        }

        [Fact]
        public void TestIterator()
        {
            var fc = new FeatureCollection();
            var f1 = new Feature();
            fc.Add(f1);
            var iterator = fc.Features.GetEnumerator();
            Assert.True(iterator.MoveNext());
            Assert.Equal(f1, iterator.Current);
        }

        [Fact]
        public void TestAccept()
        {
            var fc = new FeatureCollection();
            string result = fc.Accept(new TestVisitor());
            Assert.Equal("visited", result);
        }

        class TestVisitor : IGeoJsonObjectVisitor<string>
        {
            public string Visit(FeatureCollection fc) => "visited";
            public string Visit(Feature f) => null;
            public string Visit(Point p) => null;
            public string Visit(MultiPoint mp) => null;
            public string Visit(LineString ls) => null;
            public string Visit(MultiLineString mls) => null;
            public string Visit(Polygon p) => null;
            public string Visit(MultiPolygon mp) => null;
            public string Visit(GeometryCollection gc) => null;
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var fc1 = new FeatureCollection();
            var fc2 = new FeatureCollection();
            var f = new Feature();
            fc1.Add(f);
            fc2.Add(f);
            Assert.Equal(fc1, fc2);
            Assert.Equal(fc1.GetHashCode(), fc2.GetHashCode());
            Assert.False(fc1!.Equals(null));
            Assert.False(fc1.Equals(new Feature()));
            var fc3 = new FeatureCollection();
            Assert.NotEqual(fc1, fc3);
        }

        [Fact]
        public void TestToString()
        {
            var fc = new FeatureCollection();
            Assert.Contains("features", fc.ToString());
        }
    }
}