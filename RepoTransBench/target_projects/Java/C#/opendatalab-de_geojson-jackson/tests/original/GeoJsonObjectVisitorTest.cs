using Xunit;
using System;
using System.Collections.Generic;
using ProjectName.Models;

namespace ProjectName.Tests.Original
{
    public class GeoJsonObjectVisitorTest
    {
        public static IEnumerable<object[]> TestCases()
        {
            yield return new object[] { new GeometryCollection() };
            yield return new object[] { new FeatureCollection() };
            yield return new object[] { new Point(12D, 13D) };
            yield return new object[] { new Feature() };
            yield return new object[] { new MultiLineString(new List<LngLatAlt> { new LngLatAlt(12D, 13D) }) };
            yield return new object[] { new Polygon() };
            yield return new object[] { new MultiPolygon() };
            yield return new object[] { new MultiPoint() };
            yield return new object[] { new LineString() };
        }

        private GeoJsonObjectVisitorClass instance = new GeoJsonObjectVisitorClass();

        class GeoJsonObjectVisitorClass : IGeoJsonObjectVisitor<GeoJsonObject>
        {
            public GeoJsonObject Visit(GeometryCollection geoJsonObject)
            {
                Assert.IsType<GeometryCollection>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(FeatureCollection geoJsonObject)
            {
                Assert.IsType<FeatureCollection>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(Point geoJsonObject)
            {
                Assert.IsType<Point>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(Feature geoJsonObject)
            {
                Assert.IsType<Feature>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(MultiLineString geoJsonObject)
            {
                Assert.IsType<MultiLineString>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(Polygon geoJsonObject)
            {
                Assert.IsType<Polygon>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(MultiPolygon geoJsonObject)
            {
                Assert.IsType<MultiPolygon>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(MultiPoint geoJsonObject)
            {
                Assert.IsType<MultiPoint>(geoJsonObject);
                return geoJsonObject;
            }
            public GeoJsonObject Visit(LineString geoJsonObject)
            {
                Assert.IsType<LineString>(geoJsonObject);
                return geoJsonObject;
            }
        }

        [Theory]
        [MemberData(nameof(TestCases))]
        public void ShouldVisitRightClass(GeoJsonObject geoJsonObject)
        {
            var result = geoJsonObject.Accept(instance);
            Assert.Equal(geoJsonObject, result);
        }

        [Theory]
        [MemberData(nameof(TestCases))]
        public void ItShouldAdapter(GeoJsonObject geoJsonObject)
        {
            Assert.Null(geoJsonObject.Accept(new GeoJsonObjectVisitorAdapter<Void>()));
        }
    }

    // Helper for adapter pattern.
    public class GeoJsonObjectVisitorAdapter<T> : IGeoJsonObjectVisitor<T>
    {
        public T Visit(GeometryCollection gc) => default(T);
        public T Visit(FeatureCollection fc) => default(T);
        public T Visit(Point p) => default(T);
        public T Visit(Feature f) => default(T);
        public T Visit(MultiLineString mls) => default(T);
        public T Visit(Polygon p) => default(T);
        public T Visit(MultiPolygon mp) => default(T);
        public T Visit(MultiPoint mp) => default(T);
        public T Visit(LineString ls) => default(T);
    }
    public class Void { }
}