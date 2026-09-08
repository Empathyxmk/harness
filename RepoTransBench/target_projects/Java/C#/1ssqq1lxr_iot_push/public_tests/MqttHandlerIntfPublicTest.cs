using Xunit;

namespace PublicTests
{
    public class MqttHandlerIntfPublicTest
    {
        [Fact]
        public void TestInterfacePublicImpl()
        {
            var dummy = new PublicDummyMqttHandler();
            Assert.NotNull(dummy);

            class PublicDummyMqttHandler : ProjectName.IMqttHandlerIntf {}
        }
    }
}