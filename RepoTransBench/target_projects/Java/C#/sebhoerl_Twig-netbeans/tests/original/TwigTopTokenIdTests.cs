using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.Tests.Original
{
    public class TwigTopTokenIdTests
    {
        [Fact]
        public void TestLanguageNotNull()
        {
            var values = TwigTopTokenIdHelper.Values();
            Assert.NotNull(values);
        }
    }
}