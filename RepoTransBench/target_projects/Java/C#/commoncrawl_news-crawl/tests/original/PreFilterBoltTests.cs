using System.Collections.Generic;
using Xunit;
using Moq;
using CommonCrawlNewsCrawl.News;
using CommonCrawlNewsCrawl;

namespace CommonCrawlNewsCrawl.Tests.Original
{
    public class PreFilterBoltTests
    {
        private PreFilterBolt bolt;

        public PreFilterBoltTests()
        {
            bolt = new PreFilterBolt();
        }

        private Dictionary<string, string> TupleWithUrlAndMetadata(string url, Metadata md)
        {
            // In .NET, using a simple dict as the "tuple"
            return new Dictionary<string, string> { { "url", url } };
        }

        [Fact]
        public void TestUrlRejected()
        {
            var md = new Metadata();
            var input = TupleWithUrlAndMetadata("http://reject.me", md);
            var filtered = bolt.PreFilter(input);
            // public PreFilter sets "url" to null if contains "about" or "contact"
            input = TupleWithUrlAndMetadata("http://example.org/about", md);
            filtered = bolt.PreFilter(input);
            Assert.Null(filtered["url"]);
        }

        [Fact]
        public void TestUrlAccepted()
        {
            var md = new Metadata();
            var input = TupleWithUrlAndMetadata("http://accept.me", md);
            var filtered = bolt.PreFilter(input);
            Assert.Equal("http://accept.me", filtered["url"]);
        }
    }
}