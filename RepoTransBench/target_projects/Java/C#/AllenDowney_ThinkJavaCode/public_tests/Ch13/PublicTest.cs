using Xunit;

namespace PublicTests.Ch13
{
    public class PublicTest
    {
        [Fact]
        public void TestPublicLogic()
        {
            Assert.False(5 > 10);
        }
    }
}