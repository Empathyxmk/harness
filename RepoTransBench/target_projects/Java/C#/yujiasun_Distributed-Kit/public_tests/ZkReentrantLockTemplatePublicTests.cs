using Xunit;

namespace PublicTests.Lock
{
    public class ZkReentrantLockTemplatePublicTests
    {
        [Fact]
        public void TestBasicLockingPublic()
        {
            int x = 42;
            int y = 58;
            Assert.Equal(100, x + y);
            Assert.NotEqual(x, y);
        }
    }
}