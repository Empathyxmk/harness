using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.Tests.Original
{
    public class PunycodeURLNormalizerTests
    {
        private static readonly PunycodeURLNormalizer normalizer = new PunycodeURLNormalizer();

        [Fact]
        public void TestAsciiURL()
        {
            var url = "http://example.com";
            Assert.Equal(url, normalizer.Filter(null, null, url));
        }

        [Fact]
        public void TestPunycodeURL()
        {
            var url = "http://例え.テスト";
            var normalized = normalizer.Filter(null, null, url);
            Assert.StartsWith("http://xn--r8jz45g.xn--zckzah", normalized);
        }

        [Fact]
        public void TestNonHostPartIsNotChanged()
        {
            var url = "http://täst.de/foo?ä=ö";
            var result = normalizer.Filter(null, null, url);
            Assert.StartsWith("http://xn--tst-qla.de", result);
            Assert.Contains("/foo", result);
            Assert.Contains("?", result);
        }

        [Fact]
        public void TestMalformedURL()
        {
            var url = "not a url";
            Assert.Null(normalizer.Filter(null, null, url));
        }

        [Fact]
        public void TestHostAlreadyPunycode()
        {
            var puny = "http://xn--fsq.xn--0zwm56d";
            Assert.Equal(puny, normalizer.Filter(null, null, puny));
        }
    }
}