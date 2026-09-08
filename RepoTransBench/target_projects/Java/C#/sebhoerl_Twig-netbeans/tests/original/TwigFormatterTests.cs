using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigFormatterTests
    {
        [Fact]
        public void TestFormatterExists()
        {
            var formatter = new TwigFormatter();
            Assert.NotNull(formatter);
        }
    }
}