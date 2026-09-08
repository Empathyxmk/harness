using Xunit;

namespace OriginalTests
{
    public class PropertiesTest
    {
        [Fact]
        public void TestMqttProperties()
        {
            var props = new ProjectName.MqttProperties
            {
                Port = 1883,
                Host = "127.0.0.1",
                ClientId = "cid",
                Username = "user",
                Password = "pass",
                CleanSession = true,
                Keepalive = 120,
                Qos = 1
            };

            Assert.Equal(1883, props.Port);
            Assert.Equal("127.0.0.1", props.Host);
            Assert.Equal("cid", props.ClientId);
            Assert.Equal("user", props.Username);
            Assert.Equal("pass", props.Password);
            Assert.True(props.CleanSession);
            Assert.Equal(120, props.Keepalive);
            Assert.Equal(1, props.Qos);
        }
    }
}