using System.Collections.Generic;
using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.PublicTests
{
    public class PreFilterBoltPublicTests
    {
        [Fact]
        public void TestUrlParameterRemainsUntouched()
        {
            var bolt = new PreFilterBolt();
            var input = new Dictionary<string, string> { { "url", "http://example.net/article?id=123" } };
            var filtered = bolt.PreFilter(input);
            Assert.Equal("http://example.net/article?id=123", filtered["url"]);
        }

        [Fact]
        public void TestNonArticleUrlIsRemoved()
        {
            var bolt = new PreFilterBolt();
            var input = new Dictionary<string, string> { { "url", "http://example.org/about" } };
            var filtered = bolt.PreFilter(input);
            Assert.Null(filtered["url"]);
        }

        [Fact]
        public void TestEdgeCaseWithUnusualSubdomain()
        {
            var bolt = new PreFilterBolt();
            var input = new Dictionary<string, string> { { "url", "http://sub.subdomain.example.edu/path/to/news" } };
            var filtered = bolt.PreFilter(input);
            Assert.Equal("http://sub.subdomain.example.edu/path/to/news", filtered["url"]);
        }
    }
}