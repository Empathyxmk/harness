using System.Collections.Generic;
using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.PublicTests
{
    public class NewsSiteMapParserPublicTests
    {
        [Fact]
        public void TestParseAlternativeSitemap()
        {
            var parser = new NewsSiteMapParser();
            var xml = "<?xml version=\"1.0\"?><urlset><url><loc>http://different.com/news/1</loc></url><url><loc>http://different.com/news/2</loc></url></urlset>";
            var urls = parser.Parse(xml);
            Assert.Contains("http://different.com/news/1", urls);
            Assert.Contains("http://different.com/news/2", urls);
            Assert.Equal(2, urls.Count);
        }

        [Fact]
        public void TestParseNewsSitemapWithNamespace()
        {
            var parser = new NewsSiteMapParser();
            var xml = "<?xml version=\"1.0\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://site.org/latest/45</loc></url></urlset>";
            var urls = parser.Parse(xml);
            Assert.Contains("http://site.org/latest/45", urls);
            Assert.Single(urls);
        }

        [Fact]
        public void TestEmptySitemap()
        {
            var parser = new NewsSiteMapParser();
            var xml = "<?xml version=\"1.0\"?><urlset></urlset>";
            var urls = parser.Parse(xml);
            Assert.NotNull(urls);
            Assert.Empty(urls);
        }
    }
}