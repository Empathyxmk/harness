using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigCompletionHandlerPublicTests
    {
        [Fact]
        public void TestDummyCompletionForPublic()
        {
            string sampleText = "{# This is a comment #}";
            Assert.NotNull(sampleText);
            Assert.True(sampleText.StartsWith("{#"));
        }
    }
}