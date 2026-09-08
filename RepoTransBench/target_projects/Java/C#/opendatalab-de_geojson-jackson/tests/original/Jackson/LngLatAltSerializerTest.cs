using Newtonsoft.Json;
using Xunit;
using ProjectName.Models;

namespace ProjectName.Tests.Original.Jackson
{
    public class LngLatAltSerializerTest
    {
        [Fact]
        public void TestSerialization()
        {
            var position = new LngLatAlt(49.43245, 52.42345, 120.34626);
            var correctJson = "[49.43245,52.42345,120.34626]";
            var producedJson = JsonConvert.SerializeObject(position);
            Assert.Equal(correctJson, producedJson);
        }
    }
}