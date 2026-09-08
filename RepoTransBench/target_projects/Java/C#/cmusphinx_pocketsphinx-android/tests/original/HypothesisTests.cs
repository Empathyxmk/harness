using Xunit;
using PocketSphinx;

namespace PocketSphinxTests.Original
{
    public class HypothesisTests
    {
        [Fact]
        public void TestGetters()
        {
            var h = new Hypothesis("hello world", 42);
            Assert.Equal("hello world", h.GetHypstr());
            Assert.Equal(42, h.GetBestScore());
        }

        [Fact]
        public void TestEmptyText()
        {
            var h = new Hypothesis("", 0);
            Assert.Equal("", h.GetHypstr());
            Assert.Equal(0, h.GetBestScore());
        }

        [Fact]
        public void TestNegativeScore()
        {
            var h = new Hypothesis("neg", -1);
            Assert.Equal("neg", h.GetHypstr());
            Assert.Equal(-1, h.GetBestScore());
        }
    }
}