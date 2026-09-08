using System;
using Xunit;

namespace cyfonly_FLogger.Tests.Original
{
    public class CommUtilTest
    {
        [Fact]
        public void TestGetConfigByStringAndInt()
        {
            Assert.Equal("fallback", cyfonly_FLogger.utils.CommUtil.GetConfigByString("NOSUCHKEY", "fallback"));
            Assert.Equal(123, cyfonly_FLogger.utils.CommUtil.GetConfigByInt("NOSUCHINT", 123));
        }

        [Fact]
        public void TestGetConfigByLong()
        {
            long val = cyfonly_FLogger.utils.CommUtil.GetConfigByLong("NOSUCHLONG", 100L);
            Assert.Equal(100L, val);
        }

        [Fact]
        public void TestGetConfigByBoolean()
        {
            Assert.True(cyfonly_FLogger.utils.CommUtil.GetConfigByBoolean("NOSUCHBOOL", true));
            Assert.False(cyfonly_FLogger.utils.CommUtil.GetConfigByBoolean("NOSUCHBOOL", false));
        }

        [Fact]
        public void TestStringToBytes()
        {
            string s = "abc123";
            var b = cyfonly_FLogger.utils.CommUtil.StringToBytes(s);
            Assert.Equal(System.Text.Encoding.UTF8.GetBytes(s), b);
        }

        [Fact]
        public void TestGetExpStack()
        {
            Exception e = new Exception("expected");
            string stack = cyfonly_FLogger.utils.CommUtil.GetExpStack(e);
            Assert.Contains("expected", stack);
        }
    }
}