using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Moq;

namespace OriginalTests.Limit
{
    public class AccessSpeedLimitUnitTests
    {
        private Mock<IJedisPool> _jedisPool;
        private Mock<IJedis> _jedis;
        private AccessSpeedLimit _accessSpeedLimit;

        public AccessSpeedLimitUnitTests()
        {
            _jedisPool = new Mock<IJedisPool>();
            _jedis = new Mock<IJedis>();
            _jedisPool.Setup(j => j.GetResource()).Returns(_jedis.Object);
            _accessSpeedLimit = new AccessSpeedLimit(_jedisPool.Object);
        }

        [Fact]
        public void TestGetSetJedisPool()
        {
            var limit = new AccessSpeedLimit();
            Assert.Null(limit.JedisPool);
            limit.JedisPool = _jedisPool.Object;
            Assert.Equal(_jedisPool.Object, limit.JedisPool);
        }

        [Fact]
        public void TestTryAccessWithTryAccessInt()
        {
            _jedis.Setup(j => j.Eval(It.IsAny<string>(), It.IsAny<IList<string>>(), It.IsAny<IList<string>>())).Returns("1");
            bool result = _accessSpeedLimit.TryAccess("keyX", 5, 3);
            Assert.True(result);
        }

        [Fact]
        public void TestTryAccessFalseReturned()
        {
            _jedis.Setup(j => j.Eval(It.IsAny<string>(), It.IsAny<IList<string>>(), It.IsAny<IList<string>>())).Returns("6");
            bool result = _accessSpeedLimit.TryAccess("keyZ", 10, 5);
            Assert.False(result);
        }

        [Fact]
        public void TestLuaScriptIncludesLockLogic()
        {
            var rule = new LimitRule()
            {
                LimitCount = 5,
                Seconds = 12,
                LockCount = 6,
                LockTime = 22
            };
            var buildLua = typeof(AccessSpeedLimit).GetMethod("BuildLuaScript", BindingFlags.NonPublic | BindingFlags.Instance);
            string script = (string)buildLua.Invoke(_accessSpeedLimit, new object[] { rule });
            Assert.Contains("redis.call('expire',KEYS[1],ARGV[4])", script);
            Assert.True(rule.EnableLimitLock());
        }

        [Fact]
        public void TestLuaScriptExcludesLockLogic()
        {
            var rule = new LimitRule()
            {
                LimitCount = 7,
                Seconds = 24,
                LockCount = 0,
                LockTime = 0
            };
            var buildLua = typeof(AccessSpeedLimit).GetMethod("BuildLuaScript", BindingFlags.NonPublic | BindingFlags.Instance);
            string script = (string)buildLua.Invoke(_accessSpeedLimit, new object[] { rule });
            Assert.DoesNotContain("ARGV[4]", script);
            Assert.False(rule.EnableLimitLock());
        }
    }
}