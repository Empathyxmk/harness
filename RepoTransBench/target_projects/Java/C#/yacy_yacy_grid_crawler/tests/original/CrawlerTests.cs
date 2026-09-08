using Xunit;
using yacy_yacy_grid_crawler.crawler;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class CrawlerTests
    {
        [Fact]
        public void TestCRAWLER_SERVICESContainsExpectedClasses()
        {
            bool hasDefaultValues = false, hasCrawlStart = false;

            foreach (var c in Crawler.CRAWLER_SERVICES)
            {
                if (c.Name == "CrawlerDefaultValuesService") hasDefaultValues = true;
                if (c.Name == "CrawlStartService") hasCrawlStart = true;
            }

            Assert.True(hasDefaultValues, "CRAWLER_SERVICES should contain CrawlerDefaultValuesService");
            Assert.True(hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService");
        }
    }
}