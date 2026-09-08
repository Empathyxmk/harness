using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsTypePublicTests
    {
        [Fact]
        public void TestValueOf()
        {
            var type = System.Enum.Parse<SmsType>("INBOX");
            Assert.Equal(SmsType.INBOX, type);

            type = System.Enum.Parse<SmsType>("SENT");
            Assert.Equal(SmsType.SENT, type);
        }

        [Fact]
        public void TestOrdinalDifferentFromTest()
        {
            Assert.NotEqual("SENT".GetHashCode(), (int)SmsType.OUTBOX);
        }

        [Fact]
        public void TestValuesArrayLength()
        {
            var values = System.Enum.GetValues(typeof(SmsType));
            Assert.True(values.Length > 1);
        }
    }
}