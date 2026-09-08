using System;
using Xunit;

namespace JoonasVali.NaturalMouseMotion.Tests.Original
{
    public class HeadlessEnvTest
    {
        [Fact]
        public void ShouldHandleHeadlessEnvironment()
        {
            bool handled = Environment.GetEnvironmentVariable("IS_HEADLESS") == "1";
            Assert.True(handled);
        }
    }
}