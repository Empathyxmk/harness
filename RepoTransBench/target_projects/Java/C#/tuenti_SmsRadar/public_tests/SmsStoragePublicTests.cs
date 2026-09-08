using System.Collections.Generic;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsStoragePublicTests
    {
        private SmsStorage smsStorage;

        public SmsStoragePublicTests()
        {
            smsStorage = new SmsStorage();
        }

        [Fact]
        public void TestStoreAndGetSingleSms()
        {
            var sms = new Sms("Charlie", "+1987654321", "Hey there!", 1357924680L, SmsType.INBOX);
            smsStorage.StoreSms(sms);
            var retrieved = smsStorage.GetAllSms();
            Assert.Single(retrieved);
            var output = retrieved[0];
            Assert.Equal("Charlie", output.GetContact());
            Assert.Equal("+1987654321", output.GetAddress());
            Assert.Equal("Hey there!", output.GetMessage());
        }

        [Fact]
        public void TestStoreMultipleSms()
        {
            var s1 = new Sms("Delta", "+1234509876", "First msg", 1000000100L, SmsType.SENT);
            var s2 = new Sms("Echo", "+1987654322", "Second msg", 1000000200L, SmsType.OUTBOX);
            smsStorage.StoreSms(s1);
            smsStorage.StoreSms(s2);
            var list = smsStorage.GetAllSms();
            Assert.Equal(2, list.Count);
            Assert.Equal("First msg", list[0].GetMessage());
            Assert.Equal("Second msg", list[1].GetMessage());
        }

        [Fact]
        public void TestStorageIsCleared()
        {
            smsStorage.StoreSms(new Sms("Foxtrot", "+1324354657", "To clear", 1234000000L, SmsType.DRAFT));
            smsStorage.ClearAll();
            Assert.Empty(smsStorage.GetAllSms());
        }
    }
}