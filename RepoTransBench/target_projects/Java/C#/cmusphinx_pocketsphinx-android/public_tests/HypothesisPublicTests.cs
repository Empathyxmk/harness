using Xunit;
using PocketSphinx;

namespace PocketSphinxTests.Public
{
    public class HypothesisPublicTests
    {
        [Fact]
        public void TestGettersWithDifferentValues()
        {
            var h = new Hypothesis("public test string", 123);
            Assert.Equal("public test string", h.GetHypstr());
            Assert.Equal(123, h.GetBestScore());
        }

        [Fact]
        public void TestWhitespaceText()
        {
            var h = new Hypothesis("    ", 1000);
            Assert.Equal("    ", h.GetHypstr());
            Assert.Equal(1000, h.GetBestScore());
        }

        [Fact]
        public void TestLargeNegativeScore()
        {
            var h = new Hypothesis("edge", -999999);
            Assert.Equal("edge", h.GetHypstr());
            Assert.Equal(-999999, h.GetBestScore());
        }
    }
}