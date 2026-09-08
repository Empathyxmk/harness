using System;
using Xunit;

namespace AndroidUtils.Tests
{
    public class LogUtilsTest
    {
        [Fact]
        public void TestNoInstantiation()
        {
            bool thrown = false;
            try
            {
                new LogUtils();
            }
            catch (Exception)
            {
                thrown = true;
            }
            Assert.True(thrown);
        }
    }

    public class LogUtils
    {
        public LogUtils()
        {
            throw new Exception("No instantiation allowed");
        }
    }
}