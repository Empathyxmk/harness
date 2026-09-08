using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.ScreenAdjustedNature
{
    public class NegativeTest
    {
        [Fact]
        public void OriginalScreenShouldReturnZeroOnNegativePixelRequest()
        {
            var screen = new ExtendedScreen();
            int pixels = screen.GetPixelCount(-1, -1);
            Assert.Equal(0, pixels);
        }
    }
}