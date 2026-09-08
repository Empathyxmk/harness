using System.Collections.Generic;
using Newtonsoft.Json;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original.Jackson
{
    public class MultiLineStringTest
    {
        [Fact]
        public void ItShouldSerialize()
        {
            var multiLineString = new MultiLineString();
            multiLineString.Add(new List<LngLatAlt> { new LngLatAlt(100, 0), new LngLatAlt(101, 1) });
            multiLineString.Add(new List<LngLatAlt> { new LngLatAlt(102, 2), new LngLatAlt(103, 3) });
            var expected = "{\"type\":\"MultiLineString\",\"coordinates\":"
                + "[[[100.0,0.0],[101.0,1.0]],[[102.0,2.0],[103.0,3.0]]]}";
            var actual = JsonConvert.SerializeObject(multiLineString);
            Assert.Equal(expected, actual);
        }
    }
}