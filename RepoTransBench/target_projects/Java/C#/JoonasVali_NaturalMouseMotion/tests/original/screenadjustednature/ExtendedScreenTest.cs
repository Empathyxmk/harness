using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.ScreenAdjustedNature
{
    public class ExtendedScreenTest
    {
        [Fact]
        public void ExtendedScreenShouldSupportGetPixels()
        {
            var screen = new ExtendedScreen();
            int pixels = screen.GetPixelCount();
            Assert.True(pixels > 0);
        }
    }
}