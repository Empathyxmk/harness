using System;
using Xunit;

namespace LatencyUtils.Tests.Public
{
    public class SimplePauseDetectorPublicTests
    {
        [Fact]
        public void TestGetResolution()
        {
            var detector = new SimplePauseDetector(10, 4);
            Assert.Equal(10, detector.GetResolutionMillis());
        }

        [Fact]
        public void TestSetVerbose()
        {
            var detector = new SimplePauseDetector(3, 2);
            detector.SetVerbose(true);
            Assert.True(detector.IsVerbose());
            detector.SetVerbose(false);
            Assert.False(detector.IsVerbose());
        }
    }
}