using Xunit;

namespace Skydoves.PreferenceRoom.PublicTests
{
    // Simulate JunitComponent for public test
    public class JunitComponent
    {
        public string DeviceId { get; }

        public JunitComponent(string context, string deviceId)
        {
            DeviceId = deviceId;
        }

        public string GetDeviceId() => DeviceId;
    }

    public class JunitComponentPublicTests
    {
        private JunitComponent publicJunitComponent;

        public JunitComponentPublicTests()
        {
            publicJunitComponent = new JunitComponent("context", "public_device_id");
        }

        [Fact]
        public void TestDeviceIdIsSetPublic()
        {
            Assert.Equal("public_device_id", publicJunitComponent.GetDeviceId());
        }

        [Fact]
        public void TestDeviceIdIsNotDefaultPublic()
        {
            Assert.NotEqual("DEFAULT_DEVICE", publicJunitComponent.GetDeviceId());
        }
    }
}