using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class SmsTests
    {
        [Fact]
        public void TestConstructorAndGetters()
        {
            var sms = new Sms("12345", "1687221000000", "Hello there!", SmsType.RECEIVED);
            Assert.Equal("12345", sms.GetAddress());
            Assert.Equal("1687221000000", sms.GetDate());
            Assert.Equal("Hello there!", sms.GetMsg());
            Assert.Equal(SmsType.RECEIVED, sms.GetType());
        }

        [Fact]
        public void TestEqualsHashCodeAndToString()
        {
            var a = new Sms("a", "111", "body", SmsType.RECEIVED);
            var b = new Sms("a", "111", "body", SmsType.RECEIVED);
            var c = new Sms("b", "112", "other", SmsType.SENT);

            Assert.Equal(a, b);
            Assert.Equal(a.GetHashCode(), b.GetHashCode());
            Assert.NotEqual(a, c);
            Assert.NotEqual(a.GetHashCode(), c.GetHashCode());
            Assert.Contains("body", a.ToString());
        }

        [Fact]
        public void TestNotEqualWithNullOrOtherType()
        {
            var sms = new Sms("a", "c", "b", SmsType.UNKNOWN);
            Assert.False(sms.Equals(null));
            Assert.False(sms.Equals("Some String"));
        }
    }
}