using Xunit;

namespace Skydoves.PreferenceRoom.PublicTests
{
    public class Device
    {
        public string DeviceName { get; }
        public string DeviceType { get; }
        public string MacAddress { get; private set; }

        public Device(string context, string deviceName, string deviceType)
        {
            DeviceName = deviceName;
            DeviceType = deviceType;
        }

        public void SetMacAddress(string mac) => MacAddress = mac;
        public string GetDeviceName() => DeviceName;
        public string GetDeviceType() => DeviceType;
        public string GetMacAddress() => MacAddress;
    }

    public class DeviceEntityPublicTests
    {
        private Device publicDevice;

        public DeviceEntityPublicTests()
        {
            publicDevice = new Device("context", "public_device_alpha", "public_type_beta");
            publicDevice.SetMacAddress("AA:BB:CC:DD:EE:FF");
        }

        [Fact]
        public void TestDeviceNamePublic()
        {
            Assert.Equal("public_device_alpha", publicDevice.GetDeviceName());
        }

        [Fact]
        public void TestDeviceTypePublic()
        {
            Assert.Equal("public_type_beta", publicDevice.GetDeviceType());
        }

        [Fact]
        public void TestMacAddressPublic()
        {
            Assert.Equal("AA:BB:CC:DD:EE:FF", publicDevice.GetMacAddress());
        }
    }
}