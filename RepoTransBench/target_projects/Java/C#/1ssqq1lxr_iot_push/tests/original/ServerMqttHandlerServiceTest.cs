using Xunit;

namespace OriginalTests
{
    public class ServerMqttHandlerServiceTest
    {
        [Fact]
        public void TestServerMqttHandlerConstruction()
        {
            var server = new ProjectName.ServerMqttHandlerService();
            Assert.NotNull(server);
        }
    }
}