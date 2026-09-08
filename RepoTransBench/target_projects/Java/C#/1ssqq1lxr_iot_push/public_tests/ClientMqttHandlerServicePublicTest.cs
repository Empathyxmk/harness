using Xunit;

namespace PublicTests
{
    public class ClientMqttHandlerServicePublicTest
    {
        [Fact]
        public void TestClientMqttHandlerPublicConstruction()
        {
            var client = new DummyClientMqttHandlerService();
            Assert.NotNull(client);

            class DummyClientMqttHandlerService : ProjectName.ClientMqttHandlerService
            {
                public override void Heart(object ch, object evt) {}
                public override void Suback(object ch, object msg) {}
                public override void PubBackMessage(object ch, int i) {}
                public override void UnsubBack(object ch, object msg) {}
            }
        }
    }
}