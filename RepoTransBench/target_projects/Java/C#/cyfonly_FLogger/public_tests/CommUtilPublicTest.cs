using System;
using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class CommUtilPublicTest
    {
        [Fact]
        public void TestGetConfigByString_Public()
        {
            // Existing probably asserts default config values, use different default and key
            string val = cyfonly_FLogger.utils.CommUtil.GetConfigByString("NONEXIST_PUBLIC_KEY", "DifferentDefaultPublic");
            Assert.Equal("DifferentDefaultPublic", val);
        }

        [Fact]
        public void TestGetConfigByBoolean_Public()
        {
            bool b1 = cyfonly_FLogger.utils.CommUtil.GetConfigByBoolean("NONEXIST_PUBLIC_BOOL", true);
            Assert.True(b1);
            bool b2 = cyfonly_FLogger.utils.CommUtil.GetConfigByBoolean("NONEXIST_PUBLIC_BOOL", false);
            Assert.False(b2);
        }

        [Fact]
        public void TestGetExpStack_Public()
        {
            Exception e = new ArgumentException("PublicStackTrace");
            string stack = cyfonly_FLogger.utils.CommUtil.GetExpStack(e);
            Assert.Contains("System.ArgumentException", stack);
            Assert.Contains("PublicStackTrace", stack);
        }
    }
}