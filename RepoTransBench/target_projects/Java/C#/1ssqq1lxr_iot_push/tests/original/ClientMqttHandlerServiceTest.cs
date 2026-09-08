using Xunit;

namespace OriginalTests
{
    public class ClientMqttHandlerServiceTest
    {
        [Fact]
        public void TestClientMqttHandlerConstruction()
        {
            var client = new ProjectName.ClientMqttHandlerService();
            Assert.NotNull(client);
        }
    }
}