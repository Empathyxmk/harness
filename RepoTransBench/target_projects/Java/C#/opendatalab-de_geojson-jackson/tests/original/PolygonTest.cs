using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original.Jackson
{
    public class PolygonTest
    {
        [Fact]
        public void ItShouldSerialize()
        {
            var polygon = new Polygon(MockData.EXTERNAL);
            var expected = "{\"type\":\"Polygon\",\"coordinates\":"
                + "[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]]]}";
            var serialized = JsonConvert.SerializeObject(polygon);
            Assert.Equal(expected, serialized);
        }

        [Fact]
        public void ItShouldSerializeWithHole()
        {
            var polygon = new Polygon(MockData.EXTERNAL);
            polygon.AddInteriorRing(MockData.INTERNAL);
            var expected = "{\"type\":\"Polygon\",\"coordinates\":"
                + "[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],"
                + "[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]}";
            var serialized = JsonConvert.SerializeObject(polygon);
            Assert.Equal(expected, serialized);
        }

        [Fact]
        public void ItShouldFailOnAddInteriorRingWithoutExteriorRing()
        {
            var polygon = new Polygon();
            Assert.Throws<InvalidOperationException>(() =>
            {
                polygon.AddInteriorRing(MockData.EXTERNAL);
            });
        }

        [Fact]
        public void ItShouldDeserialize()
        {
            var json = "{\"type\":\"Polygon\",\"coordinates\":"
                + "[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],"
                + "[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]}";
            var polygon = JsonConvert.DeserializeObject<Polygon>(json);

            AssertListEquals(MockData.EXTERNAL, polygon.GetExteriorRing());
            AssertListEquals(MockData.INTERNAL, polygon.GetInteriorRing(0));
            AssertListEquals(MockData.INTERNAL, polygon.GetInteriorRings()[0]);
        }

        [Fact]
        public void ItShouldSetExteriorRing()
        {
            var polygon = new Polygon();
            polygon.SetExteriorRing(MockData.EXTERNAL);
            Assert.Equal(MockData.EXTERNAL, polygon.GetExteriorRing());
        }

        [Fact]
        public void ItShouldReplaceExteriorRing()
        {
            var polygon = new Polygon(new List<LngLatAlt> {
                new LngLatAlt(0, 0),
                new LngLatAlt(1, 0),
                new LngLatAlt(1, 1),
                new LngLatAlt(0, 1),
                new LngLatAlt(0, 0)
            });
            polygon.SetExteriorRing(MockData.EXTERNAL);
            Assert.Equal(MockData.EXTERNAL, polygon.GetExteriorRing());
            Assert.Empty(polygon.GetInteriorRings());
        }

        private void AssertListEquals(List<LngLatAlt> expected, List<LngLatAlt> actual)
        {
            Assert.Equal(expected.Count, actual.Count);
            for (int i = 0; i < actual.Count; i++)
            {
                var exp = expected[i];
                var act = actual[i];
                PointTest.AssertLngLatAlt(exp.Longitude, exp.Latitude, exp.Altitude, act);
            }
        }
    }
}