using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.PublicTests.ScreenAdjustedNature
{
    public class ScreenAdjustedNatureDefaultsPublicTest
    {
        [Fact]
        public void ShouldGetDefaultSensitivity()
        {
            var nature = new ScreenAdjustedNature();
            double sensitivity = nature.GetDefaultSensitivity();
            Assert.Equal(1.0, sensitivity);
        }
    }
}