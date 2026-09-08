using Xunit;

namespace PublicTests
{
    public class ServerMqttHandlerServicePublicTest
    {
        [Fact]
        public void TestServerMqttHandlerNewConstruction()
        {
            var server = new DummyServerMqttHandlerService();
            Assert.NotNull(server);

            class DummyServerMqttHandlerService : ProjectName.ServerMqttHandlerService { }
        }
    }
}