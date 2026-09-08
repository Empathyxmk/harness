using System.Collections.Generic;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SmsCursorParserPublicTests
    {
        [Fact]
        public void TestParseSingleSmsRow()
        {
            var rows = new List<string[]>
            {
                new[] { "+3450000000", "Text from Eve", "Eve", "1600000000000", "3" }
            };
            var smses = SmsCursorParser.Parse(rows);
            Assert.Single(smses);
            var sms = smses[0];
            Assert.Equal("+3450000000", sms.GetAddress());
            Assert.Equal("Text from Eve", sms.GetMessage());
            Assert.Equal("Eve", sms.GetContact());
            Assert.Equal(1600000000000L, sms.GetTime());
            Assert.Equal(SmsType.INBOX, sms.GetType());
        }

        [Fact]
        public void TestParseMultipleSmsRows()
        {
            var rows = new List<string[]>
            {
                new[] {"123", "Bulk1", "A", "1600001", "1"},
                new[] {"456", "Bulk2", "B", "1600002", "2"}
            };
            var smses = SmsCursorParser.Parse(rows);
            Assert.Equal(2, smses.Count);
            Assert.Equal("Bulk1", smses[0].GetMessage());
            Assert.Equal(SmsType.SENT, smses[1].GetType());
        }
    }
}