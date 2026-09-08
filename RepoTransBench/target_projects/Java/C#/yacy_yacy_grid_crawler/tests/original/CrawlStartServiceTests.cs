using Xunit;
using yacy_yacy_grid_crawler.crawler.api;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class CrawlStartServiceTests
    {
        [Fact]
        public void TestGetAPIPath()
        {
            var service = new CrawlStartService();
            Assert.EndsWith("/crawlStart.json", service.getAPIPath());
        }

        [Fact]
        public void TestServiceImplReturnsMergedDefaults()
        {
            var service = new CrawlStartService();
            var call = new Query(null);
            var resp = service.serviceImpl(call, null);
            Assert.NotNull(resp);

            var json = resp.toJSON();
            Assert.True(json.ContainsKey("crawlingDepth"), "Missing crawlingDepth");
            Assert.True(json.ContainsKey("mustmatch"), "Missing mustmatch");
            Assert.True(json.ContainsKey("user_id"), "Missing user_id");
            Assert.True(json.ContainsKey("crawlingURL"), "Missing crawlingURL");
        }

        [Fact]
        public void TestServiceImplWithOverride()
        {
            var service = new CrawlStartService();
            var call = new Query(null);
            call.Set("crawlingDepth", 10);
            call.Set("user_id", "user42");
            var resp = service.serviceImpl(call, null);
            var json = resp.toJSON();
            Assert.Equal(8, (int)json["crawlingDepth"]);
            Assert.Equal("user42", json["user_id"]);
        }
    }
}