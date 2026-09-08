using Newtonsoft.Json;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original.Jackson
{
    public class MultiPoligonTest
    {
        [Fact]
        public void ItShouldSerialize()
        {
            var multiPolygon = new MultiPolygon();
            multiPolygon.Add(new Polygon(MockData.EXTERNAL));
            var polygon = new Polygon(MockData.EXTERNAL);
            polygon.AddInteriorRing(MockData.INTERNAL);
            multiPolygon.Add(polygon);

            var expected = "{\"type\":\"MultiPolygon\",\"coordinates\":[[[[102.0,2.0],[103.0,2.0],[103.0,3.0],[102.0,3.0],[102.0,2.0]]],"
                + "[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],"
                + "[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]]}";
            var actual = JsonConvert.SerializeObject(multiPolygon);
            Assert.Equal(expected, actual);
        }

        [Fact]
        public void ItShouldDeserialize()
        {
            var multiPolygon = JsonConvert.DeserializeObject<MultiPolygon>(
                "{\"type\":\"MultiPolygon\",\"coordinates\":[[[[102.0,2.0],[103.0,2.0],[103.0,3.0],[102.0,3.0],[102.0,2.0]]],"
                + "[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],"
                + "[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]]}");
            Assert.Equal(2, multiPolygon.GetCoordinates().Count);
        }
    }
}