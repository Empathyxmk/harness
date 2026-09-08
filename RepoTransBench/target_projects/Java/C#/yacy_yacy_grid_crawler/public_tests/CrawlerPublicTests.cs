using Xunit;
using yacy_yacy_grid_crawler.crawler;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class CrawlerPublicTests
    {
        [Fact]
        public void TestCRAWLER_SERVICESContainsExpectedClasses_Public()
        {
            bool hasDefaultValues = false, hasCrawlStart = false;

            foreach (var c in Crawler.CRAWLER_SERVICES)
            {
                if (c.Name.EndsWith("DefaultValuesService")) hasDefaultValues = true;
                if (c.Name.EndsWith("CrawlStartService")) hasCrawlStart = true;
            }

            Assert.True(hasDefaultValues, "CRAWLER_SERVICES should contain DefaultValuesService");
            Assert.True(hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService");
        }
    }
}