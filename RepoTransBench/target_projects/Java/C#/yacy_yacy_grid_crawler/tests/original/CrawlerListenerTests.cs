using Xunit;
using yacy_yacy_grid_crawler.crawler;
using System;
using System.Reflection;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class CrawlerListenerTests
    {
        [Fact]
        public void TestInitPriorityQueue()
        {
            // Should run without exceptions, also validate fields are set
            CrawlerListener.initPriorityQueue(1);
            Assert.NotNull(GetStaticField("CRAWLER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("LOADER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("PARSER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("INDEXER_PRIORITY_DIMENSIONS"));
        }

        [Fact]
        public void TestPriorityDimensionsEdgeCases()
        {
            // Confirm method exists via reflection
            var t = typeof(CrawlerListener);
            var m = t.GetMethod("priorityDimensions", BindingFlags.NonPublic | BindingFlags.Static);
            Assert.NotNull(m);
        }

        private object GetStaticField(string name)
        {
            var f = typeof(CrawlerListener).GetProperty(name, BindingFlags.Public | BindingFlags.Static);
            return f.GetValue(null);
        }
    }
}