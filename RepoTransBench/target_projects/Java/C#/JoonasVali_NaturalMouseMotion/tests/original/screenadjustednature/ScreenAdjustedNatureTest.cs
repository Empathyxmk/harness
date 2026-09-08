using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.ScreenAdjustedNature;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.ScreenAdjustedNature
{
    public class ScreenAdjustedNatureTest
    {
        [Fact]
        public void ShouldScreenAdjustProperly()
        {
            var nature = new ScreenAdjustedNature();
            nature.SetAdjustment(0.5);
            Assert.Equal(0.5, nature.GetAdjustment());
        }
    }
}