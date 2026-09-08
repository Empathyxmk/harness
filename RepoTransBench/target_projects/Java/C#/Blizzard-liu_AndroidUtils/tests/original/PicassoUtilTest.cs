using System;
using Xunit;

namespace AndroidUtils.Tests
{
    public class PicassoUtilTest
    {
        [Fact]
        public void TestNoInstantiation()
        {
            bool thrown = false;
            try
            {
                new PicassoUtil();
            }
            catch (Exception)
            {
                thrown = true;
            }
            Assert.True(thrown);
        }
    }

    public class PicassoUtil
    {
        public PicassoUtil()
        {
            throw new Exception("No instantiation allowed");
        }
    }
}