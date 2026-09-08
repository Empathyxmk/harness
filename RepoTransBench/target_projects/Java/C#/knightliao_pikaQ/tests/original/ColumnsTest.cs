using Xunit;

namespace KnightliaoPikaQ.Tests.Original
{
    // Simulate Columns class with constants
    public static class Columns
    {
        public const string NAME = "name";
        public const string CAMPAIGN_ID = "campaignId";
    }

    public class ColumnsTest
    {
        [Fact]
        public void TestNameConstant()
        {
            Assert.Equal("name", Columns.NAME);
        }

        [Fact]
        public void TestCampaignIdConstant()
        {
            Assert.Equal("campaignId", Columns.CAMPAIGN_ID);
        }
    }
}