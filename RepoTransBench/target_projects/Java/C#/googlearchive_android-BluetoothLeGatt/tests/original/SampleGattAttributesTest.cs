using Xunit;
using BluetoothLeGatt;

namespace Tests.Original
{
    public class SampleGattAttributesTest
    {
        [Fact]
        public void Lookup_ReturnsCorrectNameForKnownService()
        {
            string uuid = "0000180d-0000-1000-8000-00805f9b34fb";
            string expected = "Heart Rate Service";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "Default"));
        }

        [Fact]
        public void Lookup_ReturnsCorrectNameForKnownCharacteristic()
        {
            string uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT;
            string expected = "Heart Rate Measurement";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "None"));
        }

        [Fact]
        public void Lookup_ReturnsDefaultForUnknownUuid()
        {
            string result = SampleGattAttributes.Lookup("some-unknown-uuid", "MyDefault");
            Assert.Equal("MyDefault", result);
        }

        [Fact]
        public void Lookup_DistinctForManufacturerNameString()
        {
            string uuid = "00002a29-0000-1000-8000-00805f9b34fb";
            Assert.Equal("Manufacturer Name String", SampleGattAttributes.Lookup(uuid, "None"));
        }

        [Fact]
        public void Lookup_DeviceInformationService()
        {
            string uuid = "0000180a-0000-1000-8000-00805f9b34fb";
            string expected = "Device Information Service";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "Unknown"));
        }
    }
}