using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.PublicTests
{
    public class ContentDetectorPublicTests
    {
        [Fact]
        public void TestDetectsContentHtmlNews()
        {
            var detector = new ContentDetector();
            string html = "<html><head><title>Breaking World News</title></head><body><article>Some News</article></body></html>";
            Assert.True(detector.IsNewsContent(html));
        }

        [Fact]
        public void TestNonNewsContent()
        {
            var detector = new ContentDetector();
            string html = "<html><head><title>Shopping Cart</title></head><body>Item list</body></html>";
            Assert.False(detector.IsNewsContent(html));
        }

        [Fact]
        public void TestRealisticBlogContent()
        {
            var detector = new ContentDetector();
            string html = "<html><body><div class=\"blog-post\">Personal story from travel</div></body></html>";
            Assert.False(detector.IsNewsContent(html));
        }
    }
}