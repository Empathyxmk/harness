using Xunit;

namespace OriginalTests
{
    public class MqttHanderTest
    {
        [Fact]
        public void TestDummy()
        {
            var m = new ProjectName.MqttHander();
            Assert.NotNull(m);
        }
    }
}