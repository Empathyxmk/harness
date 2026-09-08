using Xunit;
using yacy_yacy_grid_crawler.crawler.api;
using System.Collections.Generic;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class CrawlerDefaultValuesServiceTests
    {
        [Fact]
        public void TestGetAPIPath()
        {
            var service = new CrawlerDefaultValuesService();
            Assert.EndsWith("/defaultValues.json", service.getAPIPath());
        }

        [Fact]
        public void TestCrawlStartDefaultClone()
        {
            var original = CrawlerDefaultValuesService.defaultValues;
            var clone = CrawlerDefaultValuesService.crawlStartDefaultClone();

            foreach (var key in original.Keys)
            {
                Assert.Equal(original[key].ToString(), clone[key].ToString());
            }

            // Different instance
            Assert.NotSame(original, clone);
        }

        [Fact]
        public void TestServiceImplReturnsDefaultValues()
        {
            var service = new CrawlerDefaultValuesService();
            var resp = service.serviceImpl(new Query(null), null);
            Assert.NotNull(resp);

            var json = resp.toJSON();
            foreach (var key in CrawlerDefaultValuesService.defaultValues.Keys)
            {
                Assert.Equal(CrawlerDefaultValuesService.defaultValues[key].ToString(), json[key].ToString());
            }
        }
    }
}