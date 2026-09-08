using Newtonsoft.Json;
using Xunit;
using ProjectName.Models;
using System.Collections.Generic;

namespace ProjectName.Tests.Original.Jackson
{
    public class MultiPointTest
    {
        [Fact]
        public void ItShouldSerializeMultiPoint()
        {
            var multiPoint = new MultiPoint(new LngLatAlt(100, 0), new LngLatAlt(101, 1));
            var expected = "{\"type\":\"MultiPoint\",\"coordinates\":[[100.0,0.0],[101.0,1.0]]}";
            var json = JsonConvert.SerializeObject(multiPoint);
            Assert.Equal(expected, json);
        }

        [Fact]
        public void ItShouldDeserializeMultiPoint()
        {
            var multiPoint = JsonConvert.DeserializeObject<MultiPoint>("{\"type\":\"MultiPoint\",\"coordinates\":[[100.0,0.0],[101.0,1.0]]}");
            Assert.NotNull(multiPoint);
            var coordinates = multiPoint.GetCoordinates();
            PointTest.AssertLngLatAlt(100, 0, double.NaN, coordinates[0]);
            PointTest.AssertLngLatAlt(101, 1, double.NaN, coordinates[1]);
        }
    }
}