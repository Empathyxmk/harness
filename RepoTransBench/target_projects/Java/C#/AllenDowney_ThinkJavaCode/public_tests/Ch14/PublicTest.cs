using Xunit;

namespace PublicTests.Ch14
{
    public class PublicTest
    {
        [Fact]
        public void TestPlaceholder()
        {
            Assert.Equal("public".ToUpper(), "PUBLIC");
        }
    }
}