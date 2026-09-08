using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.ScreenAdjustedNature
{
    public class ScreenAdjustedNatureDefaultsTest
    {
        [Fact]
        public void ShouldSetAndGetSensitivity()
        {
            var nature = new ScreenAdjustedNature();
            nature.SetSensitivity(1.2);
            Assert.Equal(1.2, nature.GetSensitivity());
        }
    }
}