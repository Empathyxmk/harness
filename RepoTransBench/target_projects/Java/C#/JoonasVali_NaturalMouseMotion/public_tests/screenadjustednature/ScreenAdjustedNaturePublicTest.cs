using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.PublicTests.ScreenAdjustedNature
{
    public class ScreenAdjustedNaturePublicTest
    {
        [Fact]
        public void ShouldInitializeScreenAdjustedNature()
        {
            var nature = new ScreenAdjustedNature();
            Assert.NotNull(nature);
            Assert.True(nature.IsScreenAdjusted);
        }
    }
}