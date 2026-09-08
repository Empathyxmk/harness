using System;
using Xunit;
using CommonCrawlNewsCrawl;

namespace CommonCrawlNewsCrawl.Tests.Original
{
    public class FastURLFilterTests
    {
        private static readonly FastURLFilter filter = new FastURLFilter();

        [Fact]
        public void TestHostFilter()
        {
            var url = new Uri("http://may.go.com/image.jpg");
            var metadata = new Metadata();
            var filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Equal(url.ToString(), filterResult);

            url = new Uri("http://no.go.com/");
            filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Null(filterResult);
        }

        [Fact]
        public void TestDomainNotAllowed()
        {
            var metadata = new Metadata();

            var url = new Uri("http://domainnotallowed.com/forum/search.php");
            var filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Null(filterResult);

            url = new Uri("http://domainnotallowed.com/");
            filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Null(filterResult);

            url = new Uri("http://partiallyallowed.com/");
            filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Equal(url.ToString(), filterResult);

            url = new Uri("http://partiallyallowed.com/verbotten");
            filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Null(filterResult);

            url = new Uri("http://digitalpebble.com/");
            filterResult = filter.Filter(url, metadata, url.ToString());
            Assert.Equal(url.ToString(), filterResult);
        }
    }
}