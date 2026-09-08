using System;
using Xunit;

namespace AndroidUtils.Tests
{
    public class AnimationUtilsTest
    {
        [Fact]
        public void TestNoInstantiation()
        {
            bool thrown = false;
            try
            {
                new AnimationUtils();
            }
            catch (Exception)
            {
                thrown = true;
            }
            Assert.True(thrown);
        }
    }

    public class AnimationUtils
    {
        public AnimationUtils()
        {
            throw new Exception("No instantiation allowed");
        }
    }
}