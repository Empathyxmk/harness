using Xunit;
using yacy_yacy_grid_crawler.crawler;
using System;
using System.Reflection;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class CrawlerListenerPublicTests
    {
        [Fact]
        public void TestInitPriorityQueue_Public()
        {
            CrawlerListener.initPriorityQueue(2);
            Assert.NotNull(GetStaticField("CRAWLER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("LOADER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("PARSER_PRIORITY_DIMENSIONS"));
            Assert.NotNull(GetStaticField("INDEXER_PRIORITY_DIMENSIONS"));
        }

        [Fact]
        public void TestPriorityDimensionsEdgeCases_Public()
        {
            // Try/catch for reflection errors
            MethodInfo m = null;
            try
            {
                m = typeof(CrawlerListener).GetMethod("priorityDimensions", BindingFlags.NonPublic | BindingFlags.Static);
            }
            catch (Exception e)
            {
                Assert.True(false, "Method not found: " + e.Message);
            }
            Assert.NotNull(m);
        }

        private object GetStaticField(string name)
        {
            var f = typeof(CrawlerListener).GetProperty(name, BindingFlags.Public | BindingFlags.Static);
            return f.GetValue(null);
        }
    }
}