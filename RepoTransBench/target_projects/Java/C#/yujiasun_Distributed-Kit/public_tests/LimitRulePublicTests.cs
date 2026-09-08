using Xunit;

namespace PublicTests.Limit
{
    public class LimitRulePublicTests
    {
        [Fact]
        public void TestGettersAndSettersPublic()
        {
            var rule = new LimitRule();
            rule.Seconds = 25;
            rule.LimitCount = 12;
            rule.LockCount = 5;
            rule.LockTime = 200;

            Assert.Equal(25, rule.Seconds);
            Assert.Equal(12, rule.LimitCount);
            Assert.Equal(5, rule.LockCount);
            Assert.Equal(200, rule.LockTime);
        }

        [Fact]
        public void TestEnableLimitLockFalseWhenZeroPublic()
        {
            var rule = new LimitRule();
            rule.LockTime = 0;
            rule.LockCount = 0;

            Assert.False(rule.EnableLimitLock());
        }

        [Fact]
        public void TestEnableLimitLockFalseWhenOneZeroPublic()
        {
            var rule = new LimitRule();
            rule.LockTime = 8;
            rule.LockCount = 0;

            Assert.False(rule.EnableLimitLock());

            rule.LockTime = 0;
            rule.LockCount = 6;

            Assert.False(rule.EnableLimitLock());
        }

        [Fact]
        public void TestEnableLimitLockTruePublic()
        {
            var rule = new LimitRule();
            rule.LockTime = 15;
            rule.LockCount = 4;

            Assert.True(rule.EnableLimitLock());
        }
    }
}