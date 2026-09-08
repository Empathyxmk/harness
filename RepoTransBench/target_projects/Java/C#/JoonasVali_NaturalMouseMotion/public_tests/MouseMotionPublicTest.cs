using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Api;

namespace JoonasVali.NaturalMouseMotion.PublicTests
{
    public class MouseMotionPublicTest
    {
        [Fact]
        public void ShouldInstantiateMouseMotion()
        {
            var mouseMotion = new MouseMotion();
            Assert.NotNull(mouseMotion);
        }
    }
}