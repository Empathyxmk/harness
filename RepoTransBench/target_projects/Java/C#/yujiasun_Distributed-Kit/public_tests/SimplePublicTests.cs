using Xunit;

namespace PublicTests.Lock
{
    public class SimplePublicTests
    {
        [Fact]
        public void TestSomethingSimplePublic()
        {
            int a = 8;
            int b = 15;
            Assert.Equal(23, a + b);

            string s = "redisPublic";
            Assert.StartsWith("red", s);
            Assert.False(s.EndsWith("lock"));
        }
    }
}