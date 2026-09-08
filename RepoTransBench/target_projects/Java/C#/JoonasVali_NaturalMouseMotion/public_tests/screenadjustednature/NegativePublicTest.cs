using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.PublicTests.ScreenAdjustedNature
{
    public class NegativePublicTest
    {
        [Fact]
        public void ShouldHandleNegativeInputs()
        {
            var screen = new ExtendedScreen();
            int pixels = screen.GetPixelCount(-10, -30);
            Assert.True(pixels >= 0);
        }
    }
}