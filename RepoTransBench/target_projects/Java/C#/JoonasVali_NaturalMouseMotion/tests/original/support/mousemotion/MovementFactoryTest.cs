using System;
using Xunit;
using JoonasVali.NaturalMouseMotion.Support.MouseMotion;

namespace JoonasVali.NaturalMouseMotion.Tests.Original.Support.MouseMotion
{
    public class MovementFactoryTest
    {
        [Fact]
        public void ShouldCreateMovement()
        {
            var factory = new MovementFactory();
            var movement = factory.Create(100, 100);
            Assert.NotNull(movement);
            Assert.Equal(100, movement.X);
            Assert.Equal(100, movement.Y);
        }
    }
}