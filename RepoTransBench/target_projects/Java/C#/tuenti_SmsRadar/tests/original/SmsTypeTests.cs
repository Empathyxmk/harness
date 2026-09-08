using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Original
{
    public class SmsTypeTests
    {
        [Fact]
        public void TestFromValueReceived()
        {
            Assert.Equal(SmsType.RECEIVED, SmsTypeExtensions.FromValue(1));
        }

        [Fact]
        public void TestFromValueSent()
        {
            Assert.Equal(SmsType.SENT, SmsTypeExtensions.FromValue(2));
        }

        [Fact]
        public void TestFromValueUnknown()
        {
            Assert.Equal(SmsType.UNKNOWN, SmsTypeExtensions.FromValue(-1));
        }

        [Fact]
        public void TestSmsTypeValues()
        {
            Assert.Equal(-1, SmsType.UNKNOWN.GetValue());
            Assert.Equal(1, SmsType.RECEIVED.GetValue());
            Assert.Equal(2, SmsType.SENT.GetValue());
        }

        [Fact]
        public void TestValueOfString()
        {
            Assert.Equal(SmsType.UNKNOWN, System.Enum.Parse<SmsType>("UNKNOWN"));
            Assert.Equal(SmsType.RECEIVED, System.Enum.Parse<SmsType>("RECEIVED"));
            Assert.Equal(SmsType.SENT, System.Enum.Parse<SmsType>("SENT"));
        }

        [Fact]
        public void TestFromValueInvalid()
        {
            Assert.Throws<System.ArgumentException>(() => SmsTypeExtensions.FromValue(5));
        }
    }
}