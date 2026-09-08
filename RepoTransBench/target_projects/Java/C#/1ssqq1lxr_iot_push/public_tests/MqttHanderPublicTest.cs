using Xunit;

namespace PublicTests
{
    public class MqttHanderPublicTest
    {
        [Fact]
        public void TestInstantiation()
        {
            var hander = new ProjectName.MqttHander();
            Assert.NotNull(hander);
        }
    }
}