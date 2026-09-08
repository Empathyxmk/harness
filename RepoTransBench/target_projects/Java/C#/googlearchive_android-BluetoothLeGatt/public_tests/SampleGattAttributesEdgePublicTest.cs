using Xunit;
using BluetoothLeGatt;

namespace PublicTests
{
    public class SampleGattAttributesEdgePublicTest
    {
        [Fact]
        public void Lookup_NullUuid_ReturnsAlternateDefault()
        {
            Assert.Equal("alt-default", SampleGattAttributes.Lookup(null, "alt-default"));
        }

        [Fact]
        public void Lookup_EmptyUuid_ReturnsAnotherDefault()
        {
            Assert.Equal("no-value", SampleGattAttributes.Lookup("", "no-value"));
        }

        [Fact]
        public void Lookup_NullDefault_ReturnsNullForAnotherUnknown()
        {
            Assert.Null(SampleGattAttributes.Lookup("another-notfound-uuid", null));
        }
    }
}