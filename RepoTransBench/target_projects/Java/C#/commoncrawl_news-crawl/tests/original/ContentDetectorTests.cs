using System.Text;
using Xunit;
using CommonCrawlNewsCrawl.News;

namespace CommonCrawlNewsCrawl.Tests.Original
{
    public class ContentDetectorTests
    {
        [Fact]
        public void TestSimpleOrMatch()
        {
            var clues = new[] { new[] { "foo" }, new[] { "bar" } };
            var detector = new ContentDetector(clues, 100);
            Assert.Equal(0, detector.GetFirstMatch(Encoding.UTF8.GetBytes("foo hello world")));
            Assert.Equal(1, detector.GetFirstMatch(Encoding.UTF8.GetBytes("something bar here")));
            Assert.Equal(-1, detector.GetFirstMatch(Encoding.UTF8.GetBytes("baz qux")));
        }

        [Fact]
        public void TestAndMatch()
        {
            var clues = new[] { new[] { "foo", "bar" }, new[] { "baz" } };
            var detector = new ContentDetector(clues, 100);
            Assert.Equal(0, detector.GetFirstMatch(Encoding.UTF8.GetBytes("this line has foo and bar together")));
            Assert.Equal(1, detector.GetFirstMatch(Encoding.UTF8.GetBytes("some baz string")));
            Assert.Equal(-1, detector.GetFirstMatch(Encoding.UTF8.GetBytes("foo only here")));
        }

        [Fact]
        public void TestMaxOffset()
        {
            var clues = new[] { new[] { "clue" } };
            var detector = new ContentDetector(clues, 4);
            Assert.Equal(-1, detector.GetFirstMatch(Encoding.UTF8.GetBytes("say clue later")));
            Assert.Equal(0, detector.GetFirstMatch(Encoding.UTF8.GetBytes("clue here")));
        }

        [Fact]
        public void TestMatchesConvenience()
        {
            var clues = new[] { new[] { "needle" } };
            var detector = new ContentDetector(clues, 100);
            Assert.True(detector.Matches(Encoding.UTF8.GetBytes("and a needle in haystack")));
            Assert.False(detector.Matches(Encoding.UTF8.GetBytes("no match")));
        }
    }
}