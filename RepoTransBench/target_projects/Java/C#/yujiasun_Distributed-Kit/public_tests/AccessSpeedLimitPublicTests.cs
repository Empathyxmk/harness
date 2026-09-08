using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;
using Moq;

namespace PublicTests.Limit
{
    public class AccessSpeedLimitPublicTests
    {
        private Mock<IJedisPool> _jedisPool;
        private Mock<IJedis> _jedis;
        private AccessSpeedLimit _accessSpeedLimit;

        public AccessSpeedLimitPublicTests()
        {
            _jedisPool = new Mock<IJedisPool>();
            _jedis = new Mock<IJedis>();
            _jedisPool.Setup(j => j.GetResource()).Returns(_jedis.Object);
            _accessSpeedLimit = new AccessSpeedLimit(_jedisPool.Object);
        }

        [Fact]
        public void TestGetSetJedisPoolPublic()
        {
            var limit = new AccessSpeedLimit();
            Assert.Null(limit.JedisPool);
            limit.JedisPool = _jedisPool.Object;
            Assert.Equal(_jedisPool.Object, limit.JedisPool);
        }

        [Fact]
        public void TestTryAccessWithTryAccessIntPublic()
        {
            _jedis.Setup(j => j.Eval(It.IsAny<string>(), It.IsAny<IList<string>>(), It.IsAny<IList<string>>())).Returns("2");
            bool result = _accessSpeedLimit.TryAccess("keyY", 8, 4);
            Assert.True(result);
        }

        [Fact]
        public void TestTryAccessFalseReturnedPublic()
        {
            _jedis.Setup(j => j.Eval(It.IsAny<string>(), It.IsAny<IList<string>>(), It.IsAny<IList<string>>())).Returns("9");
            bool result = _accessSpeedLimit.TryAccess("keyW", 15, 7);
            Assert.False(result);
        }

        [Fact]
        public void TestLuaScriptIncludesLockLogicPublic()
        {
            var rule = new LimitRule()
            {
                LimitCount = 9,
                Seconds = 20,
                LockCount = 8,
                LockTime = 30
            };
            var buildLua = typeof(AccessSpeedLimit).GetMethod("BuildLuaScript", BindingFlags.NonPublic | BindingFlags.Instance);
            string script = (string)buildLua.Invoke(_accessSpeedLimit, new object[] { rule });
            Assert.Contains("redis.call('expire',KEYS[1],ARGV[4])", script);
            Assert.True(rule.EnableLimitLock());
        }

        [Fact]
        public void TestLuaScriptExcludesLockLogicPublic()
        {
            var rule = new LimitRule()
            {
                LimitCount = 11,
                Seconds = 30,
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