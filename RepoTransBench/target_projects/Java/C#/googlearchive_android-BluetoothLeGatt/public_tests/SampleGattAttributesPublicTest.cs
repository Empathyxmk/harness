using Xunit;
using BluetoothLeGatt;

namespace PublicTests
{
    public class SampleGattAttributesPublicTest
    {
        [Fact]
        public void Lookup_ReturnsCorrectNameForAnotherKnownService()
        {
            string uuid = "0000180a-0000-1000-8000-00805f9b34fb";
            string expected = "Device Information Service";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "DefaultValue"));
        }

        [Fact]
        public void Lookup_ReturnsCorrectNameForAnotherKnownCharacteristic()
        {
            string uuid = "00002a29-0000-1000-8000-00805f9b34fb";
            string expected = "Manufacturer Name String";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "OtherDefault"));
        }

        [Fact]
        public void Lookup_ReturnsDefaultForDifferentUnknownUuid()
        {
            string result = SampleGattAttributes.Lookup("unknown-public-uuid", "OtherDefaultValue");
            Assert.Equal("OtherDefaultValue", result);
        }

        [Fact]
        public void Lookup_DistinctForHeartRateMeasurement()
        {
            string uuid = SampleGattAttributes.HEART_RATE_MEASUREMENT;
            Assert.Equal("Heart Rate Measurement", SampleGattAttributes.Lookup(uuid, "UnknownValue"));
        }

        [Fact]
        public void Lookup_HeartRateService()
        {
            string uuid = "0000180d-0000-1000-8000-00805f9b34fb";
            string expected = "Heart Rate Service";
            Assert.Equal(expected, SampleGattAttributes.Lookup(uuid, "NewUnknown"));
        }
    }
}