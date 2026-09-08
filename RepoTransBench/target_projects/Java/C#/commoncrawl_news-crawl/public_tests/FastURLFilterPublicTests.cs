using Xunit;
using CommonCrawlNewsCrawl;

namespace CommonCrawlNewsCrawl.PublicTests
{
    public class FastURLFilterPublicTests
    {
        [Fact]
        public void TestDifferentDomainURLAllowed()
        {
            var filter = new FastURLFilter();
            Assert.True(filter.IsAllowed("https://anotherdomain.com/index.html"));
        }

        [Fact]
        public void TestFilteredExtension()
        {
            var filter = new FastURLFilter();
            Assert.False(filter.IsAllowed("http://test.com/download/file.exe"));
        }

        [Fact]
        public void TestComplexQueryString()
        {
            var filter = new FastURLFilter();
            Assert.True(filter.IsAllowed("http://somedomain.com/page?search=stormcrawler&sort=desc"));
        }
    }
}