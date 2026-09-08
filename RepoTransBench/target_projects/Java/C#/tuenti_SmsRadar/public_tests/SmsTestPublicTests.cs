using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsTestPublicTests
    {
        [Fact]
        public void TestConstructorAndGettersDifferentData()
        {
            var sms = new Sms("PublicTestContact", "+10987654321", "Hello Public Test!", 1440000000L, SmsType.DRAFT);
            Assert.Equal("PublicTestContact", sms.GetContact());
            Assert.Equal("+10987654321", sms.GetAddress());
            Assert.Equal("Hello Public Test!", sms.GetMessage());
            Assert.Equal(1440000000L, sms.GetTime());
            Assert.Equal(SmsType.DRAFT, sms.GetType());
        }

        [Fact]
        public void TestSmsEqualsDifferentData()
        {
            var sms1 = new Sms("AA", "BB", "CC", 55555555L, SmsType.OUTBOX);
            var sms2 = new Sms("AA", "BB", "CC", 55555555L, SmsType.OUTBOX);
            Assert.Equal(sms1, sms2);
        }

        [Fact]
        public void TestSmsToStringDifferentData()
        {
            var sms = new Sms("XY", "ZZ", "MessageTest", 66778899L, SmsType.DRAFT);
            var str = sms.ToString();
            Assert.Contains("XY", str);
            Assert.Contains("ZZ", str);
            Assert.Contains("MessageTest", str);
            Assert.Contains("66778899", str);
            Assert.Contains("DRAFT", str);
        }
    }
}