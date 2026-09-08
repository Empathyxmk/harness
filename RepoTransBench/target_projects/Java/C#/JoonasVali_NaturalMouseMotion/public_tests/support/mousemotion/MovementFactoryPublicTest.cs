using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support.MouseMotion;

namespace JoonasVali.NaturalMouseMotion.PublicTests.Support.MouseMotion
{
    public class MovementFactoryPublicTest
    {
        [Fact]
        public void ShouldCreateMovementWithDefaultValues()
        {
            var factory = new MovementFactory();
            var movement = factory.Create(0, 0);
            Assert.Equal(0, movement.X);
            Assert.Equal(0, movement.Y);
        }
    }
}