using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.PublicTests
{
    public class PunycodeURLNormalizerPublicTests
    {
        [Fact]
        public void TestNormalizerDifferentIDN()
        {
            var normalizer = new PunycodeURLNormalizer();
            string idn = "http://müller.de/über-uns";
            string expected = "http://xn--mller-kva.de/%C3%BCber-uns";
            Assert.Equal(expected, normalizer.Normalize(idn));
        }

        [Fact]
        public void TestNormalizerJapaneseDomain()
        {
            var normalizer = new PunycodeURLNormalizer();
            string idn = "http://例え.テスト";
            string expected = "http://xn--r8jz45g.xn--zckzah";
            Assert.StartsWith(expected, normalizer.Normalize(idn));
        }

        [Fact]
        public void TestNormalizerNonIDN()
        {
            var normalizer = new PunycodeURLNormalizer();
            string url = "http://standard.net/news";
            Assert.Equal(url, normalizer.Normalize(url));
        }
    }
}