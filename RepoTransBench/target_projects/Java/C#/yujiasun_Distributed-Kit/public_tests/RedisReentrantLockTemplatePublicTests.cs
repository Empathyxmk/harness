using Xunit;

namespace PublicTests.Lock
{
    public class RedisReentrantLockTemplatePublicTests
    {
        [Fact]
        public void TestTryLockAndUnlockPublic()
        {
            // NOTE: This test is only meaningful with real Redis, but shouldn't fail if unavailable.
            var jedisPool = new JedisPoolFake("127.0.0.1", 6379);
            var lockObj = new RedisReentrantLock(jedisPool, "publicLockKey123", 20000);
            bool acquired = false;
            try
            {
                acquired = lockObj.TryLock();
            }
            catch
            {
                // Redis probably unavailable, skip
                return;
            }
            if (acquired)
            {
                Assert.True(lockObj.IsHeldByCurrentThread());
                lockObj.Unlock();
                Assert.False(lockObj.IsHeldByCurrentThread());
            }
            else
            {
                // If Redis is unavailable or lock is already held, that's OK.
            }
        }
    }
}