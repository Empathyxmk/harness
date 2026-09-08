using Xunit;
using Contacts;

namespace Contacts.PublicTests
{
    public class AddressPublicTest
    {
        [Fact]
        public void TestConstructorsAndGetters_Type()
        {
            var a = new Address("Street 123", "Townsville", "AA", "CountryX", "98765", Address.Type.WORK);
            Assert.Equal("Street 123", a.Street);
            Assert.Equal("Townsville", a.City);
            Assert.Equal("AA", a.Region);
            Assert.Equal("CountryX", a.Country);
            Assert.Equal("98765", a.Postcode);
            Assert.Equal(Address.Type.WORK, a.TypeValue);
            Assert.Null(a.Label);
        }

        [Fact]
        public void TestConstructorsAndGetters_Label()
        {
            var a = new Address("Ave A", "Metropolis", "BB", "CountryY", "24680", "Vacation Spot");
            Assert.Equal("Ave A", a.Street);
            Assert.Equal("Metropolis", a.City);
            Assert.Equal("BB", a.Region);
            Assert.Equal("CountryY", a.Country);
            Assert.Equal("24680", a.Postcode);
            Assert.Equal(Address.Type.CUSTOM, a.TypeValue);
            Assert.Equal("Vacation Spot", a.Label);
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var a1 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME);
            var a2 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", Address.Type.HOME);
            var a3 = new Address("Zebra", "CityZ", "RR", "LandQ", "65432", "MyPlace");
            Assert.Equal(a1, a2);
            Assert.NotEqual(a1, a3);
            Assert.Equal(a1.GetHashCode(), a2.GetHashCode());
        }

        [Fact]
        public void TestTypeFromValue()
        {
            Assert.Equal(Address.Type.CUSTOM, Address.fromValue(-1));
            Assert.Equal(Address.Type.HOME, Address.fromValue(1));
            Assert.Equal(Address.Type.WORK, Address.fromValue(2));
            Assert.Equal(Address.Type.OTHER, Address.fromValue(3));
            Assert.Equal(Address.Type.UNKNOWN, Address.fromValue(100));
        }

        [Fact]
        public void TestNotEqualConditions()
        {
            var a1 = new Address("Alpha", "Beta", "Gamma", "Delta", "61616", Address.Type.WORK);
            Assert.False(a1.Equals(null));
            Assert.False(a1.Equals("NotAnAddress"));
            var a2 = new Address("Beta", "Gamma", "Delta", "Epsilon", "89898", Address.Type.WORK);
            Assert.NotEqual(a1, a2);
        }
    }
}