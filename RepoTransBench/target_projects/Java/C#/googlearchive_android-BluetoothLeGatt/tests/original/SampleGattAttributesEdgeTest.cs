using Xunit;
using BluetoothLeGatt;

namespace Tests.Original
{
    public class SampleGattAttributesEdgeTest
    {
        [Fact]
        public void Lookup_NullUuid_ReturnsDefault()
        {
            Assert.Equal("default", SampleGattAttributes.Lookup(null, "default"));
        }

        [Fact]
        public void Lookup_EmptyUuid_ReturnsDefault()
        {
            Assert.Equal("empty", SampleGattAttributes.Lookup("", "empty"));
        }

        [Fact]
        public void Lookup_NullDefault_ReturnsNullForUnknown()
        {
            Assert.Null(SampleGattAttributes.Lookup("notfound-uuid", null));
        }
    }
}