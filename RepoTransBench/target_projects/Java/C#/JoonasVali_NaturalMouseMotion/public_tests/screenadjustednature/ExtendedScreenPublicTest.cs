using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.PublicTests.ScreenAdjustedNature
{
    public class ExtendedScreenPublicTest
    {
        [Fact]
        public void ShouldInitializeExtendedScreen()
        {
            var screen = new ExtendedScreen();
            Assert.NotNull(screen);
        }
    }
}