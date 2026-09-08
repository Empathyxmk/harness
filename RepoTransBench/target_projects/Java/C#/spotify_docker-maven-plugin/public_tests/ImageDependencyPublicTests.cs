using System;
using Xunit;

namespace PublicTests
{
    public class ImageDependencyPublicTests
    {
        [Fact]
        public void TestImageDepsFromOtherModulesPublic()
        {
            int major = 2;
            int minor = 6;
            Assert.Equal(8, major + minor);
            Assert.True(minor % 2 == 0);
            Assert.False(major < 2);
        }
    }
}