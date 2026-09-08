using Xunit;
using yacy_yacy_grid_crawler.crawler.api;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class CrawlerDefaultValuesServicePublicTests
    {
        [Fact]
        public void TestGetDefaultTimeout_Public()
        {
            int defaultTimeout = CrawlerDefaultValuesService.getDefaultTimeout();
            Assert.True(defaultTimeout > 0);
        }

        [Fact]
        public void TestDefaultValuesConstants_Public()
        {
            int depth = CrawlerDefaultValuesService.defaultMaxDepth;
            int links = CrawlerDefaultValuesService.defaultMaxLinks;
            Assert.True(depth > 0 && links > 0);
            Assert.True(depth != 0 && links != 0);
        }
    }
}