using Xunit;
using Contacts;

namespace Contacts.OriginalTests
{
    public class AddressTest
    {
        [Fact]
        public void TestGettersAndConstructors_Type()
        {
            var a = new Address("addr", "str", "city", "reg", "zip", "country", Address.Type.HOME);
            Assert.Equal("addr", a.FormattedAddress);
            Assert.Equal("str", a.Street);
            Assert.Equal("city", a.City);
            Assert.Equal("reg", a.Region);
            Assert.Equal("zip", a.Postcode);
            Assert.Equal("country", a.Country);
            Assert.Null(a.Label);
            Assert.Equal(Address.Type.HOME, a.TypeValue);
        }

        [Fact]
        public void TestGettersAndConstructors_Label()
        {
            var a = new Address("addr", "str", "city", "reg", "zip", "country", "myLabel");
            Assert.Equal("myLabel", a.Label);
            Assert.Equal(Address.Type.CUSTOM, a.TypeValue);
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Address.Type.CUSTOM, Address.fromValue(0));
            Assert.Equal(Address.Type.HOME, Address.fromValue(1));
            Assert.Equal(Address.Type.WORK, Address.fromValue(2));
            Assert.Equal(Address.Type.OTHER, Address.fromValue(3));
            Assert.Equal(Address.Type.UNKNOWN, Address.fromValue(99));
        }
    }
}