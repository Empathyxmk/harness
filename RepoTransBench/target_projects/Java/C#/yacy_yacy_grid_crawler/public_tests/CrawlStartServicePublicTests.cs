using Xunit;
using yacy_yacy_grid_crawler.crawler.api;
using System.Collections.Generic;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class CrawlStartServicePublicTests
    {
        [Fact]
        public void TestParseTimeout_Public()
        {
            var parameters = new Dictionary<string, string[]>
            {
                { "timeout", new[] { "90" } }
            };
            int result = CrawlStartService.parseTimeout(parameters, 250);
            Assert.Equal(90, result);
        }

        [Fact]
        public void TestParseTimeout_Defaults_Public()
        {
            var parameters = new Dictionary<string, string[]>();
            int result = CrawlStartService.parseTimeout(parameters, 60);
            Assert.Equal(60, result);
        }

        [Fact]
        public void TestParseTimeout_Invalid_Public()
        {
            var parameters = new Dictionary<string, string[]>
            {
                { "timeout", new[] { "invalid" } }
            };
            int result = CrawlStartService.parseTimeout(parameters, 15);
            Assert.Equal(15, result);
        }
    }
}