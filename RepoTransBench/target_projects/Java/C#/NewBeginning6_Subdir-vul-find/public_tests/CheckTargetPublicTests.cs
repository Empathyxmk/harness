using Xunit;
using NewBeginning6_Subdir.Models;

namespace NewBeginning6_Subdir.PublicTests
{
    public class CheckTargetPublicTests
    {
        [Fact]
        public void TestIsValidUrl()
        {
            Assert.True(CheckTarget.IsTarget("https://www.wikipedia.org"));
            Assert.True(CheckTarget.IsTarget("http://localhost:8000/test"));
            Assert.False(CheckTarget.IsTarget("file:///tmp/test.txt"));
            Assert.False(CheckTarget.IsTarget("not_a_url"));
        }

        [Fact]
        public void TestHostLogic()
        {
            Assert.Equal("example.com", CheckTarget.Host("http://example.com/page"));
            Assert.Equal("localhost", CheckTarget.Host("https://localhost:1234"));
            Assert.Equal("", CheckTarget.Host("file:///tmp/test.txt"));
        }
    }
}