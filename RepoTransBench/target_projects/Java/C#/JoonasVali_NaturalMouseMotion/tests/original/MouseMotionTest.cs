using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.Tests.Original
{
    public class MouseMotionTest
    {
        [Fact]
        public void ShouldMoveMouseSuccessfully()
        {
            var mouseMotion = new MouseMotion();
            bool moved = mouseMotion.MoveTo(150, 170);
            Assert.True(moved);
        }
    }
}