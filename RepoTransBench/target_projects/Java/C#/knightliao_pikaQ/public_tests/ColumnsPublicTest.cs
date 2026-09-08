using Xunit;

namespace KnightliaoPikaQ.PublicTests
{
    public static class Columns
    {
        public const string NAME = "name";
        public const string CAMPAIGN_ID = "campaignId";
    }

    public class ColumnsPublicTest
    {
        [Fact]
        public void TestNameConstantNotNull()
        {
            Assert.NotNull(Columns.NAME);
            Assert.True(Columns.NAME.Length > 2);
        }

        [Fact]
        public void TestCampaignIdConstantHasId()
        {
            Assert.EndsWith("Id", Columns.CAMPAIGN_ID, System.StringComparison.OrdinalIgnoreCase);
        }
    }
}