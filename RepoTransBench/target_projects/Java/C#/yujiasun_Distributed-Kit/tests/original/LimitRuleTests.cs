using Xunit;

namespace OriginalTests.Limit
{
    public class LimitRuleTests
    {
        [Fact]
        public void TestGettersAndSetters()
        {
            var rule = new LimitRule();
            rule.Seconds = 15;
            rule.LimitCount = 10;
            rule.LockCount = 3;
            rule.LockTime = 120;

            Assert.Equal(15, rule.Seconds);
            Assert.Equal(10, rule.LimitCount);
            Assert.Equal(3, rule.LockCount);
            Assert.Equal(120, rule.LockTime);
        }

        [Fact]
        public void TestEnableLimitLockFalseWhenZero()
        {
            var rule = new LimitRule();
            rule.LockTime = 0;
            rule.LockCount = 0;

            Assert.False(rule.EnableLimitLock());
        }

        [Fact]
        public void TestEnableLimitLockFalseWhenOneZero()
        {
            var rule = new LimitRule();
            rule.LockTime = 5;
            rule.LockCount = 0;
            Assert.False(rule.EnableLimitLock());

            rule.LockTime = 0;
            rule.LockCount = 5;
            Assert.False(rule.EnableLimitLock());
        }

        [Fact]
        public void TestEnableLimitLockTrue()
        {
            var rule = new LimitRule();
            rule.LockTime = 10;
            rule.LockCount = 3;
            Assert.True(rule.EnableLimitLock());
        }
    }
}